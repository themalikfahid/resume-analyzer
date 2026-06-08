from __future__ import annotations

import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class RecommenderAgent:
    def __init__(self) -> None:
        self.base_dir = Path(__file__).resolve().parents[1]
        self.index_path = self.base_dir / "rag" / "ats_knowledge_base.index"
        self.passages_path = self.base_dir / "rag" / "passages.json"

    def recommend(self, missing_skills: list, ats_score: int, jd_text: str) -> dict:
        retrieved = self._retrieve_passages(jd_text)

        recommendations: list[str] = []

        for skill in missing_skills[:3]:
            recommendations.append(
                f"Add '{skill}' to your Skills section and include it in a project or work experience bullet point."
            )

        if ats_score < 40:
            recommendations.append(
                "Your ATS score is low. Carefully read the job description and mirror its exact keywords in your resume."
            )
        elif 40 <= ats_score <= 69:
            recommendations.append(
                "Good start. Focus on adding the missing technical skills through projects or certifications."
            )
        else:
            recommendations.append(
                "Strong match. Polish formatting and quantify achievements (e.g. improved speed by 30%)."
            )

        recommendations.append(
            "Use standard section headings: Skills, Experience, Education, Projects. Avoid tables and columns — ATS cannot read them."
        )
        recommendations.append(
            "Quantify achievements with numbers. Example: 'Reduced API response time by 40% using Redis caching.'"
        )

        if retrieved:
            recommendations.extend(retrieved[:2])

        return {"recommendations": recommendations[:6]}

    def _retrieve_passages(self, jd_text: str) -> list[str]:
        try:
            model = SentenceTransformer("all-MiniLM-L6-v2")
            index = faiss.read_index(str(self.index_path))
            with self.passages_path.open("r", encoding="utf-8") as fp:
                passages = json.load(fp)

            query_vec = model.encode([jd_text])
            distances, indices = index.search(np.array(query_vec).astype("float32"), 5)
            return [passages[i] for i in indices[0] if 0 <= i < len(passages)]
        except Exception:
            return []
