# import streamlit as st
# import spacy
# import io
# import os
# from pdfminer3.layout import LAParams
# from pdfminer3.pdfpage import PDFPage
# from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
# from pdfminer3.converter import TextConverter
# import base64

# # Load the custom spaCy model (ganti path dengan path model spaCy Anda)
# nlp = spacy.load("models")

# # Buat folder Upload Resume jika belum ada
# if not os.path.exists('./Uploaded_Resumes'):
#     os.makedirs('./Uploaded_Resumes')

# # Function to read PDF and extract text
# def pdf_reader(file):
#     resource_manager = PDFResourceManager()
#     fake_file_handle = io.StringIO()
#     converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
#     page_interpreter = PDFPageInterpreter(resource_manager, converter)
#     with open(file, 'rb') as fh:
#         for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
#             page_interpreter.process_page(page)
#         text = fake_file_handle.getvalue()

#     converter.close()
#     fake_file_handle.close()
#     return text

# # Streamlit app for CV upload and scoring
# st.set_page_config(page_title="CV Quality Scorer", page_icon='📄')
# st.title("CV Quality Scorer with spaCy Analysis")

# # Upload CV file
# pdf_file = st.file_uploader("Upload your CV (PDF format only)", type=["pdf"])

# if pdf_file is not None:
#     save_path = f'./Uploaded_Resumes/{pdf_file.name}'
#     with open(save_path, "wb") as f:
#         f.write(pdf_file.getbuffer())

#     # Display the uploaded CV
#     with open(save_path, "rb") as f:
#         base64_pdf = base64.b64encode(f.read()).decode('utf-8')
#         pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
#         st.markdown(pdf_display, unsafe_allow_html=True)

#     # Extract text from the CV
#     resume_text = pdf_reader(save_path)

#     # Analyze the resume using spaCy
#     doc = nlp(resume_text)
#     detected_position = [ent.text for ent in doc.ents if ent.label_ == 'JOB_CATEGORY']
#     detected_skills = [ent.text for ent in doc.ents if ent.label_ == 'SKILL']
#     detected_experiences = [ent.text for ent in doc.ents if ent.label_ == 'EXPERIENCE']
#     detected_projects = [ent.text for ent in doc.ents if ent.label_ == 'PROJECT']
#     detected_achievements = [ent.text for ent in doc.ents if ent.label_ == 'ACHIEVEMENT']

#     # Display the extracted details
#     st.subheader("Detected Job Position")
#     st.write(f"Position: {', '.join(detected_position) if detected_position else 'No job position detected'}")

#     st.subheader("Detected Skills")
#     st.write(f"Skills: {', '.join(detected_skills) if detected_skills else 'No skills detected'}")

#     st.subheader("Detected Work Experience")
#     st.write(f"Experiences: {', '.join(detected_experiences) if detected_experiences else 'No experiences detected'}")

#     st.subheader("Detected Projects")
#     st.write(f"Projects: {', '.join(detected_projects) if detected_projects else 'No projects detected'}")

#     st.subheader("Detected Achievements")
#     st.write(f"Achievements: {', '.join(detected_achievements) if detected_achievements else 'No achievements detected'}")

#     # Define a sample job category and required attributes
#     job_category = 'Programmer'
#     required_skills = ['Python', 'SQL', 'JavaScript', 'Version Control', 'Problem Solving']
#     required_experience = ['Software Development', 'Web Development']
#     required_projects = ['Web Application', 'Automation Script']
#     required_achievements = ['Certification', 'Award']

#     # Calculate scores
#     skill_score = len([skill for skill in detected_skills if skill in required_skills]) / len(required_skills) * 100
#     experience_score = len([exp for exp in detected_experiences if exp in required_experience]) / len(required_experience) * 100
#     project_score = len([proj for proj in detected_projects if proj in required_projects]) / len(required_projects) * 100
#     achievement_score = len([ach for ach in detected_achievements if ach in required_achievements]) / len(required_achievements) * 100

#     total_score = (skill_score + experience_score + project_score + achievement_score) / 4

#     # Display score
#     st.subheader("CV Score")
#     st.markdown(f"**Overall CV Score for the position '{job_category}': {total_score:.2f} / 100**")
#     st.write(f"Skill Score: {skill_score:.2f}%, Experience Score: {experience_score:.2f}%, Project Score: {project_score:.2f}%, Achievement Score: {achievement_score:.2f}%")

import os
import streamlit as st
import spacy
import io
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter
import base64

# Pastikan folder untuk menyimpan file ada
if not os.path.exists('./Uploaded_Resumes'):
    os.makedirs('./Uploaded_Resumes')

# Load the custom spaCy model
nlp = spacy.load("models")  # Ganti dengan path model Anda

# Function to read PDF and extract text
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

# Streamlit app for CV upload and scoring
st.set_page_config(page_title="CV Skill Categorizer and Scorer", page_icon='📄')
st.title("CV Skill Categorizer and Scorer")

# Upload CV file
pdf_file = st.file_uploader("Upload your CV (PDF format only)", type=["pdf"])

if pdf_file is not None:
    save_path = f'./Uploaded_Resumes/{pdf_file.name}'
    with open(save_path, "wb") as f:
        f.write(pdf_file.getbuffer())

    # Display the uploaded CV
    with open(save_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

    # Extract text from the CV
    resume_text = pdf_reader(save_path)

    # Analyze the resume using spaCy
    doc = nlp(resume_text)
    detected_categories = [ent.text for ent in doc.ents if ent.label_ == 'JOB_CATEGORY']
    detected_skills = [ent.text for ent in doc.ents if ent.label_ == 'SKILL']

    # Display the detected job categories and skills
    st.subheader("Detected Job Categories")
    st.write(f"Categories: {', '.join(detected_categories) if detected_categories else 'No job category detected'}")

    st.subheader("Detected Skills")
    st.write(f"Skills: {', '.join(detected_skills) if detected_skills else 'No skills detected'}")

    # Define skill requirements for job categories
    job_requirements = {
        'Data Scientist': ['Python', 'Machine Learning', 'Data Analysis', 'SQL'],
        'Web Developer': ['JavaScript', 'HTML', 'CSS', 'React', 'Node.js'],
        'Software Engineer': ['Python', 'Java', 'C++', 'Problem Solving'],
        # Tambahkan kategori lain sesuai kebutuhan
    }

    # Score calculation
    scores = {}
    for category in detected_categories:
        if category in job_requirements:
            required_skills = job_requirements[category]
            matching_skills = [skill for skill in detected_skills if skill in required_skills]
            score = len(matching_skills) / len(required_skills) * 100
            scores[category] = score

    # Display score results
    st.subheader("CV Score by Job Category")
    if scores:
        for category, score in scores.items():
            st.write(f"**{category}**: {score:.2f}%")
    else:
        st.write("No matching job category found or no skills matched.")
