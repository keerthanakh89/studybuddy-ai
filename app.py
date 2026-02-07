# 1. Import required libraries
import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# 2. Page settings
st.set_page_config(page_title="StudyBuddy AI", layout="centered")

# 3. App title and description
st.title("📘 StudyBuddy AI – Structured Learning Explainer")
st.write("Upload study content and get a simple, step-by-step explanation.")

# 4. Get Gemini API key from Streamlit Secrets
api_key = os.getenv("GEMINI_API_KEY")

if api_key is None:
    st.error("API key not found. Please add GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

# 5. Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# 6. User inputs
level = st.selectbox(
    "Select learning level",
    ["Class 6", "Class 10", "Beginner College"]
)

uploaded_file = st.file_uploader(
    "Upload textbook page / exam question / handwritten notes",
    type=["jpg", "jpeg", "png"]
)

text_input = st.text_area("OR paste your question here")

# 7. Button logic
if st.button("Explain"):
    if uploaded_file or text_input.strip() != "":
        with st.spinner("Explaining in simple language..."):

            prompt = f"""
You are an expert teacher.

Explain the given content for a {level} student.

Rules:
- Use very simple language
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
                st.error("Something went wrong while generating explanation.")
    else:
        st.warning("Please upload an image or enter text.")
