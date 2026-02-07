import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# Page configuration
st.set_page_config(page_title="StudyBuddy AI", layout="centered")

# Title
st.title("📘 StudyBuddy AI – Structured Learning Explainer")
st.write("Upload study content and get a simple, step-by-step explanation.")

# Load API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("GEMINI_API_KEY not found. Please add it in Streamlit Secrets.")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

# User inputs
level = st.selectbox(
    "Select learning level",
    ["Class 6", "Class 10", "Beginner College"]
)

uploaded_file = st.file_uploader(
    "Upload textbook page / exam question / handwritten notes",
    type=["jpg", "jpeg", "png"]
)

text_input = st.text_area("OR paste your question here")

# Button logic
if st.button("Explain"):
    if uploaded_file or text_input.strip():
        with st.spinner("Explaining..."):
            prompt = f"""
You are an expert teacher.

Explain the given content for a {level} student.

Rules:
- Use simple language
- Explain step by step
- Highlight key points
- End with a short summary
"""

            try:
                if uploaded_file:
                    image = Image.open(uploaded_file)
                    response = model.generate_content([prompt, image])
                else:
                    response = model.generate_content(prompt + "\n\n" + text_input)

                st.subheader("📖 Explanation")
                st.write(response.text)

            except Exception as e:
                st.error("Gemini error:")
                st.error(str(e))
    else:
        st.warning("Please upload an image or enter text.")
