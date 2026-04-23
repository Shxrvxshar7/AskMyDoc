# DocSense 🧠
> Ask questions. Get answers. From any document.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![LangChain](https://img.shields.io/badge/LangChain-0.2-green?style=flat-square)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-orange?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-teal?style=flat-square&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?style=flat-square&logo=streamlit)
![Gemini](https://img.shields.io/badge/Gemini-LLM-purple?style=flat-square&logo=google)

---

## What is DocSense?

DocSense is an AI-powered document intelligence app built on **Retrieval-Augmented Generation (RAG)**. Upload any PDF, ask questions in plain English, and get accurate answers — grounded in your document, not hallucinated.

Built as a learning project to understand how production RAG systems work — the same architecture used in enterprise AI applications.

---

## How It Works

```
PDF Upload → Chunking → Embeddings → ChromaDB
                                          ↓
User Question → Query Embedding → Retrieval → Gemini LLM → Answer
```

1. **Ingest** — PDF is split into overlapping text chunks
2. **Embed** — Each chunk is converted to a vector using HuggingFace Sentence Transformers
3. **Store** — Vectors are stored in ChromaDB (local vector database)
4. **Retrieve** — User query is embedded and matched against stored vectors
5. **Generate** — Relevant chunks + question are sent to Gemini → accurate answer

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| LLM | Google Gemini API |
| Orchestration | LangChain |
| Embeddings | HuggingFace Sentence Transformers |
| Vector DB | ChromaDB |
| API Backend | FastAPI |
| Frontend | Streamlit |
| Version Control | Git + GitHub |

---

## Features

- Upload any PDF and query it instantly
- Source-grounded answers — no hallucination
- FastAPI backend for clean API separation
- Streamlit UI — simple, fast, no frontend knowledge needed
- Fully local vector storage with ChromaDB

---

## Project Structure

```
DocSense/
│
├── app/
│   ├── ingest.py          # PDF loading, chunking, embedding
│   ├── retriever.py       # ChromaDB query logic
│   ├── chain.py           # LangChain RAG chain
│   └── api.py             # FastAPI endpoints
│
├── ui/
│   └── streamlit_app.py   # Streamlit frontend
│
├── data/
│   └── uploads/           # PDF storage
│
├── requirements.txt
├── .env.example
└── README.md
```

---

## Getting Started

```bash
# Clone the repo
git clone https://github.com/Shxrvxshar7/DocSense.git
cd DocSense

# Install dependencies
pip install -r requirements.txt

# Add your API key
cp .env.example .env
# Add GOOGLE_API_KEY to .env

# Run the app
streamlit run ui/streamlit_app.py
```

---

## What I Learned

- How RAG pipelines work end to end
- How embeddings convert text to meaning
- How vector similarity retrieval works
- How to build a production-style AI backend with FastAPI
- LangChain orchestration — connecting LLM, retriever, and prompt

---

## Roadmap

- [ ] Multi-document support
- [ ] Chat history / memory
- [ ] Agentic search (web + document combined)
- [ ] Cloud deployment (AWS / Azure)
- [ ] Evaluation with RAGAS

---

## Author

**Sharvesh A R**
SIH'24 National Winner | GenAI Builder | AI Enthusiast

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/sharvesh-a-r-932873257/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat-square&logo=github)](https://github.com/Shxrvxshar7)

---

> Built to understand. Built to ship. Built to grow.