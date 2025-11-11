

## 🧠 src/config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    USE_PINECONE = os.getenv("USE_PINECONE", "false").lower() == "true"
    FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", ".faiss/index.bin")
    FAISS_META_PATH = os.getenv("FAISS_META_PATH", ".faiss/meta.npy")
    MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "mlruns")
    MLFLOW_EXPERIMENT_NAME = os.getenv("MLFLOW_EXPERIMENT_NAME", "vrd_creator_brand_matching")
    PORT = int(os.getenv("PORT", "8000"))
