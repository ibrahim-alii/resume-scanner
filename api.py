import os
import tempfile
from contextlib import asynccontextmanager
from typing import Dict, List

from google import genai
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

from app import (
    compare_skills_from_text,
    composite_score,
    extract_skills_as_set,
    extract_text,
)

# Load environment variables
load_dotenv()

# Global variables for model caching
bert_model = None
gemini_model = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Pre-load ML models at startup to avoid first-request delay"""
    global bert_model, gemini_model

    print("[*] Loading BERT model...")
    bert_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    print("[+] BERT model loaded successfully")

    # Configure Gemini
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if gemini_api_key and gemini_api_key != "your_gemini_api_key_here":
        print("[*] Configuring Gemini API...")
        gemini_client = genai.Client(api_key=gemini_api_key)
        gemini_model = gemini_client
        print("[+] Gemini API configured successfully")
    else:
        print("[!] Warning: GEMINI_API_KEY not set. AI feedback will be disabled.")
        gemini_model = None

    yield

    print("[*] Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="ResuMax API",
    description="Resume analysis API with BERT + TF-IDF scoring and Gemini feedback",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite and React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for responses
class CompositeScoreResponse(BaseModel):
    composite_score: float
    bert_score: float
    tfidf_score: float
    breakdown: Dict[str, str]


class SkillsComparisonResponse(BaseModel):
    matching: List[str]
    missing: List[str]
    additional: List[str]
    match_percentage: float
    total_job_skills: int
    total_resume_skills: int
    matching_count: int
    missing_count: int
    additional_count: int


class AnalysisResponse(BaseModel):
    success: bool
    data: Dict


def generate_gemini_feedback(
    composite_score_data: Dict,
    skills_comparison: Dict,
    resume_text: str,
    job_description: str
) -> str:
    """Generate personalized resume feedback using Gemini AI"""
    if gemini_model is None:
        return "AI feedback unavailable (Gemini API key not configured)"

    try:
        # Build prompt
        prompt = f"""You are an expert resume consultant. Analyze this resume against the job description and provide 3-5 actionable, specific suggestions to improve the resume.

**Job Description:**
{job_description[:500]}...

**Resume Analysis:**
- Overall Match Score: {composite_score_data['composite_score']}/100
- BERT Semantic Score: {composite_score_data['bert_score']}/100
- TF-IDF Keyword Score: {composite_score_data['tfidf_score']}/100
- Matching Skills: {', '.join(skills_comparison['matching'][:10])}
- Missing Key Skills: {', '.join(skills_comparison['missing'][:10])}

**Instructions:**
- Provide SPECIFIC, actionable advice (not generic tips)
- Focus on the biggest gaps first (missing skills, low scores)
- Suggest HOW to add or emphasize relevant experience
- Keep each suggestion to 1-2 sentences
- Number each suggestion (1., 2., 3., etc.)
- Be encouraging but honest

Provide your feedback now:"""

        # Generate response using new API
        response = gemini_model.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt
        )
        return response.text

    except Exception as e:
        print(f"[!] Gemini API error: {str(e)}")
        return f"AI feedback temporarily unavailable. Error: {str(e)}"


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "bert_loaded": bert_model is not None,
        "gemini_loaded": gemini_model is not None
    }


@app.post("/api/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Analyze resume against job description.
    Returns scores, skills comparison, and AI feedback.
    """
    # Validate file type
    if not file.filename.endswith(('.pdf', '.docx')):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported"
        )

    # Validate file size (10MB max)
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File size must be less than 10MB"
        )

    # Save to temporary file
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(content)
        temp_path = tmp.name

    try:
        # Extract text from resume
        print(f"[*] Extracting text from {file.filename}...")
        resume_text = extract_text(temp_path)

        if not resume_text or len(resume_text.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Could not extract sufficient text from resume. Please ensure it's a valid PDF/DOCX file."
            )

        print(f"[+] Extracted {len(resume_text)} characters")

        # Calculate composite score (BERT + TF-IDF)
        print("[*] Calculating scores...")
        score_data = composite_score(resume_text, job_description)
        print(f"[+] Composite Score: {score_data['composite_score']}/100")

        # Compare skills
        print("[*] Comparing skills...")
        skills_comp = compare_skills_from_text(resume_text, job_description)
        print(f"[+] Found {skills_comp['matching_count']} matching skills, {skills_comp['missing_count']} missing")

        # Generate Gemini feedback
        print("[*] Generating AI feedback...")
        gemini_feedback = generate_gemini_feedback(
            score_data,
            skills_comp,
            resume_text,
            job_description
        )
        print("[+] AI feedback generated")

        return {
            "success": True,
            "data": {
                "composite_score": score_data,
                "skills_comparison": skills_comp,
                "gemini_feedback": gemini_feedback
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"[!] Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.unlink(temp_path)


if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print("ResuMax API Server")
    print("=" * 60)
    print("API Documentation: http://localhost:8000/docs")
    print("Health Check: http://localhost:8000/api/health")
    print("=" * 60)

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
