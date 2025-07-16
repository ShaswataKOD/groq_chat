import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# ---------- Load Environment Variables ----------
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")

# ---------- Streamlit Page Config ----------
st.set_page_config(page_title="CodeBot – Groq-Powered Code Assistant", layout="centered")

# ---------- Exit if API Key is Missing ----------
if not groq_api_key:
    st.error("🚨 Please set the GROQ_API_KEY in your .env or Streamlit secrets.")
    st.stop()

# ---------- Utility: Simple Code Intent Filter ----------
def is_code_related(query: str) -> bool:
    keywords = [
        "code", "function", "write a", "build a", "create a", "python", "java",
        "c++", "javascript", "html", "sql", "algorithm", "data structure",
        "class", "script", "loop", "array", "object", "bug", "error", "fix"
    ]
    return any(kw in query.lower() for kw in keywords)

# ---------- Init ChatBot ----------
try:
    chat = ChatGroq(
        temperature=0.3,
        model="llama3-8b-8192",
        groq_api_key=groq_api_key
    )
except Exception as e:
    st.error(f"❌ Error initializing ChatGroq: {e}")
    st.stop()

# ---------- Init Session State ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------- System Prompt: Code-Only Assistant ----------
if not any(isinstance(msg, SystemMessage) for msg in st.session_state.chat_history):
    st.session_state.chat_history.insert(0, SystemMessage(
        content="You are a strict coding assistant. Only respond to programming-related queries and generate code. For any other topics, respond with: '⚠️ I'm a coding assistant and can only respond to programming-related questions.'"
    ))

# ---------- Chat Display Styling ----------
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
        background-color: #0f1117;
        color: #e1e1e6;
    }
    .chat-container { display: flex; flex-direction: column; }
    .message { display: flex; margin-bottom: 1rem; max-width: 100%; }
    .avatar { font-size: 28px; margin-right: 0.75rem; margin-top: 0.2rem; }
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
    </style>
""", unsafe_allow_html=True)

# ---------- Title ----------
st.markdown("## 💻 CodeBot – Groq-Powered Coding Assistant")

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

# ---------- Input Form ----------
with st.form(key=f"form_{len(st.session_state.chat_history)}", clear_on_submit=True):
    user_input = st.text_input("💬", placeholder="Ask me to write code...")
    send = st.form_submit_button("Send")

    if send and user_input.strip():
        st.session_state.chat_history.append(HumanMessage(content=user_input))

        if is_code_related(user_input):
            try:
                response = chat.invoke(st.session_state.chat_history)
                st.session_state.chat_history.append(AIMessage(content=response.content))
            except Exception as e:
                st.error(f"⚠️ Error: {e}")
        else:
            msg = "⚠️ I'm a coding assistant and can only respond to programming-related questions."
            st.session_state.chat_history.append(AIMessage(content=msg))

    elif send:
        st.warning("⚠️ Message can't be empty!")

# ---------- Footer ----------
st.markdown("---")
st.markdown("Made for devs. Ask only programming stuff! 🧠")
st.mardown("Please Press 'Send' Button twice to get your response")