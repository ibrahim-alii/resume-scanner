import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { analyzeResume } from '../api/client';

export const JobDescriptionInput: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const resumeFile = location.state?.resumeFile as File | undefined;

  // Redirect if no resume file
  React.useEffect(() => {
    if (!resumeFile) {
      navigate('/');
    }
  }, [resumeFile, navigate]);

  const handleAnalyze = async () => {
    if (!resumeFile) return;

    if (!jobDescription.trim()) {
      setError('Please enter a job description');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await analyzeResume(resumeFile, jobDescription);

      // Navigate to analysis page with results
      navigate('/analysis', {
        state: {
          analysisData: result.data,
          resumeFileName: resumeFile.name
        }
      });
    } catch (err: any) {
      console.error('Analysis error:', err);
      setError(
        err.response?.data?.detail ||
        'Failed to analyze resume. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-cream flex items-center justify-center p-8">
      <div className="w-full max-w-3xl">
        {/* Title */}
        <h1 className="font-retro text-5xl mb-8 text-text font-bold text-center">
          Enter Job Description
        </h1>

        {/* Resume file name */}
        {resumeFile && (
          <div className="mb-4 text-center">
            <p className="font-retro text-text">
              Resume: <span className="font-bold">{resumeFile.name}</span>
            </p>
          </div>
        )}

        {/* Textarea */}
        <textarea
          className="
            w-full
            h-64
            p-6
            bg-white
            border-4
            border-text
            rounded-box
            font-retro
            text-text
            text-lg
            shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]
            focus:outline-none
            focus:translate-x-[2px]
            focus:translate-y-[2px]
            focus:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]
            transition-all
            resize-none
          "
          placeholder="Paste the job description here...&#10;&#10;Include key requirements, responsibilities, and required skills."
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          disabled={loading}
        />

        {/* Analyze Button */}
        <div className="mt-8 text-center">
          <button
            className="
              bg-peach
              text-text
              px-12
              py-4
              rounded-retro
              font-retro
              text-xl
              shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]
              hover:translate-x-[2px]
              hover:translate-y-[2px]
              hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]
              active:translate-x-[4px]
              active:translate-y-[4px]
              active:shadow-none
              transition-all
              disabled:opacity-50
              disabled:cursor-not-allowed
            "
            onClick={handleAnalyze}
            disabled={loading || !jobDescription.trim()}
          >
            {loading ? 'Analyzing...' : 'Analyze Resume'}
          </button>
        </div>

        {/* Loading Message */}
        {loading && (
          <div className="mt-6 text-center">
            <p className="font-retro text-text text-lg">
              Analyzing your resume...
              <br />
              <span className="text-sm">This may take 10-30 seconds</span>
            </p>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div
            className="
              mt-6
              bg-red-100
              border-2
              border-red-500
              text-red-700
              px-6
              py-3
              rounded-box
              font-retro
              shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]
            "
          >
            {error}
          </div>
        )}

        {/* Back Button */}
        <div className="mt-6 text-center">
          <button
            className="font-retro text-text underline hover:no-underline"
            onClick={() => navigate('/')}
            disabled={loading}
          >
            Back to Upload
          </button>
        </div>
      </div>
    </div>
  );
};
