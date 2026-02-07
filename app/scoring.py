import re
import numpy as np
from typing import Dict, Set, List
from app.skills_extractor import extract_skills_as_set, extract_skills

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    TfidfVectorizer = None
    cosine_similarity = None

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None


def compare_skills(resume_skills: Set[str], job_skills: Set[str]) -> Dict:
    matching = resume_skills & job_skills 
    missing = job_skills - resume_skills  
    additional = resume_skills - job_skills 
    
    if len(job_skills) > 0:
        match_percentage = (len(matching) / len(job_skills)) * 100
    else:
        match_percentage = 0.0
    
    return {
        'matching': sorted(list(matching)),
        'missing': sorted(list(missing)),
        'additional': sorted(list(additional)),
        'match_percentage': round(match_percentage, 2),
        'total_job_skills': len(job_skills),
        'total_resume_skills': len(resume_skills),
        'matching_count': len(matching),
        'missing_count': len(missing),
        'additional_count': len(additional)
    }


def compare_skills_from_text(resume_text: str, job_text: str) -> Dict:
    resume_skills = extract_skills_as_set(resume_text)
    job_skills = extract_skills_as_set(job_text)
    
    return compare_skills(resume_skills, job_skills)


def get_skills_by_category(resume_text: str, job_text: str) -> Dict:
    resume_skills_dict = extract_skills(resume_text)
    job_skills_dict = extract_skills(job_text)
    
    all_categories = set(resume_skills_dict.keys()) | set(job_skills_dict.keys())
    
    result = {}
    for category in sorted(all_categories):
        resume_set = set(resume_skills_dict.get(category, []))
        job_set = set(job_skills_dict.get(category, []))
        
        result[category] = {
            'resume_skills': sorted(list(resume_set)),
            'job_skills': sorted(list(job_set)),
            'matching': sorted(list(resume_set & job_set)),
            'missing': sorted(list(job_set - resume_set))
        }
    
    return result


def tfidf_similarity(resume_text: str, job_description: str) -> float:
    if TfidfVectorizer is None or cosine_similarity is None:
        raise ImportError("scikit-learn is not installed. Install it with: pip install scikit-learn")
    
    try:
        # Create TF-IDF vectors
        vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)  # Single words and two-word phrases
        )
        
        # Fit and transform both documents
        vectors = vectorizer.fit_transform([resume_text, job_description])
        
        # Calculate cosine similarity between resume and job description
        similarity_matrix = cosine_similarity(vectors[0:1], vectors[1:2])
        similarity_score = similarity_matrix[0][0]
        
        # Convert 0-1 to 0-100
        return float(similarity_score * 100)
    
    except Exception as e:
        raise ValueError(f"TF-IDF similarity calculation failed: {str(e)}")


def _extract_sections(text: str) -> list:
    # Common section headers
    section_patterns = [
        r'(?:experience|work experience|professional experience)(.*?)(?:(?:education|skills|projects|certifications)|$)',
        r'(?:skills|technical skills)(.*?)(?:(?:experience|education|projects|certifications)|$)',
        r'(?:education|academic)(.*?)(?:(?:experience|skills|projects|certifications)|$)',
        r'(?:projects|portfolio)(.*?)(?:(?:experience|skills|education|certifications)|$)',
    ]
    
    sections = []
    
    for pattern in section_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
        for match in matches:
            section_text = match.group(1).strip()
            if section_text:
                sections.append(section_text)
    
    # If no sections found, split into chunks
    if not sections:
        chunk_size = 500
        words = text.split()
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk.strip():
                sections.append(chunk)
    
    return sections if sections else [text]


def bert_similarity(resume_text: str, job_description: str) -> float:
    if SentenceTransformer is None:
        raise ImportError(
            "sentence-transformers is not installed. "
            "Install it with: pip install sentence-transformers torch"
        )
    
    try:
        # Load pre-trained BERT model (MiniLM - fast and balanced)
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        
        # Embed job description (single vector)
        job_embedding = model.encode(job_description, convert_to_numpy=True)
        
        # Extract resume sections and embed each
        resume_sections = _extract_sections(resume_text)
        section_embeddings = [
            model.encode(section, convert_to_numpy=True)
            for section in resume_sections
        ]
        
        # Calculate similarity for each section
        section_similarities = []
        for section_embedding in section_embeddings:
            # Reshape for cosine_similarity
            section_embedding = section_embedding.reshape(1, -1)
            job_embedding_reshaped = job_embedding.reshape(1, -1)
            
            similarity = cosine_similarity(section_embedding, job_embedding_reshaped)[0][0]
            section_similarities.append(float(similarity))
        
        # Average similarity across sections
        avg_similarity = np.mean(section_similarities) if section_similarities else 0.0
        
        # Convert 0-1 to 0-100
        return float(avg_similarity * 100)
    
    except Exception as e:
        raise ValueError(f"BERT similarity calculation failed: {str(e)}")


def composite_score(
    resume_text: str,
    job_description: str,
    bert_weight: float = 0.8,
    tfidf_weight: float = 0.2
) -> dict:

    try:
        # Calculate both scores
        bert_score = bert_similarity(resume_text, job_description)
        tfidf_score = tfidf_similarity(resume_text, job_description)
        
        # Combine with weights
        composite = (bert_score * bert_weight) + (tfidf_score * tfidf_weight)
        
        return {
            'composite_score': round(composite, 2),
            'bert_score': round(bert_score, 2),
            'tfidf_score': round(tfidf_score, 2),
            'breakdown': {
                'bert': f"{bert_weight * 100:.0f}%",
                'tfidf': f"{tfidf_weight * 100:.0f}%"
            }
        }
    
    except Exception as e:
        raise ValueError(f"Composite score calculation failed: {str(e)}")
        