export interface CompositeScore {
  composite_score: number;
  bert_score: number;
  tfidf_score: number;
  breakdown: {
    bert: string;
    tfidf: string;
  };
}

export interface SkillsComparison {
  matching: string[];
  missing: string[];
  additional: string[];
  match_percentage: number;
  total_job_skills: number;
  total_resume_skills: number;
  matching_count: number;
  missing_count: number;
  additional_count: number;
}

export interface AnalysisResponse {
  success: boolean;
  data: {
    composite_score: CompositeScore;
    skills_comparison: SkillsComparison;
    gemini_feedback: string;
  };
}
