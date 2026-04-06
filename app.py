import streamlit as st
import pdfplumber
import tempfile
import os
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords', quiet=True)

import subprocess
subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], 
               capture_output=True)

import spacy
from docx import Document

nlp = spacy.load("en_core_web_sm")

# Words that are never useful as skills
IGNORE_WORDS = set([
    "title", "job", "required", "requirements", "responsibilities","looking", "join", "team", "growing", "working", "ensure","experience", "years",
    "ability", "strong", "good", "plus","familiarity", "knowledge", "understanding", "proficiency","work", "using", "use", "also","well", "new",
    "etc","following", "including", "based", "per", "via", "within","will", "must", "should", "can", "may", "need", "like","least", "every",
    "across", "help", "make", "along","needed", "preferred", "such", "their", "they", "them","this", "that", "these","those", "with", "from",
    "into","about", "above", "below", "between", "through", "during","candidate", "company", "position", "role", "apply","excellent", "great",
    "best", "top", "highly", "very","key", "core", "main", "primary", "essential", "critical","hands", "onto", "seeking", "wanted","desired",
    "ideally","bonus", "furthermore", "additionally", "the", "and", "for","are", "was", "has", "have", "had", "been", "its", "our","your", "his",
    "her", "both", "each", "all", "any", "few","more", "most", "other", "some", "nor", "not", "only","own", "same", "than", "too", "just","but",
    "who", "which", "what", "when", "where", "how", "why", "while","although", "however", "therefore", "thus", "hence","skills", "skill", "list",
    "including", "preferred","minimum", "maximum", "least", "plus", "bonus", "nice", "hands","received","completed", "obtained", "conducted"
])

# Step 1 - Read the resume file
def read_resume(file_path):
    text = ""
    try:
        if file_path.endswith(".pdf"):
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    if page.extract_text():
                        text += page.extract_text() + "\n"
        elif file_path.endswith(".docx"):
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
    except Exception as e:
        st.error("Could not read file: " + str(e))
    return text

# Step 2 - Clean text properly
def clean_text(text):
    # Add full stop after each line so SpaCy treats them separately
    lines = text.lower().split('\n')
    lines = [line.strip() + '.' for line in lines if line.strip()]
    text = ' '.join(lines)
    # Remove special characters but keep letters and full stops
    text = re.sub(r'[^a-zA-Z\s\.]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Step 3 - Extract keywords using SpaCy
def extract_keywords(text):
    stop_words = set(stopwords.words('english'))
    all_ignore = stop_words.union(IGNORE_WORDS)
    cleaned = clean_text(text)
    doc = nlp(cleaned)
    found = set()

    # Get noun phrases - SpaCy groups words that belong together
    for chunk in doc.noun_chunks:
        phrase = chunk.text.strip()
        words = phrase.split()

        # Remove ignore words from start and end of phrase
        while words and words[0] in all_ignore:
            words.pop(0)
        while words and words[-1] in all_ignore:
            words.pop()
        phrase = " ".join(words)

        # Only keep clean meaningful phrases
        if (len(phrase) > 2 and
            len(words) >= 1 and
            not all(w in all_ignore for w in words)):
            found.add(phrase)

    # Add single important words not already in a phrase
    for word in cleaned.split():
        word = re.sub(r'[^a-zA-Z]', '', word)
        if (len(word) > 2 and
            word not in all_ignore):
            already_covered = any(
                word in phrase.split()
                for phrase in found
            )
            if not already_covered:
                found.add(word)
    return found

# Step 4 - Find matching keywords
def find_matching(resume_text, job_text):
    resume_kw = extract_keywords(resume_text)
    job_kw = extract_keywords(job_text)
    matched = set()
    for job_phrase in job_kw:
        for resume_phrase in resume_kw:
            if (job_phrase == resume_phrase or
                job_phrase in resume_phrase or
                resume_phrase in job_phrase):
                matched.add(job_phrase)
                break
    return sorted(matched)

# Step 5 - Find missing keywords
def find_missing(resume_text, job_text):
    job_kw = extract_keywords(job_text)
    matched = set(find_matching(resume_text, job_text))
    missing = [w for w in job_kw if w not in matched]
    return sorted(missing)

# Step 6 - Calculate match score
def match_score(resume_text, job_text):
    job_kw = extract_keywords(job_text)
    matched = find_matching(resume_text, job_text)
    if len(job_kw) == 0:
        return 0
    score = (len(matched) / len(job_kw)) * 100
    return round(score, 2)

# Step 7 - Give feedback based on score
def give_feedback(score):
    if score >= 80:
        return "Excellent match! Your resume is perfect for this job."
    elif score >= 60:
        return "Good match! Your resume fits this job well."
    elif score >= 40:
        return "Average match. Try adding the missing keywords below."
    else:
        return "Low match. Your resume needs improvement for this job."

#Website Interface 
st.set_page_config(page_title="Smart Resume Analyzer", page_icon="📄")
st.title("Smart Resume Analyzer")
st.write("Upload your resume and paste any job description to see how well you match!")
uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
job_description = st.text_area("Paste Job Description Here", height=200)
if uploaded_file and job_description:

    # Save uploaded file temporarily
    suffix = os.path.splitext(uploaded_file.name)[1]
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(uploaded_file.read())
    tmp.close()
    with st.spinner("Analyzing your resume..."):
        resume_text = read_resume(tmp.name)
        score = match_score(resume_text, job_description)
        matched = find_matching(resume_text, job_description)
        missing = find_missing(resume_text, job_description)
        feedback = give_feedback(score)
    st.divider()
    st.header("Results")

    # Show 3 metric boxes
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Match Score", str(score) + "%")
    with col2:
        st.metric("Keywords Matched", len(matched))
    with col3:
        st.metric("Keywords Missing", len(missing))
    st.progress(int(score))
    st.subheader("Feedback")
    st.info(feedback)
    st.divider()
    col4, col5 = st.columns(2)
    with col4:
        st.subheader("Keywords Found in Resume")
        if matched:
            for word in matched:
                st.success(word)
        else:
            st.warning("No matching keywords found")
    with col5:
        st.subheader("Keywords Missing from Resume")
        if missing:
            for word in missing:
                st.error(word)
        else:
            st.success("You have all the required keywords!")

    # Clean up temp file
    os.unlink(tmp.name)
else:
    st.info(" Please upload your resume and paste a job description above.")
