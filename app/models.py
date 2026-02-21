from dataclasses import dataclass
from typing import Optional


@dataclass
class SkillEntity:
    """Represents an extracted skill with metadata"""
    skill_name: str                    
    category: str                      
    confidence: float                  
    proficiency: str                   
    years_experience: Optional[float]  
    seniority_level: str               
    source_section: str                
    context: str                       
    extraction_method: str             

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
            'context': self.context[:100],  
            'method': self.extraction_method
        }
