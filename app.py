import streamlit as st
import google.generativeai as genai
import os
import PyPDF2

# Set your Gemini API key
GEMINI_API_KEY = "AIzaSyAKT9cbkUVqKjN8o5SwMY9Bf1X4-QOlkKw"
genai.configure(api_key=GEMINI_API_KEY)

# Load Gemini model
model = genai.GenerativeModel("models/gemini-pro")

# Function to summarize text using Gemini
def summarize(text):
    prompt = f"Summarize this document in no more than 150 words:\n\n{text[:3000]}"
    response = model.generate_content(prompt)
    return response.text

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

# Streamlit UI
st.set_page_config(page_title="GenAI Document Assistant")
st.title("📄 GenAI Document Assistant")
st.markdown("Upload **PDF** or **TXT** file to get a summary.")

uploaded_file = st.file_uploader("Upload File", type=["pdf", "txt"])

if uploaded_file is not None:
    st.success("✅ File uploaded successfully!")
    if uploaded_file.type == "application/pdf":
        document_text = extract_text_from_pdf(uploaded_file)
    else:
        document_text = uploaded_file.read().decode("utf-8")

    if st.button("Summarize"):
        with st.spinner("Summarizing..."):
            try:
                summary = summarize(document_text)
                st.subheader("📌 Summary")
                st.write(summary)
            except Exception as e:
                st.error(f"❌ Error: {e}")
