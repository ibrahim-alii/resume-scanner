import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import type {
  CompositeScore,
  SkillsComparison,
  AiSuggestions,
  SkillGap,
  QuantificationOpportunity,
  AtsOptimization,
  ImpactStatement,
  StrategicRecommendation
} from '../types/api';
import { SuggestionSection } from './SuggestionSection';

interface AnalysisData {
  composite_score: CompositeScore;
  skills_comparison: SkillsComparison;
  ai_suggestions?: AiSuggestions;
  ai_suggestions_error?: string;
}

export const AnalysisPage: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [showAllAdditionalSkills, setShowAllAdditionalSkills] = React.useState(false);

  const analysisData = location.state?.analysisData as AnalysisData | undefined;
  const resumeFileName = location.state?.resumeFileName as string | undefined;

  React.useEffect(() => {
    if (!analysisData) {
      navigate('/');
    }
  }, [analysisData, navigate]);

  if (!analysisData) return null;

  const { composite_score, skills_comparison } = analysisData;
  const additionalSkills = showAllAdditionalSkills
    ? skills_comparison.additional
    : skills_comparison.additional.slice(0, 10);
  const hiddenAdditionalCount = Math.max(skills_comparison.additional.length - 10, 0);

  return (
    <div className="min-h-screen bg-cream p-8">
      <div className="max-w-5xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="font-retro text-5xl mb-2 text-text font-bold">
            Analysis Results
          </h1>
          {resumeFileName && (
            <p className="font-retro text-text">
              Resume: <span className="font-bold">{resumeFileName}</span>
            </p>
          )}
        </div>

        <div className="mb-8">
          <div
            className="
              bg-peach
              border-4
              border-text
              rounded-box
              p-8
              shadow-[6px_6px_0px_0px_rgba(0,0,0,1)]
            "
          >
            <h2 className="font-retro text-3xl mb-4 text-text font-bold text-center">
              Match Score
            </h2>
            <div className="text-center">
              <div className="text-8xl font-retro font-bold text-text mb-4">
                {Math.round(composite_score.composite_score)}
                <span className="text-4xl">/100</span>
              </div>
              <div className="flex justify-center gap-8 font-retro text-text">
                <div>
                  <div className="text-sm">BERT (Semantic)</div>
                  <div className="text-2xl font-bold">
                    {Math.round(composite_score.bert_score)}
                  </div>
                </div>
                <div>
                  <div className="text-sm">TF-IDF (Keywords)</div>
                  <div className="text-2xl font-bold">
                    {Math.round(composite_score.tfidf_score)}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="mb-8">
          <div
            className="
              bg-white
              border-4
              border-text
              rounded-box
              p-6
              shadow-[6px_6px_0px_0px_rgba(0,0,0,1)]
            "
          >
            <h2 className="font-retro text-2xl mb-4 text-text font-bold">
              Skills Analysis
            </h2>

            <div className="mb-6 p-4 bg-peach rounded-retro">
              <div className="font-retro text-text text-lg">
                <strong>Match Rate:</strong> {Math.round(skills_comparison.match_percentage)}%
                ({skills_comparison.matching_count} of {skills_comparison.total_job_skills} required skills)
              </div>
            </div>

            {skills_comparison.matching.length > 0 && (
              <div className="mb-4">
                <h3 className="font-retro text-xl text-green-700 font-bold mb-2">
                  Matching Skills ({skills_comparison.matching.length})
                </h3>
                <div className="flex flex-wrap gap-2">
                  {skills_comparison.matching.map((skill, idx) => (
                    <span
                      key={idx}
                      className="
                        bg-green-100
                        border-2
                        border-green-600
                        text-green-800
                        px-3
                        py-1
                        rounded-retro
                        font-retro
                        text-sm
                      "
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {skills_comparison.missing.length > 0 && (
              <div className="mb-4">
                <h3 className="font-retro text-xl text-red-700 font-bold mb-2">
                  Missing Skills ({skills_comparison.missing.length})
                </h3>
                <div className="flex flex-wrap gap-2">
                  {skills_comparison.missing.map((skill, idx) => (
                    <span
                      key={idx}
                      className="
                        bg-red-100
                        border-2
                        border-red-600
                        text-red-800
                        px-3
                        py-1
                        rounded-retro
                        font-retro
                        text-sm
                      "
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {skills_comparison.additional.length > 0 && (
              <div>
                <h3 className="font-retro text-xl text-blue-700 font-bold mb-2">
                  + Additional Skills ({skills_comparison.additional.length})
                </h3>
                <div className="flex flex-wrap gap-2">
                  {additionalSkills.map((skill, idx) => (
                    <span
                      key={idx}
                      className="
                        bg-blue-100
                        border-2
                        border-blue-600
                        text-blue-800
                        px-3
                        py-1
                        rounded-retro
                        font-retro
                        text-sm
                      "
                    >
                      {skill}
                    </span>
                  ))}
                </div>
                {skills_comparison.additional.length > 10 && (
                  <button
                    className="
                      mt-3
                      bg-peach
                      text-text
                      px-4
                      py-2
                      rounded-retro
                      font-retro
                      text-sm
                      shadow-[3px_3px_0px_0px_rgba(0,0,0,1)]
                      hover:translate-x-[1px]
                      hover:translate-y-[1px]
                      hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]
                      transition-all
                    "
                    onClick={() => setShowAllAdditionalSkills((prev) => !prev)}
                  >
                    {showAllAdditionalSkills ? 'Show less' : `Show ${hiddenAdditionalCount} more`}
                  </button>
                )}
              </div>
            )}
          </div>
        </div>

        
        {analysisData.ai_suggestions && (
          <div className="mb-8">
            <div className="bg-white border-4 border-text rounded-box p-6 shadow-[6px_6px_0px_0px_rgba(0,0,0,1)]">
              <h2 className="font-retro text-3xl mb-6 text-text font-bold flex items-center gap-3">
                <span className="text-4xl">🤖</span>
                AI-Powered Resume Coach
              </h2>

              
              <SuggestionSection<SkillGap>
                title="Critical Skill Gaps"
                colorClass="bg-red-600"
                items={analysisData.ai_suggestions.skill_gaps}
                renderItem={(gap) => (
                  <div>
                    <div className="flex items-start justify-between mb-2">
                      <h4 className="font-retro text-lg font-bold text-text">{gap.skill}</h4>
                      <span
                        className={`px-3 py-1 rounded-full text-xs font-bold ${
                          gap.priority === 'critical'
                            ? 'bg-red-200 text-red-900'
                            : gap.priority === 'high'
                            ? 'bg-orange-200 text-orange-900'
                            : 'bg-yellow-200 text-yellow-900'
                        }`}
                      >
                        {gap.priority.toUpperCase()}
                      </span>
                    </div>
                    <p className="text-gray-700 mb-2">
                      <strong>Why it matters:</strong> {gap.explanation}
                    </p>
                    <p className="text-gray-700">
                      <strong>How to improve:</strong> {gap.suggestion}
                    </p>
                  </div>
                )}
              />

              
              <SuggestionSection<QuantificationOpportunity>
                title="Add Metrics & Numbers"
                colorClass="bg-blue-600"
                items={analysisData.ai_suggestions.quantification_opportunities}
                renderItem={(opp) => (
                  <div>
                    <div className="mb-3">
                      <div className="text-sm font-bold text-red-700 mb-1">❌ Before:</div>
                      <div className="bg-red-50 border-l-4 border-red-500 p-3 rounded">
                        <p className="text-gray-800 italic">"{opp.original_text}"</p>
                        <p className="text-red-600 text-sm mt-1">Issue: {opp.issue}</p>
                      </div>
                    </div>
                    <div className="mb-2">
                      <div className="text-sm font-bold text-green-700 mb-1">✅ After:</div>
                      <div className="bg-green-50 border-l-4 border-green-500 p-3 rounded">
                        <p className="text-gray-800 font-medium">"{opp.suggested_rewrite}"</p>
                      </div>
                    </div>
                    <div className="mt-2">
                      <span className="text-sm text-gray-600">
                        <strong>Metrics to consider:</strong>{' '}
                        {opp.metrics_to_consider.join(', ')}
                      </span>
                    </div>
                  </div>
                )}
              />

              
              <SuggestionSection<AtsOptimization>
                title="ATS Keyword Optimization"
                colorClass="bg-purple-600"
                items={analysisData.ai_suggestions.ats_optimization}
                renderItem={(ats) => (
                  <div>
                    <div className="flex items-start justify-between mb-2">
                      <h4 className="font-retro text-lg font-bold text-text">"{ats.keyword}"</h4>
                      <div className="flex gap-2">
                        <span
                          className={`px-2 py-1 rounded text-xs font-bold ${
                            ats.importance === 'high'
                              ? 'bg-red-200 text-red-900'
                              : ats.importance === 'medium'
                              ? 'bg-yellow-200 text-yellow-900'
                              : 'bg-gray-200 text-gray-900'
                          }`}
                        >
                          {ats.importance.toUpperCase()}
                        </span>
                        <span
                          className={`px-2 py-1 rounded text-xs font-bold ${
                            ats.current_usage === 'missing'
                              ? 'bg-red-100 text-red-800'
                              : ats.current_usage === 'underused'
                              ? 'bg-orange-100 text-orange-800'
                              : 'bg-green-100 text-green-800'
                          }`}
                        >
                          {ats.current_usage}
                        </span>
                      </div>
                    </div>
                    <p className="text-gray-700">{ats.suggestion}</p>
                  </div>
                )}
              />

              
              <SuggestionSection<ImpactStatement>
                title="Strengthen Bullet Points"
                colorClass="bg-green-600"
                items={analysisData.ai_suggestions.impact_statements}
                renderItem={(impact) => (
                  <div>
                    <div className="mb-3">
                      <div className="text-sm font-bold text-red-700 mb-1">❌ Weak:</div>
                      <div className="bg-red-50 border-l-4 border-red-500 p-3 rounded">
                        <p className="text-gray-800 italic">"{impact.original_text}"</p>
                        <p className="text-red-600 text-sm mt-1">Problem: {impact.weakness}</p>
                      </div>
                    </div>
                    <div>
                      <div className="text-sm font-bold text-green-700 mb-1">✅ Strong:</div>
                      <div className="bg-green-50 border-l-4 border-green-500 p-3 rounded">
                        <p className="text-gray-800 font-medium">"{impact.suggested_rewrite}"</p>
                        <p className="text-green-600 text-sm mt-1">
                          Action verb: <strong>{impact.action_verb_used}</strong>
                        </p>
                      </div>
                    </div>
                  </div>
                )}
              />

              
              <SuggestionSection<StrategicRecommendation>
                title="Strategic Recommendations"
                colorClass="bg-teal-600"
                items={analysisData.ai_suggestions.strategic_recommendations}
                renderItem={(rec) => (
                  <div>
                    <div className="flex items-start justify-between mb-2">
                      <span className="px-3 py-1 bg-gray-200 text-gray-800 rounded text-xs font-bold uppercase">
                        {rec.category}
                      </span>
                      <span
                        className={`px-3 py-1 rounded text-xs font-bold ${
                          rec.impact === 'high'
                            ? 'bg-red-200 text-red-900'
                            : rec.impact === 'medium'
                            ? 'bg-yellow-200 text-yellow-900'
                            : 'bg-blue-200 text-blue-900'
                        }`}
                      >
                        {rec.impact.toUpperCase()} IMPACT
                      </span>
                    </div>
                    <p className="text-gray-800 text-base leading-relaxed">{rec.recommendation}</p>
                  </div>
                )}
              />
            </div>
          </div>
        )}

        
        {analysisData.ai_suggestions_error && (
          <div className="mb-8">
            <div className="bg-yellow-50 border-4 border-yellow-500 rounded-box p-6 shadow-[6px_6px_0px_0px_rgba(0,0,0,1)]">
              <div className="flex items-start gap-3">
                <span className="text-3xl">⚠️</span>
                <div>
                  <h3 className="font-retro text-xl font-bold text-yellow-900 mb-2">
                    AI Suggestions Unavailable
                  </h3>
                  <p className="text-yellow-800">
                    {analysisData.ai_suggestions_error}
                  </p>
                  <p className="text-yellow-700 text-sm mt-2">
                    Don't worry - your resume analysis and skills comparison are still complete!
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="flex justify-center gap-4">
          <button
            className="
              bg-peach
              text-text
              px-8
              py-3
              rounded-retro
              font-retro
              text-lg
              shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]
              hover:translate-x-[2px]
              hover:translate-y-[2px]
              hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]
              active:translate-x-[4px]
              active:translate-y-[4px]
              active:shadow-none
              transition-all
            "
            onClick={() => navigate('/')}
          >
            Analyze Another Resume
          </button>
        </div>
      </div>
    </div>
  );
};
