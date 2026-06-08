from __future__ import annotations

import json
from pathlib import Path

import faiss
import numpy
from sentence_transformers import SentenceTransformer


PASSAGES = [
    "Use exact keywords from the job description in your Skills section",
    "Avoid tables, columns, and text boxes — ATS cannot parse them correctly",
    "Quantify achievements: improved performance by 40%, reduced costs by 20%",
    "Include a dedicated Skills section with all technical keywords",
    "Use standard headings: Experience, Education, Skills, Projects, Certifications",
    "Save resume as PDF unless the employer specifically requests DOCX",
    "List all tools and technologies in each work experience bullet point",
    "Match your job title to the exact title in the job description",
    "Keep resume to one page if you have less than 5 years experience",
    "Use strong action verbs: Developed, Implemented, Designed, Led, Optimized",
    "Include relevant certifications like AWS, Google, or Microsoft badges",
    "Spell out acronyms at least once: Natural Language Processing (NLP)",
    "Use a simple single-column layout for best ATS compatibility",
    "Include your LinkedIn URL and GitHub profile link",
    "Tailor your resume for each specific job application",
    "Place most relevant skills at the top of your Skills section",
    "Use bullet points not paragraphs for work experience descriptions",
    "Include the company name, job title, dates, and location for each role",
    "Add a professional summary at the top matching the job description",
    "List education with degree, institution, year, and CGPA",
    "Include side projects with tech stack and impact described",
    "Mention team size and your specific role in each project",
    "Use industry-standard tool names: React.js not ReactJS",
    "Include open source contributions if relevant",
    "Mention Agile, Scrum, or Kanban if the job description requires it",
    "Add soft skills only if explicitly mentioned in the job description",
    "Use consistent date format: Jan 2022 - Dec 2023 throughout",
    "Avoid photos, graphics, and colored backgrounds in ATS resumes",
    "Include relevant coursework if you are a fresh graduate",
    "Mention any publications, patents, or research papers",
    "List programming languages with proficiency level if asked",
    "Include volunteer work if it demonstrates relevant technical skills",
    "Use the same resume file name as your full name for professionalism",
    "Avoid first-person pronouns: use Led instead of I led",
    "Include awards and recognition with specific details and year",
    "Mention remote work or distributed team experience if relevant",
    "Add language proficiency if the role requires multilingual skills",
    "Describe impact not just tasks: built system that reduced X by Y",
    "Keep font size between 10-12pt for body text for ATS readability",
    "Test your resume by copying text — if it breaks it will fail ATS",
]


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    index_path = base_dir / "ats_knowledge_base.index"
    passages_path = base_dir / "passages.json"

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(PASSAGES)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(numpy.array(embeddings).astype("float32"))

    faiss.write_index(index, str(index_path))
    with passages_path.open("w", encoding="utf-8") as f:
        json.dump(PASSAGES, f, indent=2)

    print(f"Knowledge base built successfully with {len(PASSAGES)} passages")
