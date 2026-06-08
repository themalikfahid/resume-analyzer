from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from agents.ats_scorer import ATSScorerAgent
from agents.recommender import RecommenderAgent
from agents.resume_parser import ResumeParserAgent
from agents.skill_analyzer import SkillAnalyzerAgent


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

app = FastAPI(title="Multi-Agent ATS Resume Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ORIGIN", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

parser_agent = ResumeParserAgent()
skill_agent = SkillAnalyzerAgent()
scorer_agent = ATSScorerAgent()
recommender_agent = RecommenderAgent()


@app.get("/")
def root() -> dict:
    return {"status": "ATS Analyzer API running"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...), jd_text: str = Form(...)) -> dict:
    try:
        extension = (file.filename or "").split(".")[-1].lower()
        if extension not in {"pdf", "docx"}:
            raise HTTPException(status_code=400, detail="Only PDF and DOCX files are allowed")

        file_bytes = await file.read()

        parsed = parser_agent.parse(file_bytes, extension)
        skills = skill_agent.analyze(parsed["clean_text"], jd_text)
        score_data = scorer_agent.score(
            skills["matched_skills"],
            skills["missing_skills"],
            parsed["clean_text"],
            jd_text,
        )
        recs = recommender_agent.recommend(
            skills["missing_skills"],
            score_data["ats_score"],
            jd_text,
        )

        return {
            "ats_score": score_data["ats_score"],
            "skill_score": score_data["skill_score"],
            "semantic_score": score_data["semantic_score"],
            "matched_skills": skills["matched_skills"],
            "missing_skills": skills["missing_skills"],
            "predicted_label": score_data["predicted_label"],
            "recommendations": recs["recommendations"],
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Processing error: {exc}") from exc
