import os
import json
import hashlib

class VectorStore:
    def __init__(self, path="./memory/chroma_db"):
        self.path = path
        os.makedirs(path, exist_ok=True)

    def store(self, collection, text, metadata=None):
        doc_id = hashlib.md5(text.encode()).hexdigest()
        # تخزين بسيط بدون ChromaDB
        file_path = os.path.join(self.path, f"{collection}_{doc_id}.json")
        with open(file_path, "w") as f:
            json.dump({"text": text, "metadata": metadata or {}}, f)
        return doc_id

    def store_project_memory(self, project_id, memory):
        self.store("project_history", json.dumps(memory), {"project_id": project_id})

    def recall_project(self, query, n_results=3):
        return {"status": "not_implemented", "query": query}
