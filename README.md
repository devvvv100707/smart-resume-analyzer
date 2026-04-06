## Smart Resume Analyzer  
## AI-powered Resume Screening using NLP + Streamlit  

A smart **NLP-based resume screening system** that compares a candidate’s resume with a job description and calculates how well they match.

Built using **Python, SpaCy, NLTK, and Streamlit**, this project extracts important keywords from both the resume and job description, finds matching and missing skills, and provides an overall **resume match score with personalized feedback**.

## Overview
Recruiters often use **ATS (Applicant Tracking Systems)** to filter resumes before shortlisting candidates.
This project simulates a **basic ATS-style resume analyzer** by:
- extracting important skills and phrases
- comparing resume content with job requirements
- highlighting missing keywords
- generating a compatibility score
- suggesting resume improvements,
this makes it useful for:
  - students improving resumes
  - job seekers optimizing ATS scores
  - beginners learning NLP projects
  - ML portfolios

---
## Features
- Upload resume in **PDF or DOCX**
- Paste any **job description**
- NLP-based keyword extraction using **SpaCy**
- Stopword filtering using **NLTK**
- Generates **resume match percentage**
- Displays **matched keywords**
- Highlights **missing keywords**
- Gives **smart feedback**
- Interactive **Streamlit web interface**

---

## Tech Stack
- **Python**
- **Streamlit**
- **SpaCy**
- **NLTK**
- **pdfplumber**
- **python-docx**
- **Regex**
- **Natural Language Processing (NLP)**

---

## Project Structure
```bash
Smart-Resume-Analyzer/
│── app.py
│── requirements.txt
│── .gitignore
│── README.md
```

---

## Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/smart-resume-analyzer.git
cd smart-resume-analyzer
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3️⃣ Run the project
```bash
streamlit run app.py
```

---

## How It Works
1. Upload your resume  
2. Paste the target job description  
3. The system extracts important keywords  
4. Resume and JD are compared  
5. Match score + feedback is displayed  

---

## Output Includes
- ✅ Match Score
- ✅ Matched Skills
- ✅ Missing Skills
- ✅ Resume Suggestions
- ✅ Feedback based on ATS compatibility

---

##  Future Improvements
- Advanced ATS scoring system
- Resume ranking for multiple candidates
- ML-based candidate recommendation
- Export report as PDF
- Deploy on Streamlit Cloud
- Role-specific skill suggestions

---

## Contributors
- **Aditi Singh**
- **Dev Vashishtha**

---

