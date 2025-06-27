import streamlit as st
from resume_parser import extract_text_from_pdf
from matching import rank_resumes

# Custom CSS Styling
st.markdown("""
    <style>
    body {
        font-family: 'Segoe UI', sans-serif;
    }
    .main {
        background-color: #f9fbff;
    }
    h1 {
        color: #2e4057;
        font-size: 36px;
        text-align: center;
        margin-bottom: 20px;
    }
    .stTextArea textarea {
        font-size: 16px !important;
        font-family: 'Segoe UI', sans-serif !important;
        border-radius: 10px !important;
        padding: 12px !important;
    }
    .stFileUploader {
        border: 2px dashed #ccc;
        border-radius: 10px;
        padding: 10px;
        background-color: #f2f8ff;
    }
    .stFileUploader label {
        font-weight: bold;
        font-size: 16px;
        color: #2e4057;
    }
    .stButton button {
        background: linear-gradient(90deg, #a1c4fd 0%, #c2e9fb 100%);
        color: black;
        border-radius: 10px;
        font-size: 18px;
        font-weight: bold;
        padding: 0.6em 2em;
        transition: all 0.3s ease-in-out;
        border: none;
    }
    .stDownloadButton {
        color: black;
        border-radius: 10px;
        font-size: 18px;
        font-weight: bold;
        padding: 0.6em 2em;
        transition: all 0.3s ease-in-out;
        border: none;
    .stButton button:hover {
        background: linear-gradient(90deg, #89f7fe 0%, #66a6ff 100%);
        transform: scale(1.05);
        color: white;
    }
    .center-button {
        display: flex;
        justify-content: center;
        margin-top: 25px;
        margin-bottom: 10px;
    }
    .styled-box {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
    }
    /* Wider sidebar */
    section[data-testid="stSidebar"] {
        min-width: 340px !important;
        max-width: 360px !important;
        background: linear-gradient(to bottom right, #fdfbfb, #ebedee);
        padding: 25px 20px 20px 20px;
        font-family: 'Segoe UI', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# App title (centered)
st.markdown("""
<div style='text-align: center;'>
    <h1>📄 SmartScreenHR</h1>
</div>
""", unsafe_allow_html=True)

# Sidebar: Upload Resumes
with st.sidebar:
    st.header("📥 Upload Panel")
    uploaded_files = st.file_uploader("📁 Upload Resumes (PDFs Only)", type="pdf", accept_multiple_files=True)

# Main: Job Description Input
st.subheader("📝 Enter Job Description")
job_desc = st.text_area("", height=200)

# Score Interpretation Guide
st.markdown("""
<div style="
    padding: 10px 5px;
    border-radius: 0px;
    color: #2e2e2e;
    font-size: 16px;
    font-family: 'Segoe UI', sans-serif;">
    
<h3 style="color:#2e4057;">Marking Scores</h3>
<ul>
    <li><b>0.00 – 0.19</b>: ❌ <i>Poor match</i></li>
    <li><b>0.20 – 0.39</b>: ⚠️ <i>Average match</i></li>
    <li><b>0.40 – 0.59</b>: ✅ <i>Good match</i></li>
    <li><b>0.60 – 1.00</b>: 🌟 <i>Excellent match</i></li>
</ul>
</div>
""", unsafe_allow_html=True)


# Main: Centered Button
st.markdown('<div class="center-button">', unsafe_allow_html=True)
rank_clicked = st.button("✨ Rank Resumes")
st.markdown('</div>', unsafe_allow_html=True)

# Processing and Results
if rank_clicked:
    if not job_desc.strip():
        st.warning("Please enter a job description.")
    elif not uploaded_files:
        st.warning("Please upload at least one resume.")
    else:
        resume_texts = []
        filenames = []

        for file in uploaded_files:
            text = extract_text_from_pdf(file)
            resume_texts.append(text)
            filenames.append(file.name)

        results = rank_resumes(job_desc, resume_texts, filenames)

        st.success("✅ Ranking completed!")

        # Results section
        st.markdown('<div class="styled-box">', unsafe_allow_html=True)
        st.markdown("### 📊 Ranked Candidate Results")
        st.dataframe(results, use_container_width=True)

        csv = results.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download Results as CSV", csv, "ranked_resumes.csv", "text/csv")
        st.markdown('</div>', unsafe_allow_html=True)
