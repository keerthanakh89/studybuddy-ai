if st.button("Explain"):
    if uploaded_file or text_input.strip() != "":
        with st.spinner("Thinking like a teacher..."):

            base_prompt = f"""
You are an expert teacher.

Explain the following content for a {level} student.

Instructions:
- Use simple language
- Explain step-by-step
- Highlight key concepts
- Mention common mistakes
- End with a short summary
"""

            try:
                if uploaded_file:
                    image = Image.open(uploaded_file)
                    response = model.generate_content(
                        [base_prompt, image]
                    )
                else:
                    response = model.generate_content(
                        base_prompt + "\n\n" + text_input
                    )

                st.subheader("📖 Explanation")
                st.write(response.text)

            except Exception as e:
                st.error("Something went wrong while generating the explanation.")
                st.error(str(e))
    else:
        st.warning("Please upload an image or enter text.")
