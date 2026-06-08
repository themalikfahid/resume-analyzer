from __future__ import annotations

import re
from typing import Iterable

import spacy
from spacy.matcher import PhraseMatcher


class SkillAnalyzerAgent:
    SKILLS = [
        "Python",
        "Java",
        "C++",
        "JavaScript",
        "TypeScript",
        "React",
        "React.js",
        "Node.js",
        "FastAPI",
        "Django",
        "Flask",
        "SQL",
        "PostgreSQL",
        "MongoDB",
        "Redis",
        "Docker",
        "Kubernetes",
        "AWS",
        "Azure",
        "GCP",
        "Git",
        "Linux",
        "Bash",
        "Machine Learning",
        "Deep Learning",
        "NLP",
        "TensorFlow",
        "PyTorch",
        "scikit-learn",
        "Pandas",
        "NumPy",
        "Matplotlib",
        "spaCy",
        "NLTK",
        "BERT",
        "Transformers",
        "FAISS",
        "LangChain",
        "RAG",
        "Vector Database",
        "Sentence-BERT",
        "REST API",
        "GraphQL",
        "Microservices",
        "CI/CD",
        "Jenkins",
        "Terraform",
        "Ansible",
        "System Design",
        "Data Structures",
        "Algorithms",
        "OOP",
        "Agile",
        "Scrum",
        "Tableau",
        "Power BI",
        "Excel",
        "Statistics",
        "R",
        "Spark",
        "Hadoop",
        "Kafka",
        "RabbitMQ",
        "Nginx",
        "HTML",
        "CSS",
        "Tailwind CSS",
        "Redux",
        "Next.js",
        "Vue.js",
        "Angular",
        "Figma",
        "Penetration Testing",
        "Cybersecurity",
        "Firewalls",
        "Data Analysis",
        "Computer Vision",
        "OpenCV",
        "Selenium",
        "FastAPI",
    ]

    SKILL_ALIASES = {
        "React": ["react", "reactjs", "react js", "react.js"],
        "React.js": ["react", "reactjs", "react js", "react.js"],
        "Node.js": ["node", "nodejs", "node js", "node.js"],
        "Next.js": ["next", "nextjs", "next js", "next.js"],
        "FastAPI": ["fastapi", "fast api"],
        "scikit-learn": ["scikit-learn", "sklearn", "scikit learn"],
        "CI/CD": ["ci/cd", "ci cd", "cicd"],
        "Tailwind CSS": ["tailwind css", "tailwind"],
        "JavaScript": ["javascript", "js"],
        "TypeScript": ["typescript", "ts"],
        "PostgreSQL": ["postgresql", "postgres"],
        "Machine Learning": ["machine learning", "ml"],
        "NLP": ["natural language processing", "nlp"],
        "GraphQL": ["graphql"],
        "REST API": ["rest api", "restapi", "rest"],
        "Vue.js": ["vue", "vuejs", "vue js", "vue.js"],
        "Angular": ["angular"],
        "Redux": ["redux"],
        "Sentence-BERT": ["sentence-bert", "sentence bert", "sbert"],
        "spaCy": ["spacy"],
    }

    def __init__(self) -> None:
        self.nlp = self._load_nlp()
        self.matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        self._canonical_by_alias = self._build_alias_lookup()
        patterns = [self.nlp.make_doc(skill) for skill in self.SKILLS]
        self.matcher.add("SKILLS", patterns)

    def analyze(self, resume_text: str, jd_text: str) -> dict:
        resume_skills = self._extract_skills(resume_text)
        jd_skills = self._extract_skills(jd_text)

        matched_skills = [skill for skill in resume_skills if skill in jd_skills]
        missing_skills = [skill for skill in jd_skills if skill not in resume_skills]

        print("Resume skills:", resume_skills)
        print("JD skills:", jd_skills)
        print("Matched skills:", matched_skills)
        print("Missing skills:", missing_skills)

        return {
            "resume_skills": resume_skills,
            "jd_skills": jd_skills,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
        }

    def _load_nlp(self):
        try:
            return spacy.load("en_core_web_sm")
        except Exception:
            nlp = spacy.blank("en")
            if "sentencizer" not in nlp.pipe_names:
                nlp.add_pipe("sentencizer")
            return nlp

    def _build_alias_lookup(self) -> dict[str, str]:
        alias_lookup: dict[str, str] = {}
        for skill in self.SKILLS:
            alias_lookup[self._normalize_skill_text(skill)] = skill

        for canonical_skill, aliases in self.SKILL_ALIASES.items():
            if canonical_skill not in self.SKILLS:
                continue
            for alias in aliases:
                alias_lookup[self._normalize_skill_text(alias)] = canonical_skill

        return alias_lookup

    def _extract_skills(self, text: str) -> list[str]:
        normalized_text = self._normalize_text(text)
        doc = self.nlp(normalized_text)

        found: list[str] = []
        seen: set[str] = set()

        for _, start, end in self.matcher(doc):
            skill_text = doc[start:end].text
            canonical = self._canonicalize(skill_text)
            if canonical and canonical not in seen:
                seen.add(canonical)
                found.append(canonical)

        compact_text = normalized_text.replace(" ", "")

        for alias, canonical in self._canonical_by_alias.items():
            if not alias:
                continue

            spaced_match = re.search(rf"(?<!\w){re.escape(alias)}(?!\w)", normalized_text)
            compact_match = alias in compact_text

            if spaced_match or compact_match:
                if canonical not in seen:
                    seen.add(canonical)
                    found.append(canonical)

        ordered_found = self._order_skills(found)
        return ordered_found

    def _canonicalize(self, skill_text: str) -> str:
        normalized = self._normalize_skill_text(skill_text)
        return self._canonical_by_alias.get(normalized, skill_text.strip())

    def _normalize_text(self, text: str) -> str:
        value = (text or "").lower()
        value = value.replace("/", " ")
        value = value.replace("-", " ")
        value = value.replace(".", " ")
        value = value.replace("_", " ")
        value = re.sub(r"\s+", " ", value)
        return value.strip()

    def _normalize_skill_text(self, text: str) -> str:
        value = self._normalize_text(text)
        value = value.replace(" ", "")
        return value

    def _order_skills(self, skills: Iterable[str]) -> list[str]:
        ordered = []
        seen = set()
        skill_position = {skill: index for index, skill in enumerate(self.SKILLS)}
        for skill in sorted(skills, key=lambda item: skill_position.get(item, len(self.SKILLS))):
            if skill not in seen:
                seen.add(skill)
                ordered.append(skill)
        return ordered
