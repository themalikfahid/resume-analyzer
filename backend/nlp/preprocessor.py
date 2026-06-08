from __future__ import annotations

from functools import lru_cache

import nltk
import spacy
from nltk.corpus import stopwords


@lru_cache(maxsize=1)
def _load_nlp() -> spacy.language.Language:
    return spacy.load("en_core_web_sm")


@lru_cache(maxsize=1)
def _load_stopwords() -> set[str]:
    try:
        return set(stopwords.words("english"))
    except LookupError:
        nltk.download("stopwords", quiet=True)
        return set(stopwords.words("english"))


def preprocess(text: str) -> dict:
    nlp = _load_nlp()
    stop_words = _load_stopwords()

    doc = nlp(text or "")

    tokens: list[str] = []
    for token in doc:
        if token.is_stop or token.is_punct or token.is_space:
            continue
        lemma = token.lemma_.lower().strip()
        if not lemma:
            continue
        if lemma in stop_words:
            continue
        tokens.append(lemma)

    entities = [(ent.text, ent.label_) for ent in doc.ents]
    clean_text = " ".join(tokens)

    return {"tokens": tokens, "entities": entities, "clean_text": clean_text}
