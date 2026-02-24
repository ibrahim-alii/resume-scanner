import os
import tempfile
from contextlib import asynccontextmanager
from typing import Dict, List

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
load_dotenv(override=True)

from app import (
    compare_skills_from_text,
    composite_score,
    extract_text,
    extract_skills_hybrid,
)
from app.scoring import set_bert_model, tfidf_similarity
from app.gemini_service import generate_ai_suggestions
bert_model = None
spacy_model = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global bert_model, spacy_model

    print("[*] Loading BERT model...")
    try:
        bert_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        set_bert_model(bert_model)
        print("[+] BERT model loaded successfully")
    except Exception as e:
        bert_model = None
        print(f"[!] Warning: BERT model failed to load: {e}")
        print("[!] Semantic scoring disabled; TF-IDF fallback will be used.")

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


class SkillGap(BaseModel):
    skill: str
    priority: str
    explanation: str
    suggestion: str


class QuantificationOpportunity(BaseModel):
    original_text: str
    issue: str
    suggested_rewrite: str
    metrics_to_consider: List[str]


class AtsOptimization(BaseModel):
    keyword: str
    importance: str
    current_usage: str
    suggestion: str


class ImpactStatement(BaseModel):
    original_text: str
    weakness: str
    suggested_rewrite: str
    action_verb_used: str


class StrategicRecommendation(BaseModel):
    category: str
    recommendation: str
    impact: str


class AiSuggestions(BaseModel):
    skill_gaps: List[SkillGap]
    quantification_opportunities: List[QuantificationOpportunity]
    ats_optimization: List[AtsOptimization]
    impact_statements: List[ImpactStatement]
    strategic_recommendations: List[StrategicRecommendation]


class AnalysisResponse(BaseModel):
    success: bool
    data: Dict


def _build_enhanced_skills_comparison(resume_skills_dict, job_skills_dict, basic_comparison):
    return basic_comparison


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "bert_loaded": bert_model is not None,
        "scoring_fallback_enabled": True,
    }


@app.post("/api/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...),
):
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
        try:
            score_data = composite_score(resume_text, job_description)
        except Exception as score_error:
            print(f"[!] Composite score failed, falling back to TF-IDF only: {score_error}")
            tfidf_score = tfidf_similarity(resume_text, job_description)
            score_data = {
                "composite_score": round(tfidf_score, 2),
                "bert_score": round(tfidf_score, 2),
                "tfidf_score": round(tfidf_score, 2),
                "breakdown": {"bert": "0%", "tfidf": "100%"},
                "warning": f"Used TF-IDF fallback due to scoring error: {score_error}",
            }
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
        print("[*] Generating AI-powered suggestions with Gemini...")
        ai_suggestions = None
        ai_suggestions_error = None
        try:
            ai_suggestions = generate_ai_suggestions(
                resume_text=resume_text,
                job_description=job_description,
                missing_skills=skills_comp['missing'],
                matching_skills=skills_comp['matching']
            )
            if ai_suggestions:
                print("[+] AI suggestions generated successfully")
            else:
                print("[!] AI suggestions skipped (API not configured or returned None)")
                ai_suggestions_error = (
                    "AI suggestions are currently unavailable. "
                    "Set GEMINI_API_KEY to enable the AI Resume Coach."
                )
        except Exception as e:
            ai_suggestions_error = str(e)
            print(f"[!] AI suggestions failed: {e}")

        response_data = {
            "composite_score": score_data,
            "skills_comparison": skills_comp_enhanced,
        }
        if ai_suggestions:
            response_data["ai_suggestions"] = ai_suggestions
        if ai_suggestions_error:
            response_data["ai_suggestions_error"] = ai_suggestions_error

        return {
            "success": True,
            "data": response_data,
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
    port = int(os.getenv("PORT", "8001"))
    print(f"API Documentation: http://localhost:{port}/docs")
    print(f"Health Check: http://localhost:{port}/api/health")
    print("=" * 60)

    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")