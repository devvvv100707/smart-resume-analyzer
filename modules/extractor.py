import spacy
import re

nlp = spacy.load("en_core_web_sm")

SKILLS_DB = [
    "python", "java", "sql", "machine learning", "nlp",
    "deep learning", "tensorflow", "keras", "pandas", "numpy",
    "scikit-learn", "flask", "django", "html", "css", "javascript",
    "react", "node", "mongodb", "mysql", "docker", "git", "aws",
    "data analysis", "data science", "computer vision",
    "microsoft excel", "power bi", "tableau", "c++", "scala",
    "hadoop", "spark", "case management", "scheduling",
    "staff development", "customer service", "record keeping",
    "communication skills", "team building", "administrative"
]

def extract_entities(text):
    doc = nlp(text)
    entities = {"name": [], "org": [], "skills": []}

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            entities["name"].append(ent.text)
        elif ent.label_ == "ORG":
            entities["org"].append(ent.text)

    text_lower = text.lower()
    for skill in SKILLS_DB:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            entities["skills"].append(skill)

    return entities