import re
from typing import Dict, Set, List, Optional
from app.skills_database import SKILLS_DATABASE, SKILL_ALIASES, normalize_skill, get_skill_category
from app.models import SkillEntity


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


def extract_skills_hybrid(text: str) -> Dict[str, List[SkillEntity]]:
    try:
        from app.ner_extractor import extract_skills_ner
    except ImportError:
        return extract_skills_regex_as_entities(text)
    try:
        ner_skills = extract_skills_ner(text)
    except Exception as e:
        print(f"[!] NER extraction failed: {e}. Falling back to regex.")
        ner_skills = []
    regex_skills = extract_skills_regex_as_entities(text)
    merged = _merge_skill_results(ner_skills, regex_skills)
    organized = {}
    for skill in merged:
        if skill.category not in organized:
            organized[skill.category] = []
        organized[skill.category].append(skill)
    for category in organized:
        organized[category].sort(key=lambda x: x.confidence, reverse=True)

    return organized


def extract_skills_regex_as_entities(text: str) -> List[SkillEntity]:
    if not text:
        return []

    text_lower = text.lower()
    entities = []
    found_skills = set()

    for category, skills in SKILLS_DATABASE.items():
        for skill in skills:
            if len(skill) <= 1 or skill in found_skills:
                continue
            pattern = r'\b' + re.escape(skill) + r'\b'
            match = re.search(pattern, text_lower)
            if match:
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end].strip()
                years = _extract_years_from_context(context)
                proficiency = _detect_proficiency_from_context(context)
                seniority = _infer_seniority_level(years, proficiency)
                entity = SkillEntity(
                    skill_name=skill,
                    category=category,
                    confidence=0.95,  
                    proficiency=proficiency,
                    years_experience=years,
                    seniority_level=seniority,
                    source_section="unknown",
                    context=context,
                    extraction_method="regex"
                )
                entities.append(entity)
                found_skills.add(skill)
                continue
            plural_pattern = r'\b' + re.escape(skill) + r's\b'
            match = re.search(plural_pattern, text_lower)
            if match:
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end].strip()

                years = _extract_years_from_context(context)
                proficiency = _detect_proficiency_from_context(context)
                seniority = _infer_seniority_level(years, proficiency)

                entity = SkillEntity(
                    skill_name=skill,
                    category=category,
                    confidence=0.92,  
                    proficiency=proficiency,
                    years_experience=years,
                    seniority_level=seniority,
                    source_section="unknown",
                    context=context,
                    extraction_method="regex"
                )
                entities.append(entity)
                found_skills.add(skill)

    return entities


def _extract_years_from_context(context: str):
    patterns = [
        r'(\d+(?:\.\d+)?)\s*(?:\+)?\s*years?(?:\s+of|\s+in|\s+experience)?',
        r'for\s+(\d+(?:\.\d+)?)\s*(?:\+)?\s*years?',
        r'(\d+(?:\.\d+)?)\s*(?:\+)?\s*years?\s+(?:of|in)',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, context, re.IGNORECASE)
        if matches:
            try:
                return float(matches[0])
            except (ValueError, IndexError):
                continue

    return None


def _detect_proficiency_from_context(context: str) -> str:
    context_lower = context.lower()
    expert_keywords = [
        'expert', 'lead', 'architect', 'master', 'proficient with',
        'extensive', 'proven expertise', 'deep knowledge'
    ]
    for keyword in expert_keywords:
        if keyword in context_lower:
            return "expert"
    intermediate_keywords = [
        'experienced', 'worked with', 'skilled in', 'proficient',
        'comfortable with', 'solid', 'strong'
    ]
    for keyword in intermediate_keywords:
        if keyword in context_lower:
            return "intermediate"
    beginner_keywords = [
        'learning', 'familiar with', 'basic', 'introduced to',
        'exploring', 'beginner', 'novice'
    ]
    for keyword in beginner_keywords:
        if keyword in context_lower:
            return "beginner"
    if re.search(r'\d+\s*(?:\+)?\s*years?', context_lower):
        return "intermediate"

    return "beginner"


def _infer_seniority_level(years: Optional[float], proficiency: str) -> str:
    if years is not None:
        if years < 1:
            return "junior"
        elif years <= 3:
            return "mid"
        else:
            return "senior"

    if proficiency == "expert":
        return "senior"
    elif proficiency == "intermediate":
        return "mid"
    else:
        return "junior"


def _merge_skill_results(ner_skills: List[SkillEntity],
                        regex_skills: List[SkillEntity]) -> List[SkillEntity]:
    merged = {}  
    for skill in regex_skills:
        normalized = normalize_skill(skill.skill_name)
        if normalized not in merged:
            merged[normalized] = skill
    for skill in ner_skills:
        normalized = normalize_skill(skill.skill_name)
        if normalized in merged:
            if skill.confidence > merged[normalized].confidence:
                merged[normalized] = skill
            else:
                existing = merged[normalized]
                if skill.years_experience is not None and existing.years_experience is None:
                    existing.years_experience = skill.years_experience
                if skill.proficiency != "beginner" and existing.proficiency == "intermediate":
                    existing.proficiency = skill.proficiency
                if skill.seniority_level != "mid" and existing.seniority_level == "mid":
                    existing.seniority_level = skill.seniority_level
        else:
            merged[normalized] = skill

    return list(merged.values())
