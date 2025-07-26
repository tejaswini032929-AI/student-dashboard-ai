import streamlit as st
import pandas as pd
from openai import OpenAI

# Set page config
st.set_page_config(page_title="Student Performance Dashboard + 🤖 AI Insights")

# Sidebar - OpenAI API key
st.sidebar.markdown("🔐 **Enter OpenAI API Key**")
api_key = st.sidebar.text_input("API Key", type="password")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("StudentsPerformance.csv")

df = load_data()

# Title
st.title("📊 Student Performance Dashboard + 🤖 AI Insights")

# Dataset preview
st.subheader("📂 Dataset Preview")
st.dataframe(df.tail(10), use_container_width=True)

# AI Insights section
st.subheader("💡 Ask AI about the data")
user_query = st.text_area("What would you like to know?")

if st.button("Ask AI") and api_key and user_query:
    with st.spinner("Getting insights..."):

        try:
            client = OpenAI(api_key=api_key)

            # Format system + user messages
            prompt = (
                f"You are a data expert. Analyze this dataframe and answer user queries.\n\n"
                f"Data preview:\n{df.head(10).to_csv(index=False)}\n\n"
                f"User question: {user_query}"
            )

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You're a data analyst assistant."},
                    {"role": "user", "content": prompt}
                ]
            )

            ai_reply = response.choices[0].message.content
            st.success("AI Answer:")
            st.write(ai_reply)

        except Exception as e:
            st.error(f"⚠️ Error: {e}")

elif st.button("Ask AI") and not api_key:
    st.warning("🔑 Please enter your OpenAI API key.")


