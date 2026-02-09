from dataclasses import dataclass
from typing import Optional


@dataclass
class SkillEntity:
    """Represents an extracted skill with metadata"""
    skill_name: str                    # e.g., "Python", "React"
    category: str                      # e.g., "programming_languages"
    confidence: float                  # 0.0-1.0 (from NER or regex)
    proficiency: str                   # "beginner", "intermediate", "expert"
    years_experience: Optional[float]  # e.g., 5.0 for "5 years"
    seniority_level: str               # "junior", "mid", "senior"
    source_section: str                # "experience", "education", "skills", etc.
    context: str                       # The sentence/phrase it appeared in
    extraction_method: str             # "ner" or "regex"

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'skill': self.skill_name,
            'category': self.category,
            'confidence': round(self.confidence, 2),
            'proficiency': self.proficiency,
            'years_experience': self.years_experience,
            'seniority_level': self.seniority_level,
            'source_section': self.source_section,
            'context': self.context[:100],  # Truncate context for response
            'method': self.extraction_method
        }
