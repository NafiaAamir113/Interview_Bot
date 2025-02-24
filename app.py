import streamlit as st
from together import Together
import os

# Load API key from Streamlit secrets
TOGETHER_API_KEY = st.secrets["TOGETHER_API_KEY"]
client = Together(api_key=TOGETHER_API_KEY)

# Function to generate interview questions
def generate_questions(domain):
    """Generates industry-standard interview questions for the given job role."""
    messages = [
        {"role": "system", "content": "You are an expert in conducting interviews."},
        {"role": "user", "content": f"Generate a list of 10 industry-standard interview questions for a {domain} position."}
    ]

    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=messages,
        max_tokens=500,
        temperature=0.7,
        top_p=0.7,
        top_k=50,
        repetition_penalty=1,
        stop=["<|eot_id|>", "<|eom_id|>"],
    )

    return response.choices[0].message.content.strip()

# Streamlit UI
st.title("🧠 AI Interview Question Generator")
st.write("Generate professional interview questions based on industry standards.")

# User Input
domain = st.text_input("Enter the job role (e.g., Data Analyst, Software Engineer)")

if st.button("Generate Questions"):
    if domain:
        with st.spinner("Generating questions..."):
            questions = generate_questions(domain)
            st.subheader(f"📌 Questions for {domain}:")
            st.write(questions)
    else:
        st.warning("Please enter a job role.")
