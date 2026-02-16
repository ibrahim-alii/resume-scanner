import os
import tempfile
from contextlib import asynccontextmanager
from typing import Dict, List

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

from app import (
    compare_skills_from_text,
    composite_score,
    extract_text,
    extract_skills_hybrid,
)

# Load environment variables (.env values override existing shell vars)
load_dotenv(override=True)

# Global variables for model caching
bert_model = None
spacy_model = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Pre-load ML models at startup to avoid first-request delay"""
    global bert_model, spacy_model

    print("[*] Loading BERT model...")
    bert_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    print("[+] BERT model loaded successfully")

    print("[*] Loading spaCy NER model...")
    try:
        from app.ner_extractor import get_ner_model
        spacy_model = get_ner_model()
        print("[+] spaCy NER model loaded successfully")
    except Exception as e:
        print(f"[!] Warning: spaCy NER model failed to load: {e}")
        print("[!] NER features will be disabled. Please install: pip install spacy")
        print("[!] Then download the model: python -m spacy download en_core_web_lg")
        spacy_model = None

    yield

    print("[*] Shutting down...")


app = FastAPI(
    title="ResuMatch API",
    description="Resume analysis API with BERT + TF-IDF scoring and skills comparison",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


def _build_enhanced_skills_comparison(resume_skills_dict, job_skills_dict, basic_comparison):
    """Build skills comparison maintaining simple string arrays for frontend compatibility."""
    return basic_comparison


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "bert_loaded": bert_model is not None,
    }


@app.post("/api/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...),
):
    """
    Analyze resume against job description.
    Returns scores and skills comparison.
    """
    if not file.filename.endswith((".pdf", ".docx")):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")

    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size must be less than 10MB")

    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(content)
        temp_path = tmp.name

    try:
        print(f"[*] Extracting text from {file.filename}...")
        resume_text = extract_text(temp_path)

        if not resume_text or len(resume_text.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Could not extract sufficient text from resume. Please ensure it's a valid PDF/DOCX file.",
            )

        print(f"[+] Extracted {len(resume_text)} characters")

        print("[*] Calculating scores...")
        score_data = composite_score(resume_text, job_description)
        print(f"[+] Composite Score: {score_data['composite_score']}/100")

        print("[*] Extracting skills (hybrid NER + regex)...")
        resume_skills_hybrid = extract_skills_hybrid(resume_text)
        job_skills_hybrid = extract_skills_hybrid(job_description)

        print("[*] Comparing skills...")
        skills_comp = compare_skills_from_text(resume_text, job_description)
        print(f"[+] Found {skills_comp['matching_count']} matching skills, {skills_comp['missing_count']} missing")

        skills_comp_enhanced = _build_enhanced_skills_comparison(
            resume_skills_hybrid, job_skills_hybrid, skills_comp
        )

        return {
            "success": True,
            "data": {
                "composite_score": score_data,
                "skills_comparison": skills_comp_enhanced,
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"[!] Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print("ResuMatch API Server")
    print("=" * 60)
    print("API Documentation: http://localhost:8000/docs")
    print("Health Check: http://localhost:8000/api/health")
    print("=" * 60)

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
