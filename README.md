⚖️ NyayaAI — Constitutional Problem Solver (India)

NyayaAI is a professional-grade Retrieval-Augmented Generation (RAG) system designed to empower Indian citizens by providing actionable legal guidance grounded in the Constitution of India.

Most citizens find legal language intimidating. NyayaAI bridges this gap by allowing users to describe real-life problems (like unpaid wages, police misconduct, or discrimination) in plain English and receive responses mapped to relevant Constitutional Articles.

🚀 Project Overview

NyayaAI helps users:

Explain problems in simple language

Automatically map the scenario to relevant Constitutional Articles

Get a structured response with:

Article citations

Legal reasoning

Action plan / next steps

⚠️ Disclaimer: NyayaAI is an educational tool and does not provide formal legal advice. Always consult a qualified lawyer for legal proceedings.

🧠 Core Features
✅ Scenario-Based Reasoning

Unlike basic search, NyayaAI understands a user’s grievance and maps it to specific Articles.

✅ Article Integrity (Parent Document Retrieval)

Uses advanced chunking to ensure Articles are not “cut in half,” preserving full legal context.

✅ Lightning Fast Inference

Powered by Groq’s LPU technology for sub-second response times.

✅ Multilingual Potential

Built on Llama 3.3, enabling future support for multiple Indian languages.

🛠️ Tech Stack (Free Power Stack)
Component	Technology
Orchestration	LangChain
LLM (Reasoning)	Groq (Llama-3.3-70b-versatile)
Embeddings	Google Gemini (text-embedding-004)
Vector Store	ChromaDB (Local / In-Memory)
UI Framework	Streamlit
🧩 Technical Implementation
📌 Data Ingestion

Extracted text from the official Constitution of India PDF using PyPDFLoader.

📌 Recursive Chunking (Parent–Child Strategy)

Parent chunks preserve full Article context

Child chunks improve semantic retrieval accuracy

📌 Semantic Search

Legal text converted into embeddings using Gemini embedding models

Stored in ChromaDB for fast similarity search

📌 Contextual Prompting

Custom legal persona prompt ensures the AI:

cites Articles

explains reasoning

provides structured action plans

📁 Folder Structure
NyayaAI/
│
├── app.py                  # Streamlit web interface
├── src/
│   ├── engine.py           # RAG pipeline + retrieval + Groq integration
│   └── prompts.py          # Legal persona prompt + response format rules
│
├── data/                   # Source documents (Constitution PDF, processed text, etc.)
├── requirements.txt
└── README.md

🧪 Strategic Test Questions (Lawyer Thinking Test)

These scenario-based questions test whether NyayaAI can map messy real-life situations to the correct Constitutional Articles.

1) Labor & Wages (Economic Justice Test)

Question:

"I have been working as a driver for 4 months, but my owner has not paid my salary and is threatening to fire me if I ask for it. Does the Constitution protect me?"

Expected Constitutional Mapping:

Article 23 — Prohibition of forced labour (begar)

Article 21 — Right to livelihood (part of Right to Life)

2) Police & Liberty (Personal Freedom Test)

Question:

"The police took my brother to the station 30 hours ago without telling us why, and they haven't taken him to a judge. Is this legal?"

Expected Constitutional Mapping:

Article 22 — Must be produced before a magistrate within 24 hours

Article 21 — Protection of life and personal liberty

3) Discrimination (Social Equality Test)

Question:

"A local government school is refusing to admit my daughter because of our caste/religion. What can I do?"

Expected Constitutional Mapping:

Article 15 — Prohibition of discrimination

Article 21A — Right to education (6–14 years)

4) Gender & Privacy (Modern Rights Test)

Question:

"Can the government force me to share my private phone data without a valid reason?"

Expected Constitutional Mapping:

Right to Privacy under Article 21
(as recognized in the Puttaswamy judgment)

✅ Future Improvements (Optional Section)

Add multilingual UI (Hindi / Marathi / Tamil etc.)

Add IPC/CrPC support for criminal procedure guidance

Add case-law citations (Supreme Court landmark judgments)

Deploy on cloud with persistent vector DB

📌 Disclaimer

NyayaAI is an educational and informational tool. It is not a substitute for professional legal advice.
For legal proceedings, consult a licensed advocate
