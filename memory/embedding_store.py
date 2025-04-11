import faiss
import os
import pickle
from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# File paths
INDEX_PATH = "memory/embeddings/chat_embeddings.index"
META_PATH = "memory/embeddings/metadata.pkl"

# Load or initialize index and metadata
if os.path.exists(INDEX_PATH):
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "rb") as f:
        metadata = pickle.load(f)
else:
    index = faiss.IndexFlatL2(384)  # 384-dim for 'all-MiniLM-L6-v2'
    metadata = []  # Stores (user_input, response, emotion)


def store_message(user_input, response, emotion):
    vector = embedder.encode([user_input])[0]
    index.add(np.array([vector]))
    metadata.append((user_input, response, emotion))
    _save()


def search_similar_messages(query, top_k=3):
    vector = embedder.encode([query])[0]
    D, I = index.search(np.array([vector]), top_k)
    results = []
    for idx in I[0]:
        if idx < len(metadata):
            results.append(metadata[idx])
    return results


def _save():
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(metadata, f)
