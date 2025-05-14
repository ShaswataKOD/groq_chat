import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# ---------- LOAD ENV or STREAMLIT SECRETS ----------
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")

# ---------- Streamlit Page Config ----------
st.set_page_config(page_title="Groq ProBot – Your Formal AI Assistant", layout="centered")

# ---------- Exit if API Key is Missing ----------
if not groq_api_key:
    st.error("🚨 Please set the GROQ_API_KEY in your .env or Streamlit secrets.")
    st.stop()

# ---------- DARK STYLING + AVATAR SUPPORT ----------
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
        background-color: #0f1117;
        color: #e1e1e6;
    }

    h1 {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(to right, #3a0ca3, #4361ee);
        border-radius: 12px;
        box-shadow: 0 0 15px rgba(67, 97, 238, 0.4);
        margin-bottom: 2rem;
        color: #ffffff;
    }

    .chat-container {
        display: flex;
        flex-direction: column;
    }

    .message {
        display: flex;
        margin-bottom: 1rem;
        max-width: 100%;
    }

    .avatar {
        font-size: 28px;
        margin-right: 0.75rem;
        margin-top: 0.2rem;
    }

    .bubble-user {
        background: linear-gradient(to right, #3f37c9, #4895ef);
        color: white;
        padding: 0.9rem 1.2rem;
        border-radius: 12px;
        font-size: 16px;
        box-shadow: 0 0 10px rgba(72, 149, 239, 0.3);
        max-width: 80%;
    }

    .bubble-ai {
        background-color: #1f1f2e;
        color: #e1e1e6;
        padding: 0.9rem 1.2rem;
        border-radius: 12px;
        font-size: 16px;
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.05);
        max-width: 80%;
    }

    .stTextInput input {
        background-color: #1c1e26;
        color: #e1e1e6;
        border: 1px solid #333;
        border-radius: 10px;
        padding: 0.6rem;
        font-size: 16px;
    }

    .stTextInput input:focus {
        border-color: #4895ef;
        box-shadow: 0 0 0 0.2rem rgba(72, 149, 239, 0.25);
    }

    .stButton button {
        background-color: #4895ef;
        color: white;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        font-size: 16px;
        border: none;
        transition: all 0.2s ease;
        margin-top: 0.5rem;
    }

    .stButton button:hover {
        background-color: #4361ee;
        transform: scale(1.03);
    }

    hr {
        border-top: 1px solid #333;
    }

    a {
        color: #91cfff;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("## 🤖 Groq ProBot – Your Formal AI Assistant")

# ---------- Init Session State ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------- Init Chat ----------
try:
    chat = ChatGroq(temperature=0.7, model="llama3-8b-8192", groq_api_key=groq_api_key)
except Exception as e:
    st.error(f"❌ Error initializing ChatGroq: {e}")
    st.stop()

# ---------- Add system prompt for professional tone ----------
if not any(isinstance(msg, SystemMessage) for msg in st.session_state.chat_history):
    st.session_state.chat_history.insert(0,
        SystemMessage(content="You are a professional and courteous AI assistant. Always respond in a clear, formal, and business-like tone.")
    )

# ---------- Display Chat History ----------
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.chat_history:
    if isinstance(msg, HumanMessage):
        st.markdown(f"""
        <div class="message" style="justify-content: flex-end;">
            <div class="bubble-user">{msg.content}</div>
            <div class="avatar">🧑</div>
        </div>
        """, unsafe_allow_html=True)
    elif isinstance(msg, AIMessage):
        st.markdown(f"""
        <div class="message" style="justify-content: flex-start;">
            <div class="avatar">🤖</div>
            <div class="bubble-ai">{msg.content}</div>
        </div>
        """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------- Chat Input + Send Button ----------
with st.form(key=f"form_{len(st.session_state.chat_history)}", clear_on_submit=True):
    user_input = st.text_input("💬", placeholder="Type your message here...")
    send = st.form_submit_button("Send")

    if send and user_input.strip():
        st.session_state.chat_history.append(HumanMessage(content=user_input))
        try:
            response = chat.invoke(st.session_state.chat_history)
            st.session_state.chat_history.append(AIMessage(content=response.content))
            st.redisplay()  # Updated line to refresh the chat
        except Exception as e:
            st.error(f"⚠️ Error: {e}")
    elif send:
        st.warning("⚠️ Message can't be empty!")

# ---------- Footer ----------
st.markdown("---")
st.markdown("Made with ❤️ using [Streamlit](https://streamlit.io) and [Groq](https://groq.com) 🚀")
