from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from scipy.sparse import csr_matrix, hstack
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split


def _compute_numeric_features(df: pd.DataFrame) -> pd.DataFrame:
    resume_words = df["resume_text"].fillna("").str.lower().str.split()
    jd_words = df["jd_text"].fillna("").str.lower().str.split()

    matched_count = []
    missing_count = []
    skill_coverage = []
    match_score = []
    exp_match = []
    edu_match = []

    for r_words, j_words in zip(resume_words, jd_words):
        r_set = set(r_words)
        j_set = set(j_words)
        matched = len(r_set & j_set)
        missing = len(j_set - r_set)
        coverage = matched / max(len(j_set), 1)

        matched_count.append(matched)
        missing_count.append(missing)
        skill_coverage.append(coverage)
        match_score.append(coverage * 100)
        exp_match.append(1 if "experience" in r_set and "experience" in j_set else 0)
        edu_match.append(1 if "education" in r_set and "education" in j_set else 0)

    return pd.DataFrame(
        {
            "skill_coverage": skill_coverage,
            "matched_count": matched_count,
            "missing_count": missing_count,
            "match_score": match_score,
            "exp_match": exp_match,
            "edu_match": edu_match,
        }
    )


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    data_path = base_dir / "data" / "ats_resume_dataset.csv"
    model_path = base_dir / "model.pkl"
    vectorizer_path = base_dir / "vectorizer.pkl"

    df = pd.read_csv(data_path)

    combined_text = df["resume_text"].fillna("") + " " + df["jd_text"].fillna("")
    num_features = _compute_numeric_features(df)
    y = df["label"].astype(str)

    X_train_text, X_test_text, X_train_num, X_test_num, y_train, y_test = train_test_split(
        combined_text,
        num_features.values,
        y,
        test_size=0.2,
        stratify=y,
        random_state=42,
    )

    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        sublinear_tf=True,
        min_df=2,
    )

    X_train_tfidf = vectorizer.fit_transform(X_train_text)
    X_test_tfidf = vectorizer.transform(X_test_text)

    X_train_final = hstack([X_train_tfidf, csr_matrix(X_train_num)])
    X_test_final = hstack([X_test_tfidf, csr_matrix(X_test_num)])

    model = RandomForestClassifier(
        n_estimators=200,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train_final, y_train)

    y_pred = model.predict(X_test_final)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(classification_report(y_test, y_pred))

    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)
    print("Model saved successfully")
