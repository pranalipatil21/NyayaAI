import os
import logging
import warnings

# --- PyTorch & Hugging Face CPU/Noise Optimizations ---
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

# Suppress Hugging Face download telemetry & rate limit warning logs
warnings.filterwarnings("ignore", message=".*unauthenticated requests.*")
warnings.filterwarnings("ignore", category=UserWarning)

try:
    import torch
    torch.set_num_threads(1)
    torch.set_num_interop_threads(1)
except (ImportError, RuntimeError):
    pass

try:
    from transformers.utils import logging as transformers_logging
    transformers_logging.set_verbosity_error()
except ImportError:
    pass

logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)
# -----------------------------------------------------

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from .prompts import SYSTEM_PROMPT

load_dotenv()

class NyayaEngine:
    def __init__(self):
        # 1. Initialize Local Embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5",
            model_kwargs={'device': 'cpu'}
        )
        
        # Candidate Groq models in priority order
        env_model = os.getenv("GROQ_MODEL")
        candidate_models = []
        if env_model:
            candidate_models.append(env_model)
        
        defaults = ["openai/gpt-oss-120b", "groq/compound", "qwen/qwen3.6-27b", "llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
        for m in defaults:
            if m not in candidate_models:
                candidate_models.append(m)
                
        self.candidate_models = candidate_models
        self.llm = ChatGroq(
            model=self.candidate_models[0],
            temperature=0.1
        )
        
        # 2. Setup Storage
        self.vectorstore = Chroma(
            collection_name="nyaya_legal_db",
            embedding_function=self.embeddings,
            persist_directory="./chroma_db"
        )
        
        # 3. Setup Splitters
        self.parent_splitter = RecursiveCharacterTextSplitter(
            separators=["\nArticle ", "\nPART ", "\n\n"],
            chunk_size=2000,
            chunk_overlap=0
        )
        self.child_splitter = RecursiveCharacterTextSplitter(
            chunk_size=400,
            chunk_overlap=50
        )
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 4})

    def ingest_data(self, pdf_path):
        """Loads and indexes the PDF as searchable chunks."""
        if not os.path.exists(pdf_path):
            return False
        
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()

        parent_docs = self.parent_splitter.split_documents(docs)
        child_docs = self.child_splitter.split_documents(parent_docs)

        if child_docs:
            self.vectorstore.add_documents(child_docs)
        return True

    def get_response(self, query, language="English"):
        """Retrieves context and generates legal advice in the specified language, alongside cited sources."""
        retrieved_docs = self.retriever.invoke(query)
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])
        
        # Append language instruction to LLM prompt
        lang_instruction = ""
        if language and language != "English":
            lang_instruction = f"\n\nCRITICAL LANGUAGE INSTRUCTION: You MUST translate and write your entire response (including all headings, bullet points, rights descriptions, action steps, disclaimers, and fallback responses) into {language}. Do not output any English text unless it is an official legal terms or article numbers (like 'Article 21')."
            
        formatted_prompt = SYSTEM_PROMPT.format(context=context) + lang_instruction
        
        # Attempt invocation with fallback model list
        response = None
        last_error = None
        
        for model_name in self.candidate_models:
            try:
                llm = ChatGroq(model=model_name, temperature=0.1)
                response = llm.invoke([
                    ("system", formatted_prompt),
                    ("human", query)
                ])
                self.llm = llm  # Store working model instance
                break
            except Exception as e:
                logging.warning(f"Groq model '{model_name}' failed: {e}. Trying next candidate...")
                last_error = e

        # Optional secondary fallback: Google Gemini
        if response is None:
            google_key = os.getenv("GOOGLE_API_KEY")
            if google_key:
                try:
                    from langchain_google_genai import ChatGoogleGenerativeAI
                    gemini_llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=google_key, temperature=0.1)
                    response = gemini_llm.invoke([
                        ("system", formatted_prompt),
                        ("human", query)
                    ])
                except Exception as ge:
                    logging.error(f"Gemini fallback failed: {ge}")

        if response is None:
            raise last_error or RuntimeError("All available LLM models failed to process query.")
        
        # Structure source documents for the UI to display explainability information
        sources = []
        for idx, doc in enumerate(retrieved_docs):
            page_num = doc.metadata.get("page", 0) + 1 if "page" in doc.metadata else "Unknown"
            source_file = os.path.basename(doc.metadata.get("source", "constitution.pdf"))
            sources.append({
                "id": idx + 1,
                "content": doc.page_content,
                "source": source_file,
                "page": page_num
            })

        return {
            "answer": response.content,
            "sources": sources
        }

    def transcribe_audio(self, audio_file):
        """Transcribes audio using Groq's Whisper API in a multilingual-aware manner."""
        try:
            from groq import Groq
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            
            # Read recorded audio bytes
            audio_bytes = audio_file.read()
            
            # Send to Groq's transcription endpoint
            transcription = client.audio.transcriptions.create(
                file=("recorded_audio.wav", audio_bytes),
                model="whisper-large-v3",
                prompt="Indian legal grievance, Indian names, Constitution of India, Hindi, Marathi, Tamil, Telugu, Bengali",
                response_format="text"
            )
            return transcription
        except Exception as e:
            raise RuntimeError(f"Voice transcription failed: {str(e)}")