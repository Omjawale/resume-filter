
import streamlit as st
from PyPDF2 import PdfReader

def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.lower()

st.title("Resume Filter Tool")

keywords = st.text_input("Enter keywords (comma separated)", "python, 3 years")
uploaded_files = st.file_uploader("Upload Resumes (PDF)", type="pdf", accept_multiple_files=True)

if st.button("Filter Resumes"):
    if not uploaded_files:
        st.warning("Please upload at least one PDF.")
    else:
        keyword_list = [k.strip().lower() for k in keywords.split(",")]
        matched = []
        for file in uploaded_files:
            text = extract_text_from_pdf(file)
            if all(k in text for k in keyword_list):
                matched.append(file.name)
        if matched:
            st.success(f"Matching Resumes: {', '.join(matched)}")
        else:
            st.error("No resumes matched all keywords.")
