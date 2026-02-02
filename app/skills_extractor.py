import re
from typing import Dict, Set, List
from app.skills_database import SKILLS_DATABASE, SKILL_ALIASES, normalize_skill


def extract_skills(text: str) -> Dict[str, List[str]]:
    """
    Extract technical skills from resume or job description text.
    
    Args:
        text: The text to extract skills from (resume or job description)
    
    Returns:
        Dictionary with skill categories as keys and lists of found skills as values
        Example: {
            'programming_languages': ['python', 'javascript'],
            'cloud_platforms': ['aws', 'gcp']
        }
    """
    if not text:
        return {category: [] for category in SKILLS_DATABASE.keys()}
    
    # Convert to lowercase for matching
    text_lower = text.lower()
    
    # Dictionary to store found skills by category
    found_skills = {category: [] for category in SKILLS_DATABASE.keys()}
    
    # Track skills we've already found to avoid duplicates
    found_skills_set = set()
    
    # Iterate through each category
    for category, skills in SKILLS_DATABASE.items():
        for skill in skills:
            # Skip single-letter skills to avoid false positives
            if len(skill) <= 1:
                continue
            
            # Skip if we've already found this skill
            if skill in found_skills_set:
                continue
            
            # Use word boundaries to match whole words only
            # Escape special regex characters in the skill name
            pattern = r'\b' + re.escape(skill) + r'\b'
            
            if re.search(pattern, text_lower):
                found_skills[category].append(skill)
                found_skills_set.add(skill)
                continue
            
            # Also try with 's' suffix for plurals (framework -> frameworks)
            plural_pattern = r'\b' + re.escape(skill) + r's\b'
            if re.search(plural_pattern, text_lower):
                found_skills[category].append(skill)
                found_skills_set.add(skill)
    
    # Remove empty categories for cleaner output
    result = {category: skills for category, skills in found_skills.items() if skills}
    
    return result


def extract_skills_as_set(text: str) -> Set[str]:
    """
    Extract technical skills as a flat set (no category organization).
    Useful for set operations (intersection, difference, etc.).
    
    Args:
        text: The text to extract skills from
    
    Returns:
        Set of found skills (lowercase)
        Example: {'python', 'javascript', 'aws', 'gcp'}
    """
    skills_dict = extract_skills(text)
    all_skills = set()
    for skills_list in skills_dict.values():
        all_skills.update(skills_list)
    return all_skills
