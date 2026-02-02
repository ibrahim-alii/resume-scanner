from typing import Dict, Set, List
from app.skills_extractor import extract_skills_as_set, extract_skills


def compare_skills(resume_skills: Set[str], job_skills: Set[str]) -> Dict:
    """
    Compare resume skills with job description skills using set operations.
    
    Args:
        resume_skills: Set of skills extracted from resume
        job_skills: Set of skills extracted from job description
    
    Returns:
        Dictionary containing:
        - matching: Skills found in both resume and job
        - missing: Skills required by job but not on resume
        - additional: Skills on resume but not required by job
        - match_percentage: Percentage of job skills covered by resume
        - total_job_skills: Total number of skills in job description
        - total_resume_skills: Total number of skills in resume
    """
    # Set operations for skill comparison
    matching = resume_skills & job_skills  # Intersection
    missing = job_skills - resume_skills  # Job skills not on resume
    additional = resume_skills - job_skills  # Resume skills not in job
    
    # Calculate match percentage
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
    """
    Extract skills from both resume and job description, then compare them.
    Convenience function that combines extraction and comparison.
    
    Args:
        resume_text: Text content of resume
        job_text: Text content of job description
    
    Returns:
        Dictionary with comparison results (same as compare_skills output)
    """
    resume_skills = extract_skills_as_set(resume_text)
    job_skills = extract_skills_as_set(job_text)
    
    return compare_skills(resume_skills, job_skills)


def get_skills_by_category(resume_text: str, job_text: str) -> Dict:
    """
    Get skill comparison results organized by category.
    Shows which skills match, are missing, etc., grouped by category.
    
    Args:
        resume_text: Text content of resume
        job_text: Text content of job description
    
    Returns:
        Dictionary where each category contains:
        - resume_skills: Skills from resume in this category
        - job_skills: Skills in job description in this category
        - matching: Skills that match in this category
        - missing: Skills missing from resume in this category
    """
    resume_skills_dict = extract_skills(resume_text)
    job_skills_dict = extract_skills(job_text)
    
    # Get all categories from both
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
