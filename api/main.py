from fastapi import FastAPI
from pydantic import BaseModel
import json, faiss, numpy as np, logging
from pathlib import Path

from crawling.crawler import crawl_website
from text_extraction.extractor import extract_clean_text
from chunking.chunker import chunk_text
from embeddings.embedder import embed_texts

logging.basicConfig(level=logging.INFO)
app = FastAPI(title="RAG Support Bot")

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

INDEX = None
CHUNKS = []

class CrawlRequest(BaseModel):
    baseUrl: str

class QuestionRequest(BaseModel):
    question: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/crawl")
def crawl(payload: CrawlRequest):
    global INDEX, CHUNKS

    pages = crawl_website(payload.baseUrl)
    clean_pages = [extract_clean_text(p) for p in pages]

    chunks, cid = [], 0
    for page in clean_pages:
        for c in chunk_text(page["text"]):
            chunks.append({
                "chunk_id": cid,
                "url": page["url"],
                "title": page["title"],
                "content": c
            })
            cid += 1

    vectors = np.array(embed_texts([c["content"] for c in chunks])).astype("float32")
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)

    json.dump(chunks, open(DATA_DIR / "chunks.json", "w"), indent=2)
    faiss.write_index(index, str(DATA_DIR / "faiss.index"))

    INDEX, CHUNKS = index, chunks
    return {"message": "Crawl & indexing completed", "pages": len(pages), "chunks": len(chunks)}

@app.post("/reindex")
def reindex(payload: CrawlRequest):
    return crawl(payload)

@app.post("/ask")
def ask(payload: QuestionRequest):
    if INDEX is None:
        return {"error": "Run /crawl first"}

    q_emb = np.array(embed_texts([payload.question])).astype("float32")
    _, idxs = INDEX.search(q_emb, 5)
    retrieved = [CHUNKS[i] for i in idxs[0]]

    context = "\n\n".join(c["content"] for c in retrieved)
    return {
        "answer": context[:1500],
        "sources": list(set(c["url"] for c in retrieved))
    }