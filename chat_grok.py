import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage

# ---------- LOAD ENV or STREAMLIT SECRETS ----------
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")

# ---------- Streamlit Page Config ----------
st.set_page_config(page_title="Groq Chatbot", layout="centered")

# ---------- Exit if API Key is Missing ----------
if not groq_api_key:
    st.error("🚨 Please set the GROQ_API_KEY in your .env or Streamlit secrets.")
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

    .stTextInput input {
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

# ---------- Model Selection ----------
model_name = st.selectbox("🔧 Choose Groq Model", ["llama3-8b-8192", "qwen-2.5-32b"])

# ---------- Init Session State ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------- Init Chat ----------
try:
    chat = ChatGroq(temperature=0.7, model=model_name, groq_api_key=groq_api_key)
except Exception as e:
    st.error(f"❌ Error initializing ChatGroq: {e}")
    st.stop()

# ---------- Chat Input ----------
user_input = st.text_input("💬 Your message:", key="user_input", placeholder="Ask me anything...")

# ---------- Send Message ----------
if st.button("🚀 Send"):
    if user_input.strip():
        # Add user message to history
        st.session_state.chat_history.append(HumanMessage(content=user_input))

        try:
            # Invoke with full conversation history
            response = chat.invoke(st.session_state.chat_history)

            # Add AI response to history
            st.session_state.chat_history.append(AIMessage(content=response.content))
        except Exception as e:
            st.error(f"⚠️ Error: {e}")
    else:
        st.warning("⚠️ Please enter a message.")

# ---------- Display Chat History ----------
for msg in st.session_state.chat_history:
    if isinstance(msg, HumanMessage):
        st.markdown(f"<div class='message-user'><strong>You:</strong> {msg.content}</div>", unsafe_allow_html=True)
    elif isinstance(msg, AIMessage):
        st.markdown(f"<div class='message-ai'><strong>Groq:</strong> {msg.content}</div>", unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown("---")
st.markdown("Made with ❤️ using [Streamlit](https://streamlit.io) and [Groq](https://groq.com) 🚀")
