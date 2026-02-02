from typing import Dict, Set, List
from app.skills_extractor import extract_skills_as_set, extract_skills


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
