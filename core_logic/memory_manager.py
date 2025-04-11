import faiss
import numpy as np
import os
import json

class MemoryManager:
    def __init__(self, user_id, dim=384):
        self.user_id = user_id
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.data = []
        self.vector_store_path = f"memory_{user_id}.json"
        self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.vector_store_path):
            with open(self.vector_store_path, 'r') as f:
                saved = json.load(f)
                self.data = saved["data"]
                vectors = np.array(saved["vectors"]).astype('float32')
                if len(vectors) > 0:
                    self.index.add(vectors)

    def _save_memory(self):
        vectors = self.index.reconstruct_n(0, self.index.ntotal).tolist()
        with open(self.vector_store_path, 'w') as f:
            json.dump({
                "data": self.data,
                "vectors": vectors
            }, f)

    def store_interaction(self, user_input, ai_response):
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        combined = f"User: {user_input} AI: {ai_response}"
        vector = model.encode([combined])[0].astype('float32')
        self.index.add(np.array([vector]))
        self.data.append({"user": user_input, "ai": ai_response})
        self._save_memory()

    def retrieve_relevant(self, query, limit=5):
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        vector = model.encode([query])[0].astype('float32')
        D, I = self.index.search(np.array([vector]), limit)

        results = []
        for i in I[0]:
            if i < len(self.data):
                results.append(self.data[i])
        return results
