
import streamlit as st
import pandas as pd
import openai
import os

# Load dataset
df = pd.read_csv("students_performance_200.csv")

# Page config
st.set_page_config(page_title="AI Student Dashboard", layout="wide")
st.title("📊 Student Performance Dashboard + 🤖 AI Insights")

# Sidebar - OpenAI API key input
st.sidebar.subheader("🔐 Enter OpenAI API Key")
openai_api_key = st.sidebar.text_input("API Key", type="password")

# Display dataset preview
st.subheader("📁 Dataset Preview")
st.dataframe(df, use_container_width=True)

# Basic stats
st.subheader("📈 Quick Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("Average Math Score", round(df["math score"].mean(), 2))
col2.metric("Average Reading Score", round(df["reading score"].mean(), 2))
col3.metric("Average Writing Score", round(df["writing score"].mean(), 2))

# Optional: Plotting
st.subheader("📊 Score Distribution")
selected_score = st.selectbox("Choose a subject", ["math score", "reading score", "writing score"])
st.bar_chart(df[selected_score])

# AI-powered question box
st.subheader("🤖 Ask AI about the Dataset")

if openai_api_key:
    openai.api_key = openai_api_key
    question = st.text_area("What would you like to know?", placeholder="E.g., What's the average score for students who completed the test preparation course?")

    if st.button("Ask AI"):
        with st.spinner("Thinking..."):
            # Convert DataFrame to CSV string (shortened version for input)
            csv_snippet = df.head(50).to_csv(index=False)
            prompt = f"""
You are a data analyst assistant. Here's the dataset snippet:

{csv_snippet}

Answer this question about the dataset:
{question}
"""
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful data analysis assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5,
                    max_tokens=500
                )
                st.success(response['choices'][0]['message']['content'])
            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.info("Enter your OpenAI API key in the sidebar to enable AI-powered analysis.")
