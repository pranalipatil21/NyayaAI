import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_core.stores import InMemoryStore
from langchain_classic.retrievers import ParentDocumentRetriever
from .prompts import SYSTEM_PROMPT

load_dotenv()

class NyayaEngine:
    def __init__(self):
        # 1. Initialize APIs
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        self.llm = ChatGroq(
            model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            temperature=0.1
        )
        
        # 2. Setup Storage (Using InMemoryStore for stability)
        self.store = InMemoryStore()
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
        
        # 4. Initialize Retriever
        self.retriever = ParentDocumentRetriever(
            vectorstore=self.vectorstore,
            docstore=self.store,
            child_splitter=self.child_splitter,
            parent_splitter=self.parent_splitter,
        )

    def ingest_data(self, pdf_path):
        """Loads and indexes the PDF."""
        if not os.path.exists(pdf_path):
            return False
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        self.retriever.add_documents(docs, ids=None)
        return True

    def get_response(self, query):
        """Retrieves context and generates legal advice."""
        # Get relevant articles
        retrieved_docs = self.retriever.invoke(query)
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])
        
        # Build prompt
        formatted_prompt = SYSTEM_PROMPT.format(context=context)
        
        # Call LLM
        response = self.llm.invoke([
            ("system", formatted_prompt),
            ("human", query)
        ])
        return response.content