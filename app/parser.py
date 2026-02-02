import os
import re
from pathlib import Path
from typing import Optional, Dict, List

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

try:
    from docx import Document
except ImportError:
    Document = None


def extract_from_pdf(file_path: str) -> str:
    if PdfReader is None:
        raise ImportError("pypdf is not installed. Install it with: pip install pypdf")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        pdf = PdfReader(file_path)
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")


def extract_from_word(file_path: str) -> str:
    if Document is None:
        raise ImportError("python-docx is not installed. Install it with: pip install python-docx")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        raise ValueError(f"Failed to extract text from Word document: {str(e)}")


def extract_text(file_path: str) -> str:
    file_path = str(file_path)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    file_ext = Path(file_path).suffix.lower()
    
    if file_ext == ".pdf":
        return extract_from_pdf(file_path)
    elif file_ext == ".docx":
        return extract_from_word(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_ext}. Supported formats: .pdf, .docx")


def extract_contact_info(text: str) -> Dict[str, List[str]]:
    
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    phone_pattern = r'(?:\+?1[-\.\s]?)?\(?\d{3}\)?[-\.\s]?\d{3}[-\.\s]?\d{4}'
    
    linkedin_pattern = r'(?:https?://)?(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+'
    
    github_pattern = r'(?:https?://)?(?:www\.)?github\.com/[a-zA-Z0-9_-]+'
    
    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)
    linkedin = re.findall(linkedin_pattern, text, re.IGNORECASE)
    github = re.findall(github_pattern, text, re.IGNORECASE)
    
    return {
        'email': emails,
        'phone': phones,
        'linkedin': linkedin,
        'github': github
    }

