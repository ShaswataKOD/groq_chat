import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables from .env file
load_dotenv()

# Fetch the API key from environment
groq_api_key = os.getenv("GROQ_API_KEY")

# Show error if API key is not set
if not groq_api_key:
    st.error("Please set the GROQ_API_KEY environment variable.")
    st.stop()

# Streamlit app UI
st.header("💬 Chat with Groq")

# Model selection dropdown
model_name = st.selectbox("Select Groq Model", ["llama3-8b-8192", "qwen-2.5-32b"])

# Initialize ChatGrok
try:
    chat = ChatGroq(temperature=0.7, model=model_name, groq_api_key=groq_api_key)
except Exception as e:
    st.error(f"Error initializing ChatGroq: {e}")
    st.stop()

# Text input for user query
user_input = st.text_area("Enter your message:", height=200)

# Button to send query
if st.button("Ask"):
    if user_input.strip():
        try:
            response = chat.invoke(user_input)
            st.write(response.content)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a question.")
