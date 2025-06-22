
import streamlit as st
from PyPDF2 import PdfReader
import docx2txt
import pandas as pd
import io

st.set_page_config(page_title="Resume Filter Tool – Om Jawale")
st.title("📄 Resume Filter Tool – Created by Om Jawale")
st.markdown("Upload resumes (PDF, DOCX, or TXT) and filter them by keywords (e.g., Python, 3 years)")

def extract_text(file):
    if file.type == "application/pdf":
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text.lower()
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return docx2txt.process(file).lower()
    elif file.type == "text/plain":
        return str(file.read().decode("utf-8")).lower()
    return ""

keywords = st.text_input("Enter keywords (comma separated)", "python, 3 years")
uploaded_files = st.file_uploader("Upload Resumes", type=["pdf", "docx", "txt"], accept_multiple_files=True)

if st.button("🔍 Filter Resumes"):
    if not uploaded_files:
        st.warning("Please upload at least one resume.")
    else:
        keyword_list = [k.strip().lower() for k in keywords.split(",")]
        results = []

        for file in uploaded_files:
            text = extract_text(file)
            if not text:
                continue
            match_count = sum(1 for k in keyword_list if k in text)
            match_percent = round((match_count / len(keyword_list)) * 100, 2)
            results.append({
                "Filename": file.name,
                "Match %": match_percent
            })

        df = pd.DataFrame(results).sort_values(by="Match %", ascending=False)
        st.dataframe(df)

        if not df.empty:
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
                df.to_excel(writer, index=False)
            st.download_button("📥 Download Results as Excel", data=buffer.getvalue(), file_name="matched_resumes.xlsx", mime="application/vnd.ms-excel")
        else:
            st.error("No resumes processed.")

st.markdown("---")
st.markdown("© 2025 **Om Jawale** – All rights reserved.")
