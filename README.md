# AI-Based Resume Screening and Candidate Shortlisting System

An AI-powered recruitment support system that analyzes resumes against job descriptions using NLP, traditional text similarity, semantic embeddings, and transparent scoring.

## Overview

Recruiters often need to review a large number of resumes for a single position.

This project provides an automated candidate analysis pipeline that:

- Accepts PDF and DOCX resumes
- Extracts resume text
- Extracts candidate information
- Identifies technical skills
- Stores candidate profiles
- Accepts job descriptions
- Matches candidates against job requirements
- Calculates explicit skill matching
- Calculates TF-IDF similarity
- Calculates semantic similarity using Sentence Transformers
- Generates a transparent relevance score
- Stores screening results
- Provides a recruiter dashboard
- Supports JWT authentication
- Runs using Docker

## System Architecture

Resume
→ Text Extraction
→ Text Cleaning
→ Information Extraction
→ Candidate Database

Job Description
→ Job Processing
→ Required/Preferred Skills

Candidate + Job
→ Skill Matching
→ TF-IDF Similarity
→ Semantic Similarity
→ Weighted Scoring
→ Screening Result

## Technology Stack

### Frontend

- React
- Vite
- Axios
- React Router
- CSS

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- JWT Authentication

### NLP / Machine Learning

- scikit-learn
- TF-IDF
- Cosine Similarity
- Sentence Transformers
- all-MiniLM-L6-v2

### Database

- SQLite

### Deployment

- Docker
- Docker Compose
- Nginx

## Features

### Resume Processing

Supports:

- PDF
- DOCX

Extracted information includes:

- Name
- Email
- Phone
- Skills
- Education
- Experience
- Projects

### Candidate Matching

The system calculates:

- Required skill match
- Preferred skill match
- TF-IDF similarity
- Semantic similarity
- Overall relevance score

### Authentication

The backend supports:

- User registration
- User login
- JWT-based authentication
- Protected API endpoints

## Scoring

The prototype currently uses:

- Required skills: 40%
- Preferred skills: 10%
- TF-IDF similarity: 15%
- Semantic similarity: 35%

These weights are configurable and should be treated as prototype parameters rather than validated hiring criteria.

## Important Limitation

This system is designed as a recruitment decision-support tool.

It should not independently make employment decisions.

The system should not use protected or sensitive personal attributes for candidate ranking.

Recruiters should review the underlying evidence before making decisions.

## Running Locally

### Backend

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt

# Scanned PDFs need Tesseract OCR in addition to the Python packages above.
# If it is not on PATH, set TESSERACT_CMD to the full path to tesseract.exe.
# PowerShell example:
$env:TESSERACT_CMD = "C:\Program Files\Tesseract-OCR\tesseract.exe"

uvicorn app.main:app --reload