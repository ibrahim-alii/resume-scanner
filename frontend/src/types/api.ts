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

export interface SkillGap {
  skill: string;
  priority: 'critical' | 'high' | 'medium';
  explanation: string;
  suggestion: string;
}

export interface QuantificationOpportunity {
  original_text: string;
  issue: string;
  suggested_rewrite: string;
  metrics_to_consider: string[];
}

export interface AtsOptimization {
  keyword: string;
  importance: 'high' | 'medium' | 'low';
  current_usage: 'missing' | 'underused' | 'present';
  suggestion: string;
}

export interface ImpactStatement {
  original_text: string;
  weakness: string;
  suggested_rewrite: string;
  action_verb_used: string;
}

export interface StrategicRecommendation {
  category: 'positioning' | 'structure' | 'format' | 'other';
  recommendation: string;
  impact: 'high' | 'medium' | 'low';
}

export interface AiSuggestions {
  skill_gaps: SkillGap[];
  quantification_opportunities: QuantificationOpportunity[];
  ats_optimization: AtsOptimization[];
  impact_statements: ImpactStatement[];
  strategic_recommendations: StrategicRecommendation[];
}

export interface AnalysisResponse {
  success: boolean;
  data: {
    composite_score: CompositeScore;
    skills_comparison: SkillsComparison;
    ai_suggestions?: AiSuggestions;
    ai_suggestions_error?: string;
  };
}
