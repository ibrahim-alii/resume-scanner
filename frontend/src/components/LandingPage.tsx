import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export const LandingPage: React.FC = () => {
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // Validate file type
    if (!file.name.endsWith('.pdf') && !file.name.endsWith('.docx')) {
      setError('Please upload a PDF or DOCX file');
      return;
    }

    // Validate file size (10MB)
    if (file.size > 10 * 1024 * 1024) {
      setError('File size must be less than 10MB');
      return;
    }

    // Navigate to job description page with the file
    navigate('/job-description', { state: { resumeFile: file } });
  };

  return (
    <div className="min-h-screen bg-cream flex items-center justify-center p-8">
      <div className="text-center">
        {/* Title */}
        <h1 className="font-retro text-7xl mb-4 text-text font-bold">
          ResuMax
        </h1>

        {/* Description */}
        <p className="font-retro text-xl mb-12 text-text">
          Match your resume to any job - instantly
        </p>

        {/* Upload Button */}
        <label htmlFor="file-upload">
          <div
            className="
              bg-peach
              text-text
              px-12
              py-4
              rounded-retro
              font-retro
              text-xl
              inline-block
              cursor-pointer
              shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]
              hover:translate-x-[2px]
              hover:translate-y-[2px]
              hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]
              active:translate-x-[4px]
              active:translate-y-[4px]
              active:shadow-none
              transition-all
            "
          >
            Upload Resume
          </div>
        </label>
        <input
          id="file-upload"
          type="file"
          accept=".pdf,.docx"
          onChange={handleFileSelect}
          className="hidden"
        />

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
      </div>
    </div>
  );
};
