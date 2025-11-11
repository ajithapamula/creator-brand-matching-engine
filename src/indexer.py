import os
import numpy as np
import faiss
from pathlib import Path
from typing import Tuple
from .config import Config
from .embeddings import embed_texts
from .repository import CreatorRepository

FAISS_DIR = Path(Config.FAISS_INDEX_PATH).parent
FAISS_DIR.mkdir(parents=True, exist_ok=True)

class FaissIndex:
    def __init__(self, d: int):
        self.index = faiss.IndexFlatIP(d)

    def add(self, vectors: np.ndarray):
        self.index.add(vectors)

    def search(self, query: np.ndarray, k: int = 5) -> Tuple[np.ndarray, np.ndarray]:
        return self.index.search(query, k)

    def ntotal(self) -> int:
        return self.index.ntotal

def build_or_load_index(repo: CreatorRepository) -> tuple[FaissIndex, np.ndarray, list[dict]]:
    creators = repo.all_creators()
    texts = (creators["bio"].fillna("") + " " + creators["topics"].fillna("")).tolist()
    meta = creators.to_dict(orient="records")
    X = embed_texts(texts)
    index = FaissIndex(X.shape[1])
    index.add(X)
    faiss.write_index(index.index, str(Config.FAISS_INDEX_PATH))
    np.save(Config.FAISS_META_PATH, X)
    return index, X, meta
