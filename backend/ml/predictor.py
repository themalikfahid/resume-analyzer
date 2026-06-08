from __future__ import annotations

import os

import joblib
from scipy.sparse import csr_matrix, hstack


class MLPredictor:
    def __init__(self) -> None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_path = os.path.join(base_dir, "model.pkl")
        self.vectorizer_path = os.path.join(base_dir, "vectorizer.pkl")

        self.model = joblib.load(self.model_path)
        self.vectorizer = joblib.load(self.vectorizer_path)

    def predict(self, resume_text: str, jd_text: str) -> str:
        combined = f"{resume_text} {jd_text}"
        vec = self.vectorizer.transform([combined])
        vec_final = hstack([vec, csr_matrix([[0, 0, 0, 0, 0, 0]])])
        prediction = self.model.predict(vec_final)[0]
        return str(prediction)
