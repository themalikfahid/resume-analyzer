from __future__ import annotations

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from ml.predictor import MLPredictor


class ATSScorerAgent:
    def __init__(self) -> None:
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def score(self, matched_skills, missing_skills, resume_text, jd_text) -> dict:
        jd_total = len(matched_skills) + len(missing_skills)
        skill_score = (len(matched_skills) / max(jd_total, 1)) * 60

        resume_vec = self.model.encode([resume_text])
        jd_vec = self.model.encode([jd_text])
        sim = cosine_similarity(resume_vec, jd_vec)[0][0]
        semantic_score = float(sim) * 40

        ats_score = min(100, round(skill_score + semantic_score))

        try:
            predicted_label = MLPredictor().predict(resume_text, jd_text)
        except Exception:
            predicted_label = "N/A"

        return {
            "ats_score": int(ats_score),
            "skill_score": float(skill_score),
            "semantic_score": float(semantic_score),
            "predicted_label": str(predicted_label),
        }
