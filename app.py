import streamlit as st
import os
from src.engine import NyayaEngine

# Page Config
st.set_page_config(page_title="NyayaAI", page_icon="⚖️", layout="centered")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    .main { background-color: #f5f7f9; }
    </style>
    """, unsafe_allow_html=True) # Correct parameter name

st.title("⚖️ NyayaAI: Citizen's Constitutional Guide")
st.caption("Empowering Indian citizens with legal knowledge through AI")

# Initialize Engine (Cached)
@st.cache_resource
def load_nyaya_engine():
    engine = NyayaEngine()
    pdf_path = "data/constitution.pdf"
    if os.path.exists(pdf_path):
        with st.spinner("Indexing the Constitution for the first time..."):
            engine.ingest_data(pdf_path)
    return engine

try:
    engine = load_nyaya_engine()
except Exception as e:
    st.error(f"Error initializing system: {e}")
    st.stop()

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Explain your problem (e.g., 'My boss is not paying me')"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing legal context..."):
            answer = engine.get_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

# Sidebar
with st.sidebar:
    st.header("About NyayaAI")
    st.write("This tool uses the Indian Constitution to help you identify your rights in daily scenarios like:")
    st.markdown("- Unpaid Wages\n- Police Misconduct\n- Discrimination\n- Right to Education")
    st.divider()
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()