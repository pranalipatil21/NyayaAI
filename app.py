import streamlit as st
import os
from src.engine import NyayaEngine

# Page Config
st.set_page_config(page_title="NyayaAI", page_icon="⚖️", layout="centered")

# Custom CSS for modern premium legal theme
st.markdown("""
    <style>
    /* Import Google Fonts for elegant typography */
    @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400..700;1,400..700&family=Playfair+Display:ital,wght@0,400..900;1,400..900&family=Inter:wght@300;400;500;600&display=swap');

    /* Global Body Styles */
    .stApp {
        background-color: #FAF7F2 !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Force all base text inside main app to be dark for high-contrast readability */
    .stApp p, .stApp span, .stApp li, .stApp label, .stApp div[data-testid="stMarkdownContainer"] {
        color: #1E1E1C !important;
    }

    /* Headings styling */
    h1, h2, h3, .legal-header {
        font-family: 'Playfair Display', serif !important;
        color: #1E1E1C !important;
        font-weight: 700 !important;
    }

    /* Top Hero Header Design */
    .hero-container {
        text-align: center;
        padding: 30px 15px;
        background-color: #FAF7F2;
        border-bottom: 2px solid #B89C72;
        margin-bottom: 25px;
    }

    .hero-title {
        font-family: 'Playfair Display', serif !important;
        font-size: 2.8rem !important;
        color: #1E1E1C !important;
        margin-bottom: 5px;
        letter-spacing: 1.5px;
        font-weight: 800 !important;
    }

    .hero-tagline {
        font-family: 'Lora', serif !important;
        font-size: 1.1rem !important;
        color: #B89C72 !important;
        font-style: italic;
        margin-bottom: 10px;
        letter-spacing: 0.5px;
    }

    .hero-divider {
        height: 1px;
        width: 120px;
        background-color: #B89C72;
        margin: 12px auto;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #F3EFE9 !important;
        border-right: 1px solid #E6DEC1 !important;
    }

    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        font-family: 'Playfair Display', serif !important;
        color: #1E1E1C !important;
    }

    /* Force all text in Sidebar to be dark and readable */
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] li,
    section[data-testid="stSidebar"] div {
        color: #1E1E1C !important;
    }

    /* Tab Headers styling to fix visibility */
    button[data-testid="stTab"] p {
        color: #5D5954 !important;
        font-weight: 500 !important;
        font-family: 'Lora', serif !important;
    }
    button[data-testid="stTab"][aria-selected="true"] p {
        color: #B89C72 !important;
        font-weight: 700 !important;
    }

    /* Chat Messages styling */
    div[data-testid="stChatMessage"] {
        background-color: #FFFFFF !important;
        border: 1px solid #EFEBE4 !important;
        border-radius: 12px !important;
        padding: 16px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.015) !important;
    }
    
    div[data-testid="stChatMessage"] p,
    div[data-testid="stChatMessage"] li,
    div[data-testid="stChatMessage"] span,
    div[data-testid="stChatMessage"] div {
        color: #1E1E1C !important;
    }
    
    div[data-testid="stChatMessageUser"] {
        background-color: #F6F3EC !important;
        border-left: 4px solid #4C5270 !important;
    }

    div[data-testid="stChatMessageAssistant"] {
        border-left: 4px solid #B89C72 !important;
    }

    /* Custom Chat Input styling */
    div[data-testid="stChatInput"] {
        background-color: #FFFFFF !important;
        border: 1px solid #B89C72 !important;
        border-radius: 24px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04) !important;
    }

    div[data-testid="stChatInput"] textarea {
        color: #1E1E1C !important;
        font-family: 'Inter', sans-serif !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #8C6C42 !important;
        opacity: 0.65;
    }

    /* Expander styling for legal sources */
    div[data-testid="stExpander"] {
        border: 1px solid #E6DEC1 !important;
        border-radius: 8px !important;
        background-color: #FDFDFB !important;
        margin-top: 10px !important;
    }

    div[data-testid="stExpander"] summary {
        font-family: 'Lora', serif !important;
        color: #8C6C42 !important;
        font-weight: 600 !important;
    }

    .source-block {
        border-left: 3px solid #B89C72;
        padding-left: 12px;
        margin-bottom: 15px;
        background-color: #FAF7F2;
        padding-top: 8px;
        padding-bottom: 8px;
        border-radius: 0 4px 4px 0;
    }

    .source-title {
        font-family: 'Lora', serif !important;
        font-size: 0.9rem !important;
        font-weight: bold;
        color: #8C6C42;
        margin-bottom: 4px;
    }

    .source-content {
        font-size: 0.85rem !important;
        color: #4A453F;
        line-height: 1.4;
        font-style: italic;
    }

    /* Premium Styled Buttons */
    .stButton>button {
        background-color: #FFFFFF !important;
        color: #8C6C42 !important;
        border: 1px solid #B89C72 !important;
        border-radius: 20px !important;
        font-weight: 600 !important;
        padding: 8px 24px !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 2px 6px rgba(184, 156, 114, 0.15) !important;
    }

    .stButton>button:hover {
        background-color: #B89C72 !important;
        color: #FFFFFF !important;
        border-color: #B89C72 !important;
        box-shadow: 0 4px 10px rgba(184, 156, 114, 0.3) !important;
        transform: translateY(-1px);
    }

    /* Disclaimer box styling */
    .disclaimer-box {
        border: 1px solid #B89C72;
        background-color: #FAF7F2;
        color: #8C6C42;
        padding: 12px;
        border-radius: 6px;
        font-size: 0.85rem;
        margin-top: 20px;
        line-height: 1.4;
        text-align: justify;
    }
    </style>
    """, unsafe_allow_html=True)

# Top Hero Banner (Always visible)
st.markdown("""
<div class="hero-container">
    <div class="hero-title">NyayaAI</div>
    <div class="hero-tagline">Led by the Truth • Citizen's Constitutional Guide</div>
    <div class="hero-divider"></div>
</div>
""", unsafe_allow_html=True)

# Helper function for Text-to-Speech (gTTS)
def generate_speech(text, language_name):
    """Generates an in-memory MP3 audio stream using gTTS based on selected language."""
    from gtts import gTTS
    import io
    
    # Map selected language to gTTS language codes
    lang_map = {
        "English": "en",
        "Hindi (हिन्दी)": "hi",
        "Marathi (मराठी)": "mr",
        "Tamil (தமிழ்)": "ta",
        "Telugu (తెలుగు)": "te",
        "Bengali (বাংলা)": "bn"
    }
    lang_code = lang_map.get(language_name, "en")
    
    # Pre-process text to strip markdown formatting characters for cleaner audio synthesis
    clean_text = text.replace("**", "").replace("*", "").replace("`", "").replace("#", "").replace("- ", "")
    
    try:
        tts = gTTS(text=clean_text, lang=lang_code)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp
    except Exception as e:
        st.error(f"Text-to-Speech failed: {e}")
        return None

# Initialize Engine (Cached)
@st.cache_resource
def load_nyaya_engine():
    engine = NyayaEngine()
    pdf_path = "data/constitution.pdf"
    try:
        has_index = engine.vectorstore._collection.count() > 0
    except Exception:
        has_index = False

    if os.path.exists(pdf_path) and not has_index:
        with st.spinner("Indexing the Constitution for the first time... This will take a moment."):
            engine.ingest_data(pdf_path)
    return engine

try:
    engine = load_nyaya_engine()
except Exception as e:
    st.error(f"Error initializing system: {e}")
    st.stop()

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.markdown("<h2 class='legal-header'>⚖️ Nyaya Sahayak</h2>", unsafe_allow_html=True)
    st.write("An educational AI tool designed to help Indian citizens identify their Constitutional rights.")
    st.divider()
    
    # Language Picker Selector
    st.markdown("<h3 class='legal-header'>🌐 Language / भाषा</h3>", unsafe_allow_html=True)
    selected_lang = st.selectbox(
        "Choose consultation language:",
        ["English", "Hindi (हिन्दी)", "Marathi (मराठी)", "Tamil (தமிழ்)", "Telugu (తెలుగు)", "Bengali (বাংলা)"]
    )
    
    st.divider()
    st.markdown("<h3 class='legal-header'>Example Scenarios</h3>", unsafe_allow_html=True)
    st.info("💼 **Labor & Livelihood:**\n'I work as a driver but my boss has refused to pay my wages.'")
    st.info("🚨 **Personal Liberty:**\n'My brother was taken by police 30 hours ago and hasn't seen a judge.'")
    st.info("🏫 **Social Discrimination:**\n'A government school refuses to admit my daughter because of our caste.'")
    
    st.divider()
    if st.button("Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_voice_id = None
        st.session_state.voice_prompt = None
        st.rerun()
        
    st.markdown("""
    <div class="disclaimer-box">
        <strong>⚠️ Educational Disclaimer:</strong><br>
        NyayaAI is an educational helper tool. It does not provide official legal representation or advice. 
        For court representation and legal disputes, please consult a qualified advocate.
    </div>
    """, unsafe_allow_html=True)

# Create App Tabs
tab_home, tab_chat = st.tabs(["🏛️ Homepage & Work Done", "💬 Constitutional Assistant"])

# --- TAB 1: HOMEPAGE ---
with tab_home:
    col_logo, col_title = st.columns([1, 4])
    with col_logo:
        if os.path.exists("data/justice_logo.png"):
            st.image("data/justice_logo.png", width=90)
    with col_title:
        st.markdown("<h2 style='margin-top: 5px; font-family: \"Playfair Display\", serif;'>Nyaya Sahayak</h2>", unsafe_allow_html=True)
        st.markdown("<p style='font-family: \"Lora\", serif; color: #B89C72; font-style: italic;'>Truth Alone Triumphs • Satyameva Jayate</p>", unsafe_allow_html=True)
    
    st.divider()

    # Hero Lady Justice Image
    if os.path.exists("data/lady_justice.png"):
        st.image("data/lady_justice.png", use_container_width=True)

    # Classic Quote Block
    st.markdown("""
    <div style="background-color: #FDFDFB; border-left: 3px solid #B89C72; padding: 20px; margin: 20px 0; border-radius: 4px; box-shadow: 0 4px 10px rgba(0,0,0,0.015);">
        <p style="font-family: 'Lora', serif; font-size: 1.15rem; font-style: italic; color: #1E1E1C; line-height: 1.6; margin-bottom: 8px;">
            "However good a Constitution may be, if those who are implementing it are not good, it will prove to be bad. 
            However bad a Constitution may be, if those implementing it are good, it will prove to be good."
        </p>
        <span style="font-weight: bold; color: #8C6C42; font-size: 0.9rem;">— Dr. B.R. Ambedkar (Father of the Constitution of India)</span>
    </div>
    """, unsafe_allow_html=True)

    # Project Description
    st.markdown("### 🏛️ Project Overview")
    st.write("""
    Legal language is highly complex and intimidating to the average citizen. **NyayaAI** is a professional-grade 
    Retrieval-Augmented Generation (RAG) system designed to empower Indian citizens. By translating real-life complaints 
    (such as discrimination, police excesses, education denial, or unpaid labor) into simple English, NyayaAI matches 
    them directly with relevant protective articles within the **Constitution of India (1950)**.
    """)

    # Technical Milestones / What We Have Done
    st.markdown("### 🛠️ What Have Done (Technical Architecture)")
    st.write("We implemented several optimizations to build a highly fast, quiet, trustworthy, and scoped constitutional guide:")

    st.markdown("""
    <div style="display: grid; grid-template-columns: 1fr; gap: 15px; margin-top: 15px; margin-bottom: 25px;">
        <div style="background-color: #FFFFFF; border: 1px solid #E6DEC1; padding: 15px; border-radius: 8px;">
            <h4 style="color: #8C6C42; margin-top: 0; font-family: 'Playfair Display', serif; margin-bottom: 8px;">📖 Recursive Chunking (Parent-Child Strategy)</h4>
            <p style="font-size: 0.9rem; color: #4A453F; margin-bottom: 0; line-height: 1.5;">
                We used a custom text splitter to load the Constitution of India. Legal Articles must not be split in half arbitrarily, 
                as that breaks legal context. Our <b>Parent-Child Splitter</b> saves the complete uncut Article as the parent document 
                for final LLM reading context, while using smaller vectorized child chunks to match the user's search queries accurately.
            </p>
        </div>
        <div style="background-color: #FFFFFF; border: 1px solid #E6DEC1; padding: 15px; border-radius: 8px;">
            <h4 style="color: #8C6C42; margin-top: 0; font-family: 'Playfair Display', serif; margin-bottom: 8px;">⚡ PyTorch CPU Optimization (Silent Operation)</h4>
            <p style="font-size: 0.9rem; color: #4A453F; margin-bottom: 0; line-height: 1.5;">
                To prevent high CPU usage that causes laptop fans to buzz loudly when calculating local embeddings, we optimized 
                PyTorch to run on a <b>single thread</b> (<code>torch.set_num_threads(1)</code>). Query embedding runs instantly 
                but silently, using minimal battery and zero background load.
            </p>
        </div>
        <div style="background-color: #FFFFFF; border: 1px solid #E6DEC1; padding: 15px; border-radius: 8px;">
            <h4 style="color: #8C6C42; margin-top: 0; font-family: 'Playfair Display', serif; margin-bottom: 8px;">🌐 Multilingual Speech-to-Text & Text-to-Speech</h4>
            <p style="font-size: 0.9rem; color: #4A453F; margin-bottom: 0; line-height: 1.5;">
                To ensure accessibility, citizens can record their legal issues in their own voice. Audio is transcribed 
                via Groq's high-speed Whisper API, and answers can be read out loud using Google Text-to-Speech in 
                <b>English, Hindi, Marathi, Tamil, Telugu, or Bengali</b>, depending on user selection.
            </p>
        </div>
        <div style="background-color: #FFFFFF; border: 1px solid #E6DEC1; padding: 15px; border-radius: 8px;">
            <h4 style="color: #8C6C42; margin-top: 0; font-family: 'Playfair Display', serif; margin-bottom: 8px;">🛡️ Strict Scope Guardrails (Anti-Hallucination)</h4>
            <p style="font-size: 0.9rem; color: #4A453F; margin-bottom: 0; line-height: 1.5;">
                We integrated strict rules to protect the chatbot from answering off-topic general knowledge queries 
                (like sports, math, coding, or foreign geography). If a question is not about Indian Constitutional issues, 
                it declines with a standard, formal scope warning.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='text-align: center; color: #B89C72; font-style: italic; font-size: 0.95rem;'>Click the <b>Constitutional Assistant</b> tab at the top to begin your consultation.</p>", unsafe_allow_html=True)


# --- TAB 2: LEGAL ASSISTANT ---
with tab_chat:
    # Chat History & Audio State Setup
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "last_voice_id" not in st.session_state:
        st.session_state.last_voice_id = None
    if "voice_prompt" not in st.session_state:
        st.session_state.voice_prompt = None

    # Display Microphone Audio Input Widget
    audio_file = st.audio_input("🎤 Record your grievance / अपनी आवाज़ में समस्या रिकॉर्ड करें")

    voice_query_ready = False
    
    # Process Voice Input
    if audio_file:
        voice_id = f"{audio_file.size}_{audio_file.name}"
        # Transcribe only if we have not processed this audio file yet
        if st.session_state.last_voice_id != voice_id:
            with st.spinner("Transcribing speech..."):
                try:
                    transcription = engine.transcribe_audio(audio_file)
                    st.session_state.voice_prompt = transcription
                    st.session_state.last_voice_id = voice_id
                except Exception as e:
                    st.error(f"Transcription error: {e}")
        
        # Display the transcription and provide a submit button
        if st.session_state.voice_prompt:
            st.info(f"🗣️ **Transcribed Text:** *\"{st.session_state.voice_prompt}\"*")
            if st.button("⚖️ Submit Transcribed Voice Query", use_container_width=True):
                voice_query_ready = True

    # Display Messages from History
    for idx, message in enumerate(st.session_state.messages):
        avatar = "👤" if message["role"] == "user" else "⚖️"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])
            
            # If assistant message has source articles, display them below
            if message["role"] == "assistant":
                # Text-to-Speech Playback Button
                if st.button(f"🔊 Play Audio Response", key=f"tts_{idx}"):
                    with st.spinner("Synthesizing audio..."):
                        audio_fp = generate_speech(message["content"], selected_lang)
                        if audio_fp:
                            st.audio(audio_fp, format="audio/mp3")

                if "sources" in message and message["sources"]:
                    with st.expander("🔍 Constitutional Context & Sources Used"):
                        for src in message["sources"]:
                            st.markdown(f"""
                            <div class="source-block">
                                <div class="source-title">Article Snippet {src['id']} (Source: {src['source']}, Page {src['page']})</div>
                                <div class="source-content">"{src['content']}"</div>
                            </div>
                            """, unsafe_allow_html=True)

    # Establish final query string from either text input or voice input
    query_text = None
    
    # Check if voice button was clicked
    if voice_query_ready and st.session_state.voice_prompt:
        query_text = st.session_state.voice_prompt
        # Reset voice query state so it doesn't fire twice
        st.session_state.voice_prompt = None
        st.session_state.last_voice_id = None
        
    # Check if standard text input is sent
    text_prompt = st.chat_input("Describe your grievance (e.g. 'My owner has not paid my wages for 4 months')")
    if text_prompt:
        query_text = text_prompt

    # Process Query
    if query_text:
        # Add user message to session state & display
        st.session_state.messages.append({"role": "user", "content": query_text})
        with st.chat_message("user", avatar="👤"):
            st.markdown(query_text)

        # Generate Assistant Response
        with st.chat_message("assistant", avatar="⚖️"):
            with st.spinner("Consulting the Constitution of India..."):
                response_data = engine.get_response(query_text, language=selected_lang)
                answer = response_data["answer"]
                sources = response_data["sources"]
                
                # Render answer
                st.markdown(answer)
                
                # Check if it was rejected by guardrails (so we don't display empty RAG sources)
                is_rejected = "I am unable to deliver an answer to this question" in answer
                
                # Automatically offer TTS option immediately
                if st.button("🔊 Play Audio Response", key=f"tts_latest"):
                    with st.spinner("Synthesizing audio..."):
                        audio_fp = generate_speech(answer, selected_lang)
                        if audio_fp:
                            st.audio(audio_fp, format="audio/mp3")

                # Display source expander for immediate feedback
                if sources and not is_rejected:
                    with st.expander("🔍 Constitutional Context & Sources Used"):
                        for src in sources:
                            st.markdown(f"""
                            <div class="source-block">
                                <div class="source-title">Article Snippet {src['id']} (Source: {src['source']}, Page {src['page']})</div>
                                <div class="source-content">"{src['content']}"</div>
                            </div>
                            """, unsafe_allow_html=True)
                
                # Save assistant message and sources to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": [] if is_rejected else sources
                })
                st.rerun()