import re
from typing import Dict, Set, List
from app.skills_database import SKILLS_DATABASE, SKILL_ALIASES, normalize_skill


def extract_skills(text: str) -> Dict[str, List[str]]:
    if not text:
        return {category: [] for category in SKILLS_DATABASE.keys()}
    
    text_lower = text.lower()
    
    found_skills = {category: [] for category in SKILLS_DATABASE.keys()}
    
    found_skills_set = set()
    
    for category, skills in SKILLS_DATABASE.items():
        for skill in skills:
            if len(skill) <= 1:
                continue
            
            if skill in found_skills_set:
                continue
            
            pattern = r'\b' + re.escape(skill) + r'\b'
            
            if re.search(pattern, text_lower):
                found_skills[category].append(skill)
                found_skills_set.add(skill)
                continue
            
            plural_pattern = r'\b' + re.escape(skill) + r's\b'
            if re.search(plural_pattern, text_lower):
                found_skills[category].append(skill)
                found_skills_set.add(skill)
    
    result = {category: skills for category, skills in found_skills.items() if skills}
    
    return result


def extract_skills_as_set(text: str) -> Set[str]:
    skills_dict = extract_skills(text)
    all_skills = set()
    for skills_list in skills_dict.values():
        all_skills.update(skills_list)
    return all_skills
