# Uses retrieval logic to generate FAQ answers (optional)
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

# ---------- CONFIG ----------
TOP_K = 5
MODEL_NAME = "all-MiniLM-L6-v2"
DATA_DIR = Path("data")
FAQ_OUTPUT = DATA_DIR / "faq.json"

# ---------- LOAD EMBEDDING MODEL ----------
print("Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)

# ---------- LOAD DATA ----------
print("Loading chunks and FAISS index...")
with open(DATA_DIR / "chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

index = faiss.read_index(str(DATA_DIR / "faiss.index"))

# ---------- COMMON FASTAPI QUESTIONS ----------
questions = [
    "What is FastAPI?",
    "What is FastAPI mainly used for?",
    "What are the main features of FastAPI?",
    "How does FastAPI handle data validation?",
    "What is automatic API documentation in FastAPI?",
    "What standards does FastAPI support?",
    "What is ASGI and how does FastAPI use it?",
    "What role does Pydantic play in FastAPI?",
    "How does FastAPI compare to Flask?",
    "Is FastAPI suitable for production use?"
]

faq = []

# ---------- GENERATE FAQ ----------
for question in questions:
    print(f"Processing: {question}")

    # Embed question
    q_embedding = model.encode([question])
    q_embedding = np.array(q_embedding).astype("float32")

    # Retrieve relevant chunks
    distances, indices = index.search(q_embedding, TOP_K)
    retrieved_chunks = [chunks[i] for i in indices[0]]

    # Build answer purely from retrieved content
    context = " ".join(c["content"] for c in retrieved_chunks)

    if not context.strip():
        answer = "I don’t know based on the provided information."
    else:
        answer = context[:1200]  # keep concise

    faq.append({
        "question": question,
        "answer": answer,
        "sources": list(set(c["url"] for c in retrieved_chunks))
    })

# ---------- SAVE FAQ ----------
with open(FAQ_OUTPUT, "w", encoding="utf-8") as f:
    json.dump(faq, f, indent=2)

print(f"\n✅ FAQ document generated at {FAQ_OUTPUT}")
