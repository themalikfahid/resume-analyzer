<<<<<<< HEAD
# Multi-Agent ATS Resume Analyzer

An AI-powered ATS (Applicant Tracking System) Resume Analyzer that evaluates resumes against job descriptions using Natural Language Processing (NLP), Machine Learning, Retrieval-Augmented Generation (RAG), and Multi-Agent Architecture. The system analyzes skill matches, calculates ATS compatibility scores, predicts candidate suitability, identifies skill gaps, and generates personalized recommendations for resume optimization.

---

## Features

* Resume Upload (PDF & DOCX)
* ATS Compatibility Scoring (0–100)
* Skill Matching & Gap Analysis
* Semantic Similarity Analysis using Sentence-BERT
* Machine Learning-Based Candidate Classification
* RAG-Powered ATS Recommendations
* Multi-Agent Workflow using CrewAI
* Interactive React Dashboard
* Real-Time Resume Evaluation
* No External LLM APIs Required

---

## Tech Stack

### Backend

* Python
* FastAPI
* CrewAI
* spaCy
* NLTK
* scikit-learn
* Sentence Transformers (SBERT)
* FAISS
* pdfplumber
* python-docx

### Frontend

* React.js
* Tailwind CSS
* Axios

### AI & ML

* Random Forest Classifier
* Sentence-BERT Embeddings
* Retrieval-Augmented Generation (RAG)
* Skill Extraction & Semantic Matching

---

## System Architecture

```text
Resume Upload
      │
      ▼
Resume Parser Agent
      │
      ▼
Skill Analyzer Agent
      │
      ▼
ATS Scorer Agent
      │
      ▼
Machine Learning Predictor
      │
      ▼
FAISS Knowledge Retrieval
      │
      ▼
Recommendation Agent
      │
      ▼
Results Dashboard
```

---

## Core Components

### Resume Parser Agent

* Extracts text from PDF and DOCX resumes.
* Performs NLP preprocessing.
* Generates clean and structured resume content.

### Skill Analyzer Agent

* Detects technical skills from resumes and job descriptions.
* Identifies matched and missing skills.
* Computes skill coverage metrics.

### ATS Scorer Agent

* Calculates ATS compatibility scores.
* Uses semantic similarity between resumes and job descriptions.
* Combines skill matching and semantic analysis.

### ML Predictor

* Uses a Random Forest classifier.
* Predicts candidate suitability:

  * High
  * Medium
  * Low

### Recommendation Agent

* Generates personalized ATS recommendations.
* Uses FAISS-based semantic retrieval.
* Suggests improvements based on missing skills and ATS best practices.

---

## Machine Learning Pipeline

1. Resume and Job Description Processing
2. Feature Engineering
3. TF-IDF Vectorization
4. Random Forest Classification
5. Candidate Suitability Prediction

Target Classes:

* High Match
* Medium Match
* Low Match

---

## RAG Knowledge Base

The project implements Retrieval-Augmented Generation (RAG) using:

* Sentence-BERT Embeddings
* FAISS Vector Database
* ATS Optimization Knowledge Base

This enables semantic retrieval of ATS best practices and resume improvement suggestions.

---

## Key Outputs

The system provides:

* ATS Score
* Skill Match Score
* Semantic Match Score
* Matched Skills
* Missing Skills
* Candidate Classification
* Resume Improvement Recommendations

---

## Project Structure

```text
backend/
├── agents/
├── ml/
├── nlp/
├── rag/
└── main.py

frontend/
├── src/
├── public/
└── package.json
```

---

## Installation

### Backend

```bash
=======
# ATS Resume Analyzer - Semester Project

## Setup

### Backend
>>>>>>> 85f80a8 (Initial commit: ATS Resume Analyzer)
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m nltk.downloader stopwords punkt
<<<<<<< HEAD
python rag/knowledge_base.py
python ml/train_model.py
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm start
```

---

## Future Enhancements

* Resume Ranking System
* Job Recommendation Engine
* Recruiter Dashboard
* Interview Readiness Analysis
* Multi-Resume Comparison
* Resume Builder Integration
* Advanced Analytics Dashboard

---

## Academic Project

This project demonstrates the practical implementation of:

* Natural Language Processing
* Machine Learning
* Semantic Search
* Vector Databases
* Retrieval-Augmented Generation
* Multi-Agent AI Systems
* Full-Stack Web Development

---

## Author

**Fahid Asif**
BS Data Science
University of Central Punjab (UCP)
=======
Place ats_resume_dataset.csv in backend/ml/data/
python rag/knowledge_base.py
python ml/train_model.py
uvicorn main:app --reload --port 8000

### Frontend (new terminal)
cd frontend
npm install
npm start

Open: http://localhost:3000
>>>>>>> 85f80a8 (Initial commit: ATS Resume Analyzer)
