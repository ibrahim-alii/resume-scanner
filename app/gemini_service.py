"""
Gemini API integration for AI-powered resume suggestions.
"""
import os
import json
from google import genai
from google.genai import types
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

# Load .env for direct module usage too (api.py also loads this at startup)
load_dotenv(override=True)

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
if GEMINI_MODEL.startswith("models/"):
    GEMINI_MODEL = GEMINI_MODEL[len("models/"):]

# Initialize client if API key is available
client = None
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)


def generate_ai_suggestions(
    resume_text: str,
    job_description: str,
    missing_skills: List[str],
    matching_skills: List[str]
) -> Optional[Dict[str, Any]]:
    """
    Generate AI-powered resume improvement suggestions using Gemini.

    Args:
        resume_text: The candidate's resume text (will be truncated to 4000 chars)
        job_description: The target job description (will be truncated to 2000 chars)
        missing_skills: List of skills from JD not found in resume
        matching_skills: List of skills found in both resume and JD

    Returns:
        Dictionary with 5 categories of suggestions, or None if API fails
    """

    # Skip if no API key configured
    if not GEMINI_API_KEY or not client:
        print("[!] GEMINI_API_KEY not configured, skipping AI suggestions")
        return None

    try:
        # Truncate inputs to prevent token overflow
        resume_truncated = resume_text[:4000]
        jd_truncated = job_description[:2000]
        missing_top = missing_skills[:15]  # Top 15 missing skills
        matching_top = matching_skills[:20]  # Top 20 matching skills

        # Build the prompt
        prompt = f"""You are an expert resume coach with 15+ years of experience helping candidates optimize their resumes for Applicant Tracking Systems (ATS) and human recruiters.

**YOUR TASK:** Analyze the resume against the job description and provide specific, actionable improvement suggestions in 5 categories.

**IMPORTANT INSTRUCTIONS:**
- Base ALL suggestions on actual content in the resume and job description provided below
- Be specific and actionable - quote actual text from the resume when suggesting improvements
- Prioritize high-impact changes that will improve ATS matching and recruiter appeal
- Do NOT provide generic advice - every suggestion must be grounded in the actual documents

---

**RESUME TEXT:**
{resume_truncated}

---

**JOB DESCRIPTION:**
{jd_truncated}

---

**SKILLS ANALYSIS:**
- **Missing Skills (not in resume):** {', '.join(missing_top) if missing_top else 'None'}
- **Matching Skills (found in resume):** {', '.join(matching_top) if matching_top else 'None'}

---

**PROVIDE SUGGESTIONS IN THESE 5 CATEGORIES:**

1. **Skill Gaps (Priority: High)** - Top 3-5 missing skills that are critical for this role
   - For each skill: explain WHY it matters and HOW to acquire/demonstrate it
   - Prioritize as "critical", "high", or "medium" based on job requirements

2. **Quantification Opportunities (Priority: High)** - 3-5 bullet points lacking metrics
   - Find bullets in the resume that describe accomplishments but lack numbers (%, $, time, size)
   - Suggest specific metrics to add based on the context
   - Provide a rewritten version with quantification

3. **ATS Optimization (Priority: Medium)** - Keywords from job description to incorporate
   - Identify 5-7 important keywords/phrases from the JD that are missing or underused
   - Rate importance as "high", "medium", or "low"
   - Suggest where and how to naturally incorporate them

4. **Impact Statements (Priority: Medium)** - 2-3 weak bullets to strengthen
   - Find task-oriented or passive bullets in the resume
   - Rewrite using CAR framework (Challenge-Action-Result) with strong action verbs
   - Explain what makes the original weak

5. **Strategic Recommendations (Priority: Low)** - 2-3 high-level positioning tips
   - Overall resume structure, formatting, or positioning advice
   - Categorize as "positioning", "structure", "format", or "other"
   - Rate impact as "high", "medium", or "low"

---

**OUTPUT FORMAT:** Return ONLY valid JSON matching this exact schema:

{{
  "skill_gaps": [
    {{
      "skill": "Kubernetes",
      "priority": "critical",
      "explanation": "The JD explicitly requires container orchestration experience for managing microservices infrastructure",
      "suggestion": "Consider completing a Kubernetes certification (CKA) or add a personal project deploying a containerized app to your resume"
    }}
  ],
  "quantification_opportunities": [
    {{
      "original_text": "Managed team and improved processes",
      "issue": "Lacks team size and improvement metrics",
      "suggested_rewrite": "Managed team of 8 engineers, reducing deployment time by 40% through process automation",
      "metrics_to_consider": ["team size", "time reduction %", "efficiency gain"]
    }}
  ],
  "ats_optimization": [
    {{
      "keyword": "CI/CD",
      "importance": "high",
      "current_usage": "missing",
      "suggestion": "Add 'CI/CD pipeline' to your DevOps experience section when describing automated testing implementation"
    }}
  ],
  "impact_statements": [
    {{
      "original_text": "Responsible for database optimization",
      "weakness": "Task-oriented, passive voice, no measurable outcome",
      "suggested_rewrite": "Optimized PostgreSQL database queries, reducing average page load time from 3s to 0.5s (83% improvement)",
      "action_verb_used": "Optimized"
    }}
  ],
  "strategic_recommendations": [
    {{
      "category": "structure",
      "recommendation": "Move your Technical Skills section above Work Experience to immediately highlight your Python, AWS, and Docker expertise",
      "impact": "high"
    }}
  ]
}}

**RETURN ONLY THE JSON - NO OTHER TEXT.**
"""

        # Generate suggestions using new API
        print(f"[*] Calling Gemini API ({GEMINI_MODEL})...")

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3,  # Lower temperature for focused, consistent output
                top_p=0.95,
                top_k=40,
                max_output_tokens=8192,
                response_mime_type="application/json",  # Force JSON output
            )
        )

        # Parse JSON response
        suggestions = json.loads(response.text)

        print(f"[+] AI suggestions generated successfully")
        return suggestions

    except json.JSONDecodeError as e:
        print(f"[!] Failed to parse Gemini JSON response: {e}")
        print(f"[!] Raw response: {response.text[:500]}")
        raise RuntimeError("Gemini returned invalid JSON response") from e

    except Exception as e:
        print(f"[!] Error generating AI suggestions: {e}")
        raise RuntimeError(f"Gemini request failed: {e}") from e
