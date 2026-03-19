# AskMyDocs — RAG Document Intelligence System

> Upload any document. Ask anything. Get grounded, source-aware answers powered by Gemini.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-ff4b4b?style=flat-square)
![ChromaDB](https://img.shields.io/badge/ChromaDB-vector--db-purple?style=flat-square)
![Gemini](https://img.shields.io/badge/Gemini-2.5--flash-green?style=flat-square)

---

## What it does

AskMyDocs is a full-stack RAG (Retrieval-Augmented Generation) system that lets you have a conversation with any document. Instead of reading through pages of text, you upload a file and ask questions in plain English — the system finds the most relevant passages and uses Gemini to generate a grounded, accurate answer.

No hallucinations. No guessing. Every answer comes directly from your document.

---

## Demo
[Live app](https://rag-document-intelligence-vvsun9pvqjctp3wslay8lq.streamlit.app/)

Upload a PDF, DOCX, TXT, CSV, HTML, or Markdown file and start asking:

- *"What are the key points of this document?"*
- *"What conclusions does the author draw?"*
- *"Summarise the main argument."*

---

## How it works

```
Document
   │
   ▼
Loader ──► extracts clean text from any file type
   │
   ▼
Chunker ──► splits text into overlapping 500-char passages
   │
   ▼
Embedder ──► converts each chunk to a vector (Gemini Embedding)
   │         stores vectors in ChromaDB on disk
   ▼
  [User asks a question]
   │
   ▼
Query Embedder ──► embeds the question using the same model
   │
   ▼
Semantic Search ──► finds the top 3 most relevant chunks
   │
   ▼
Gemini 2.5 Flash ──► generates a grounded answer from context
   │
   ▼
Answer
```

---

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| LLM | Gemini 2.5 Flash |
| Embeddings | Gemini Embedding 2 Preview |
| Vector DB | ChromaDB (persistent) |
| PDF parsing | pdfplumber |
| DOCX parsing | python-docx |
| Environment | python-dotenv |

---

## Project structure

```
rag-document-intelligence/
│
├── app.py          # Streamlit frontend
├── loader.py       # File reader (PDF, DOCX, TXT, CSV, HTML)
├── chunker.py      # Text splitter with overlap
├── embedder.py     # Gemini embeddings + ChromaDB storage
├── retriever.py    # Semantic search + Gemini answer generation
├── .env            # API key (never committed)
├── .gitignore
└── uploads/        # Temporary file storage
```

---

## Getting started

### 1. Clone the repo

```bash
git clone https://github.com/Oyedunni1/rag-document-intelligence.git
cd rag-document-intelligence
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install streamlit langchain langchain-google-genai google-genai chromadb pdfplumber python-docx python-dotenv pandas beautifulsoup4 openpyxl
```

### 4. Set up your API key

Create a `.env` file in the root directory:

```
GOOGLE_API_KEY=your_gemini_api_key_here
```

Get your free API key at [aistudio.google.com](https://aistudio.google.com).

### 5. Run the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Supported file types

| Format | Extension |
|---|---|
| PDF | `.pdf` |
| Word Document | `.docx` |
| Plain Text | `.txt` |
| Markdown | `.md` |
| CSV | `.csv` |
| HTML | `.html` |

---

## Key concepts

**Retrieval-Augmented Generation (RAG)** — instead of relying on an LLM's training data, RAG retrieves relevant passages from your own documents and feeds them as context to the model. This means answers are grounded in your actual content, not generated from memory.

**Embeddings** — numerical representations of text that capture semantic meaning. Two passages about the same topic will have similar embeddings even if they use different words. This is what makes semantic search possible.

**Vector database** — a database optimised for storing and searching embeddings. ChromaDB stores your document vectors on disk so you don't have to re-embed every time you restart the app.

---

## Built by Oyedunni Oyewumi


[Portfolio](https://oyedunni1.github.io) · [GitHub](https://github.com/Oyedunni1) · [LinkedIn](https://linkedin.com/in/oyedunni-oyewumi)
