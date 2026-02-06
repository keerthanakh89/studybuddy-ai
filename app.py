import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

st.set_page_config(page_title="StudyBuddy AI", layout="centered")

st.title("📘 StudyBuddy AI – Structured Learning Explainer")
st.write("Upload study content and get a simple, step-by-step explanation.")

# Load API key
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

level = st.selectbox(
    "Select learning level",
    ["Class 6", "Class 10", "Beginner College"]
)

uploaded_file = st.file_uploader(
    "Upload textbook page / exam question / handwritten notes",
    type=["png", "jpg", "jpeg"]
)

text_input = st.text_area("Or paste your question/text here")

if st.button("Explain"):
    if uploaded_file or text_input:
        with st.spinner("Thinking like a teacher..."):
            prompt = f"""
You are an expert teacher.

Explain the content for a {level} student.

Instructions:
- Use simple language
- Explain step-by-step
- Highlight key concepts
- Mention common mistakes
- End with a short summary
"""

            if uploaded_file:
                image = Image.open(uploaded_file)
                response = model.generate_content([prompt, image])
            else:
                response = model.generate_content(prompt + text_input)

            st.subheader("📖 Explanation")
            st.write(response.text)
    else:
        st.warning("Please upload an image or enter text.")

