from __future__ import annotations

from io import BytesIO

import pdfplumber
from docx import Document

from nlp.preprocessor import preprocess


class ResumeParserAgent:
    def parse(self, file_bytes: bytes, file_type: str) -> dict:
        extracted_text = self._extract_text(file_bytes, file_type)
        if not extracted_text.strip():
            raise ValueError("No text could be extracted from the uploaded file.")

        processed = preprocess(extracted_text)
        return {
            "raw_text": extracted_text,
            "clean_text": processed["clean_text"],
            "tokens": processed["tokens"],
            "entities": processed["entities"],
        }

    def _extract_text(self, file_bytes: bytes, file_type: str) -> str:
        if file_type == "pdf":
            texts: list[str] = []
            with pdfplumber.open(BytesIO(file_bytes)) as pdf:
                for page in pdf.pages:
                    texts.append(page.extract_text() or "")
            return "\n".join(texts)

        if file_type == "docx":
            doc = Document(BytesIO(file_bytes))
            paragraphs = [paragraph.text for paragraph in doc.paragraphs]
            return "\n".join(paragraphs)

        raise ValueError("Unsupported file type. Please upload PDF or DOCX.")
