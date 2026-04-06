
SKILLS_DB = [
    "python", "java", "sql", "machine learning", "nlp",
    "deep learning", "tensorflow", "keras", "pandas", "numpy",
    "scikit-learn", "flask", "django", "html", "css", "javascript",
    "react", "node", "mongodb", "mysql", "docker", "git", "aws",
    "data analysis", "data science", "computer vision", "excel",
    "power bi", "tableau", "c++", "r", "scala", "hadoop", "spark"
]

def get_skill_gaps(resume_skills, job_description):
    job_lower = job_description.lower()
    required = [s for s in SKILLS_DB if s in job_lower]
    missing = [s for s in required if s not in resume_skills]
    return missing

def get_feedback(score):
    if score >= 80:
        return "✅ Excellent match! Your resume is well aligned with this job."
    elif score >= 60:
        return "🟡 Good match! Consider adding a few missing skills."
    elif score >= 40:
        return "🟠 Average match. Work on the missing skills listed below."
    else:
        return "🔴 Low match. Your resume needs significant improvement for this role."
    