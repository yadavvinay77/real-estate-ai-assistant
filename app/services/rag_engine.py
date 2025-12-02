# app/services/rag_engine.py

import os
import glob

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

import numpy as np


class RAGEngine:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.docs = []
        self.embeddings = []

        for path in glob.glob("app/data/rag_docs/*.txt"):
            text = open(path, "r", encoding="utf-8").read()
            self.docs.append(text)
            self.embeddings.append(self.model.encode(text))

        self.embeddings = np.vstack(self.embeddings) if self.embeddings else np.zeros((1, 384))

    # FIND MOST RELEVANT DOCUMENT
    def retrieve(self, query: str):
        q_emb = self.model.encode(query).reshape(1, -1)
        sims = cosine_similarity(q_emb, self.embeddings)[0]
        idx = int(np.argmax(sims))
        return self.docs[idx]

    # ANSWER QUERY USING SIMPLE GROUNDING
    def answer(self, query: str) -> str:
        if not self.docs:
            return "I don’t have enough information about that yet."

        doc = self.retrieve(query)

        return (
            "📘 *Based on verified property documentation:*\n\n"
            + doc[:700]
            + "\n\n(Answer grounded using RAG)"
        )
