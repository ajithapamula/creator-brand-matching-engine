from sentence_transformers import SentenceTransformer
import numpy as np
from functools import lru_cache
from .config import Config

@lru_cache(maxsize=1)
def get_model():
    return SentenceTransformer(Config.EMBEDDING_MODEL)

def embed_texts(texts: list[str]) -> np.ndarray:
    model = get_model()
    emb = model.encode(texts, normalize_embeddings=True, convert_to_numpy=True)
    return emb.astype("float32")
