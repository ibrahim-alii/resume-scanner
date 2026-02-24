import re
from typing import List, Optional, Dict
from app.models import SkillEntity
from app.skills_database import get_skill_category, get_all_skills, normalize_skill

try:
    import spacy
    from spacy.matcher import PhraseMatcher, Matcher
except ImportError:
    spacy = None
    PhraseMatcher = None
    Matcher = None


class SkillNER:
    def __init__(self):
        self.model = None
        self.phrase_matcher = None
        self.matcher = None
        self.all_skills = get_all_skills()
        self.load_model()

    def load_model(self):
        if spacy is None:
            raise ImportError(
                "spacy is not installed. Install it with: "
                "pip install spacy && python -m spacy download en_core_web_lg"
            )

        try:
            self.model = spacy.load("en_core_web_lg")
            self.phrase_matcher = PhraseMatcher(self.model.vocab)
            self.matcher = Matcher(self.model.vocab)
            for skill in self.all_skills:
                pattern = self.model.make_doc(skill)
                self.phrase_matcher.add("SKILL", [pattern])
            self._add_regex_patterns()

        except OSError:
            raise OSError(
                "spaCy model 'en_core_web_lg' not found. "
                "Download it with: python -m spacy download en_core_web_lg"
            )

    def _add_regex_patterns(self):
        year_pattern = [
            {"LOWER": {"REGEX": r"^\d+(\.\d+)?(\+)?$"}},  
            {"LOWER": {"REGEX": r"^years?$"}},             
            {"LOWER": {"REGEX": r"^(of|in)?$"}, "OP": "?"},  
            {"ENT_TYPE": "SKILL", "OP": "+"}               
        ]

    def extract_skills_ner(self, text: str) -> List[SkillEntity]:
        if self.model is None:
            return []

        doc = self.model(text)
        skills = []
        seen_skills = set()
        matches = self.phrase_matcher(doc)

        for match_id, start, end in matches:
            span = doc[start:end]
            skill_text = span.text.lower()

            if skill_text in seen_skills:
                continue
            context_start = max(0, span.start_char - 50)
            context_end = min(len(text), span.end_char + 50)
            context = text[context_start:context_end].strip()
            proficiency = self._detect_proficiency(context)
            years = self._extract_years_experience(context)
            seniority = self._infer_seniority(years, proficiency)
            normalized = normalize_skill(skill_text)
            category = get_skill_category(normalized) or "other"
            section = self._detect_section(doc, span)
            confidence = self._calculate_confidence("exact_match", 1.0, years, proficiency)

            skill = SkillEntity(
                skill_name=skill_text,
                category=category,
                confidence=confidence,
                proficiency=proficiency,
                years_experience=years,
                seniority_level=seniority,
                source_section=section,
                context=context,
                extraction_method="ner"
            )

            skills.append(skill)
            seen_skills.add(skill_text)

        return skills

    def _detect_proficiency(self, context: str) -> str:
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

    def _extract_years_experience(self, context: str) -> Optional[float]:
        patterns = [
            r'(\d+(?:\.\d+)?)\s*(?:\+)?\s*years?(?:\s+of|\s+in|\s+experience)?',
            r'for\s+(\d+(?:\.\d+)?)\s*(?:\+)?\s*years?',
            r'(\d+(?:\.\d+)?)\s*(?:\+)?\s*years?\s+(?:of|in)',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, context, re.IGNORECASE)
            if matches:
                try:
                    value = float(matches[0])
                    return value
                except (ValueError, IndexError):
                    continue

        return None

    def _infer_seniority(self, years: Optional[float], proficiency: str) -> str:
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

    def _detect_section(self, doc, span) -> str:
        text_before = doc[:span.start].text.lower()

        if "experience" in text_before or "work" in text_before:
            return "experience"
        elif "education" in text_before or "degree" in text_before or "school" in text_before:
            return "education"
        elif "skill" in text_before or "technical" in text_before:
            return "skills"
        elif "project" in text_before or "portfolio" in text_before:
            return "projects"
        else:
            return "other"

    def _calculate_confidence(self, match_type: str, match_quality: float,
                             years: Optional[float], proficiency: str) -> float:
        base_confidence = 0.85  
        confidence = base_confidence * match_quality
        if years is not None:
            confidence = min(0.95, confidence + 0.05)
        if proficiency in ["expert", "intermediate"]:
            confidence = min(0.95, confidence + 0.02)

        return round(confidence, 2)
_ner_instance = None


def get_ner_model() -> SkillNER:
    global _ner_instance
    if _ner_instance is None:
        _ner_instance = SkillNER()
    return _ner_instance


def extract_skills_ner(text: str) -> List[SkillEntity]:
    ner = get_ner_model()
    return ner.extract_skills_ner(text)
