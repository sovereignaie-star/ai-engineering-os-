"""
Vector Store
تخزين واسترجاع الذاكرة باستخدام ChromaDB
"""

import chromadb
from chromadb.utils import embedding_functions
import os
import json
import hashlib

class VectorStore:
    def __init__(self, path: str = "./memory/chroma_db"):
        self.path = path
        self.client = chromadb.PersistentClient(path=path)
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        # إنشاء المجموعات
        self.short_term = self.client.get_or_create_collection(
            name="short_term",
            embedding_function=self.embedding_fn
        )
        self.long_term = self.client.get_or_create_collection(
            name="long_term",
            embedding_function=self.embedding_fn
        )
        self.semantic = self.client.get_or_create_collection(
            name="semantic",
            embedding_function=self.embedding_fn
        )
        self.project_history = self.client.get_or_create_collection(
            name="project_history",
            embedding_function=self.embedding_fn
        )

    def store(self, collection: str, text: str, metadata: dict = None):
        """تخزين نص في مجموعة محددة"""
        collections = {
            "short_term": self.short_term,
            "long_term": self.long_term,
            "semantic": self.semantic,
            "project_history": self.project_history
        }
        
        col = collections.get(collection)
        if not col:
            raise ValueError(f"Collection {collection} not found")
        
        doc_id = hashlib.md5(text.encode()).hexdigest()
        col.add(
            documents=[text],
            metadatas=[metadata or {}],
            ids=[doc_id]
        )
        return doc_id

    def search(self, collection: str, query: str, n_results: int = 5):
        """بحث في مجموعة محددة"""
        collections = {
            "short_term": self.short_term,
            "long_term": self.long_term,
            "semantic": self.semantic,
            "project_history": self.project_history
        }
        
        col = collections.get(collection)
        if not col:
            raise ValueError(f"Collection {collection} not found")
        
        results = col.query(
            query_texts=[query],
            n_results=n_results
        )
        return results

    def store_project_memory(self, project_id: str, memory: dict):
        """تخزين ذاكرة مشروع كامل"""
        text = json.dumps(memory)
        metadata = {
            "project_id": project_id,
            "timestamp": memory.get("timestamp", ""),
            "status": memory.get("status", "completed")
        }
        self.store("project_history", text, metadata)

    def recall_project(self, query: str, n_results: int = 3):
        """استرجاع مشاريع مشابهة"""
        results = self.search("project_history", query, n_results)
        return results
