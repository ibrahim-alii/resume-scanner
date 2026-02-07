import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import type { CompositeScore, SkillsComparison } from '../types/api';

interface AnalysisData {
  composite_score: CompositeScore;
  skills_comparison: SkillsComparison;
  gemini_feedback: string;
}

export const AnalysisPage: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const analysisData = location.state?.analysisData as AnalysisData | undefined;
  const resumeFileName = location.state?.resumeFileName as string | undefined;

  // Redirect if no data
  React.useEffect(() => {
    if (!analysisData) {
      navigate('/');
    }
  }, [analysisData, navigate]);

  if (!analysisData) return null;

  const { composite_score, skills_comparison, gemini_feedback } = analysisData;

  return (
    <div className="min-h-screen bg-cream p-8">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
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

        {/* Composite Score */}
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

        {/* Skills Comparison */}
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

            {/* Stats */}
            <div className="mb-6 p-4 bg-peach rounded-retro">
              <div className="font-retro text-text text-lg">
                <strong>Match Rate:</strong> {Math.round(skills_comparison.match_percentage)}%
                ({skills_comparison.matching_count} of {skills_comparison.total_job_skills} required skills)
              </div>
            </div>

            {/* Matching Skills */}
            {skills_comparison.matching.length > 0 && (
              <div className="mb-4">
                <h3 className="font-retro text-xl text-green-700 font-bold mb-2">
                  ✓ Matching Skills ({skills_comparison.matching.length})
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

            {/* Missing Skills */}
            {skills_comparison.missing.length > 0 && (
              <div className="mb-4">
                <h3 className="font-retro text-xl text-red-700 font-bold mb-2">
                  ✗ Missing Skills ({skills_comparison.missing.length})
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

            {/* Additional Skills */}
            {skills_comparison.additional.length > 0 && (
              <div>
                <h3 className="font-retro text-xl text-blue-700 font-bold mb-2">
                  + Additional Skills ({skills_comparison.additional.length})
                </h3>
                <div className="flex flex-wrap gap-2">
                  {skills_comparison.additional.slice(0, 10).map((skill, idx) => (
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
                  {skills_comparison.additional.length > 10 && (
                    <span className="font-retro text-text text-sm self-center">
                      +{skills_comparison.additional.length - 10} more
                    </span>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Gemini Feedback */}
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
            <h2 className="font-retro text-2xl mb-4 text-text font-bold flex items-center gap-2">
              <span>🤖</span> AI Suggestions
            </h2>
            <div className="font-retro text-text whitespace-pre-line">
              {gemini_feedback}
            </div>
          </div>
        </div>

        {/* Action Buttons */}
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
