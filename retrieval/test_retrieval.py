import json, faiss, numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
chunks = json.load(open("data/chunks.json"))
index = faiss.read_index("data/faiss.index")

q = input("Query: ")
qv = np.array(model.encode([q])).astype("float32")
_, idxs = index.search(qv, 5)

for i in idxs[0]:
    print(chunks[i]["url"])
    print(chunks[i]["content"][:200])
    print("-"*50)