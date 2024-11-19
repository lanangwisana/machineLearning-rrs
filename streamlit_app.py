import streamlit as st
import pandas as pd
import spacy
import io
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter

# Load spaCy model
nlp = spacy.load(".venv/Lib/site-packages/en_core_web_sm/en_core_web_sm-3.8.0")

# Load Job Requirements
job_requirements = pd.read_csv('Job_Category_Requirements.csv')

# Function to extract text from a PDF
def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()

    converter.close()
    fake_file_handle.close()
    return text

# Function to extract skills from text using spaCy
def extract_skills(text):
    doc = nlp(text)
    skills = []
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop:
            skills.append(token.text.lower())
    return set(skills)

# Streamlit App
st.title("CV Scorer and Analyzer")

# Step 1: Select Job Category
st.sidebar.header("Select Job Category")
categories = job_requirements['Job Category'].tolist()
job_category = st.sidebar.selectbox("Choose a Job Category", categories)

# Step 2: Upload CV
uploaded_file = st.file_uploader("Upload your CV (PDF format only)", type=["pdf"])

if uploaded_file is not None:
    # Read and extract text from the uploaded CV
    resume_text = pdf_reader(uploaded_file)
    user_skills = extract_skills(resume_text)
    
    # Fetch Job Requirements for the selected category
    selected_job = job_requirements[job_requirements['Job Category'] == job_category]
    mandatory_skills = set(selected_job['Mandatory Skills'].values[0].strip("[]").replace("'", "").split(", "))
    additional_skills = set(selected_job['Additional Skills'].values[0].strip("[]").replace("'", "").split(", "))
    
    # Calculate Matches and Score
    mandatory_matches = user_skills & mandatory_skills
    additional_matches = user_skills & additional_skills
    mandatory_score = len(mandatory_matches) / len(mandatory_skills) * 70 if mandatory_skills else 0
    additional_score = len(additional_matches) / len(additional_skills) * 30 if additional_skills else 0
    total_score = mandatory_score + additional_score

    # Display Results
    st.subheader("CV Analysis")
    st.write("### Selected Job Category:")
    st.write(f"**{job_category}**")

    st.write("### Job Requirements:")
    st.write(f"**Mandatory Skills:** {', '.join(mandatory_skills)}")
    st.write(f"**Additional Skills:** {', '.join(additional_skills)}")

    st.write("### Skills Matched:")
    st.write(f"**Matched Mandatory Skills:** {', '.join(mandatory_matches)}")
    st.write(f"**Matched Additional Skills:** {', '.join(additional_matches)}")

    st.write(f"### CV Score: **{total_score:.2f} / 100**")

    # Feedback Based on Score
    if total_score >= 80:
        st.success("Your CV is highly compatible with the job requirements!")
    elif 50 <= total_score < 80:
        st.warning("Your CV is moderately compatible. Consider improving your skills.")
    else:
        st.error("Your CV has low compatibility. You may need to acquire more relevant skills.")