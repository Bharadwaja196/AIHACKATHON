# memory_manager.py

import faiss
import numpy as np
import os
import pickle
from embeddings.embedding_manager import EmbeddingManager

class MemoryManager:
    def __init__(self, user_id, dim=384):
        self.user_id = user_id
        self.embedding_manager = EmbeddingManager()
        self.index_file = f"{user_id}_faiss.index"
        self.data_file = f"{user_id}_memory.pkl"
        self.dimension = dim

        self.index = faiss.IndexFlatL2(self.dimension)
        self.memory_data = []

        if os.path.exists(self.index_file) and os.path.exists(self.data_file):
            self._load_index()

    def _load_index(self):
        self.index = faiss.read_index(self.index_file)
        with open(self.data_file, 'rb') as f:
            self.memory_data = pickle.load(f)

    def _save_index(self):
        faiss.write_index(self.index, self.index_file)
        with open(self.data_file, 'wb') as f:
            pickle.dump(self.memory_data, f)

    def store_interaction(self, user_text, ai_response):
        vector = self.embedding_manager.embed_text(user_text)
        self.index.add(np.array([vector]))
        self.memory_data.append({
            "user": user_text,
            "ai": ai_response,
            "vector": vector
        })
        self._save_index()

    def retrieve_relevant(self, query_text, limit=5):
        query_vector = self.embedding_manager.embed_text(query_text)
        D, I = self.index.search(np.array([query_vector]), limit)
        return [self.memory_data[i] for i in I[0] if i < len(self.memory_data)]
