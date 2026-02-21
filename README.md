# Resume Scanner

> AI-powered resume analysis tool that extracts skills, matches candidates to job descriptions, and provides intelligent improvement suggestions.

## Overview

Resume Scanner is a full-stack application that leverages natural language processing (NLP) and machine learning to analyze resumes against job descriptions. It provides detailed scoring, skill gap analysis, and AI-generated recommendations to help candidates optimize their resumes for specific roles.

## Features

- **AI-Powered Skill Extraction**: Multi-method extraction using Named Entity Recognition (NER), hybrid BERT embeddings, and regex patterns
- **Multi-Format Support**: Parse PDF and DOCX resume files with automatic text extraction
- **Intelligent Matching**: Composite scoring system combining BERT semantic similarity and TF-IDF analysis
- **Gemini AI Suggestions**: Get actionable improvement recommendations including:
  - Skill gap identification with learning priorities
  - Quantification opportunities for impact statements
  - ATS (Applicant Tracking System) keyword optimization
  - Enhanced action verbs and strategic positioning
- **Visual Dashboard**: Modern React interface with real-time analysis results
- **Named Entity Recognition**: Extract names, education, and experience using spaCy's advanced NLP models
- **Detailed Skills Comparison**: View matching, missing, and additional skills with match percentages

## Tech Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **Machine Learning**:
  - scikit-learn for TF-IDF analysis
  - sentence-transformers (BERT) for semantic similarity
  - PyTorch as the ML backend
- **NLP**: spaCy for named entity recognition
- **Document Parsing**: pypdf and python-docx for resume extraction
- **AI Integration**: Google Gemini API for intelligent suggestions

### Frontend
- **React 19** with TypeScript for type safety
- **Vite** - Next-generation build tool and dev server
- **Tailwind CSS v4** - Modern utility-first CSS with custom dark slate/cyan theme
- **React Router v7** - Client-side routing
- **Axios** - HTTP client for API communication

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Node.js 16+ and npm
- Google Gemini API key (optional, for AI suggestions)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd resume-scanner
   ```

2. **Backend Setup**:
   ```bash
   # Install Python dependencies
   pip install -r requirements.txt

   # Download spaCy model (required for NER)
   python -m spacy download en_core_web_lg
   ```

3. **Configure Environment Variables**:

   Create a `.env` file in the root directory:
   ```bash
   # Optional: Add your Gemini API key for AI-powered suggestions
   GEMINI_API_KEY=your_api_key_here

   # Optional: Custom port (defaults to 8001)
   PORT=8001
   ```

4. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   ```

### Running the Application

1. **Start the Backend Server** (from root directory):
   ```bash
   python api.py
   ```
   The API will be available at `http://localhost:8001`

   - API Documentation: `http://localhost:8001/docs`
   - Health Check: `http://localhost:8001/api/health`

2. **Start the Frontend** (in a new terminal, from `frontend/` directory):
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`

3. **Access the Application**:

   Open your browser and navigate to `http://localhost:5173`

## Usage

1. Upload your resume (PDF or DOCX format, max 10MB)
2. Paste the job description you're targeting
3. Click "Analyze Resume" to receive:
   - Composite match score (0-100)
   - Detailed skills comparison
   - AI-powered improvement suggestions (if Gemini API configured)
4. Review the results and optimize your resume based on recommendations

## Project Structure

```
resume-scanner/
├── api.py                    # FastAPI backend entry point
├── app/                      # Backend application modules
│   ├── gemini_service.py     # Gemini AI integration
│   ├── ner_extractor.py      # Named entity recognition
│   ├── parser.py             # Document text extraction
│   ├── scoring.py            # BERT + TF-IDF scoring
│   ├── skills_database.py    # Skills taxonomy
│   └── skills_extractor.py   # Skill extraction logic
├── frontend/                 # React + TypeScript frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   └── App.tsx           # Main application
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## API Endpoints

- `GET /api/health` - Health check and model status
- `POST /api/analyze` - Analyze resume against job description
  - Parameters:
    - `file`: Resume file (PDF/DOCX)
    - `job_description`: Job description text

## Development

### Backend Development

The backend uses FastAPI with automatic OpenAPI documentation:
- Interactive API docs: `http://localhost:8001/docs`
- Alternative docs: `http://localhost:8001/redoc`

Models are pre-loaded at startup to avoid first-request delays.

### Frontend Development

The frontend uses Vite's hot module replacement (HMR) for instant updates:
```bash
cd frontend
npm run dev
```

Build for production:
```bash
npm run build
```

## License

This project is available for educational and personal use.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.
