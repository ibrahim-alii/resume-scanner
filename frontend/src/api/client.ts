import axios from 'axios';
import type { AnalysisResponse } from '../types/api';

const API_BASE = '/api';

export const analyzeResume = async (
  file: File,
  jobDescription: string
): Promise<AnalysisResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('job_description', jobDescription);

  const response = await axios.post<AnalysisResponse>(
    `${API_BASE}/analyze`,
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 60000, 
    }
  );

  return response.data;
};

export const checkHealth = async () => {
  const response = await axios.get(`${API_BASE}/health`);
  return response.data;
};
