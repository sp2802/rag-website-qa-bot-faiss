# RAG-Based Website Q&A Bot

## Project Overview

This project implements an end-to-end **Retrieval Augmented Generation (RAG)** system that answers user questions **strictly based on the content of a crawled website**.

The system crawls the **FastAPI documentation website**, processes and indexes its content, and exposes REST APIs that allow users to ask questions and receive **grounded, source-backed answers**.  
Hallucinations are prevented by restricting answers to retrieved context only.

---

## Website Used for Crawling

**Base URL**
https://fastapi.tiangolo.com

This site was chosen because it is text-heavy, crawler-friendly, and ideal for demonstrating semantic search and RAG.

---

## Project Architecture

Crawl → Clean → Chunk → Embed → Vector DB → Retrieve → Answer

---

## Setup Instructions

1. Create and activate virtual environment

python -m venv venv   
venv\Scripts\activate    (Windows)

2. Install dependencies

pip install -r requirements.txt

3. Start the API server

python run.py

Server runs at:  
http://localhost:8000

---

## REST API Endpoints

### POST /crawl

Crawls the FastAPI documentation and builds the vector index.

Request:
{
  "baseUrl": "https://fastapi.tiangolo.com"
}

Actions:
- Crawl internal pages
- Extract and clean visible text
- Chunk content with overlap
- Generate embeddings
- Index embeddings using FAISS

Response:
{
  "message": "Crawl & indexing completed",
  "pages": 20,
  "chunks": 120
}

---

### POST /ask

Answers user questions using retrieved documentation content.

Request:
{
  "question": "What is FastAPI?"
}

Response:
{
  "answer": "FastAPI is a modern, fast web framework for building APIs with Python...",
  "sources": ["https://fastapi.tiangolo.com/"]
}

If the answer is not present in the crawled content, the system responds:
"I don’t know based on the provided information."

---

### POST /reindex (Optional Enhancement)

Rebuilds embeddings and the FAISS index when website content changes.

Request:
{
  "baseUrl": "https://fastapi.tiangolo.com"
}

---

## Testing Questions

I have used questions to test the system:

- What is FastAPI?
- What is FastAPI mainly used for?
- What are the main features of FastAPI?
- How does FastAPI handle data validation?
- What is ASGI and how does FastAPI use it?
- Who is the Prime Minister of India?

Expected behavior for unrelated questions:
"I don’t know based on the provided information."

---

## FAQ Generation (Optional Enhancement)

A batch script generates a full FAQ document using the same retrieval pipeline.

Generate FAQ JSON:
python scripts/generate_faq.py

Output:
data/faq.json

Convert FAQ to Markdown:
python scripts/faq_to_markdown.py

Output:
data/FAQ.md

---

## Technologies Used

Python  
FastAPI  
Sentence Transformers (all-MiniLM-L6-v2)  
FAISS  
BeautifulSoup  
Requests
