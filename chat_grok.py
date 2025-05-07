import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Streamlit page config
st.set_page_config(page_title="Groq Chatbot", layout="centered")

# Exit if API key missing
if not groq_api_key:
    st.error("🚨 Please set the GROQ_API_KEY in your .env file.")
    st.stop()

# ---------- STYLING ----------
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
    }

    h1 {
        color: #ffffff;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(to right, #5e60ce, #48bfe3);
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    .stTextArea textarea {
        font-size: 16px;
        border-radius: 10px;
    }

    .message-user {
        background-color: #dff7df;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
        font-size: 16px;
    }

    .message-ai {
        background-color: #f0f4ff;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
        font-size: 16px;
        color: #333333;
    }

    .stButton button {
        background-color: #4361ee;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        font-size: 16px;
        transition: 0.2s ease;
    }

    .stButton button:hover {
        background-color: #3a0ca3;
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("## 🤖 Groq-Powered Chat Assistant")

# ---------- MODEL SELECTION ----------
model_name = st.selectbox("🔧 Choose Groq Model", ["llama3-8b-8192", "qwen-2.5-32b"])

# ---------- Init Chat ----------
try:
    chat = ChatGroq(temperature=0.7, model=model_name, groq_api_key=groq_api_key)
except Exception as e:
    st.error(f"❌ Error initializing ChatGroq: {e}")
    st.stop()

# ---------- USER INPUT ----------
user_input = st.text_area("💬 Type your question:", placeholder="e.g. Tell me a joke, or explain a concept", height=150)

# ---------- BUTTON + OUTPUT ----------
if st.button("🚀 Send"):
    if user_input.strip():
        st.markdown(f"<div class='message-user'><strong>You:</strong> {user_input}</div>", unsafe_allow_html=True)
        try:
            response = chat.invoke(user_input)
            st.markdown(f"<div class='message-ai'><strong>Groq:</strong> {response.content}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"⚠️ Error: {e}")
    else:
        st.warning("⚠️ Please enter a message to ask.")

# ---------- FOOTER ----------
st.markdown("---")
st.markdown("Made with ❤️ using [Streamlit](https://streamlit.io) and [Groq](https://groq.com) 🚀")
