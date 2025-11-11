from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
import numpy as np

from src.config import Config
from src.embeddings import embed_texts
from src.repository import CreatorRepository, BrandRepository
from src.indexer import build_or_load_index
from src.ranker import rank_candidates
from src.mlflow_tracking import tracked_run, log_retrieval

app = FastAPI(title="VRD Creator-Brand Matching API")

creator_repo = CreatorRepository()
brand_repo = BrandRepository()
index, X, META = build_or_load_index(creator_repo)

class RecommendRequest(BaseModel):
    brand_description: str = Field(..., description="Brand brief text")
    top_k: int = 5
    alpha: float = 0.8
    beta: float = 0.2

class CreatorIn(BaseModel):
    creator_id: str
    name: str
    bio: str
    topics: str
    avg_engagement_rate: float
    followers: int

@app.get("/health")
async def health():
    return {"status": "ok", "index_size": index.ntotal()}

@app.post("/recommend")
async def recommend(req: RecommendRequest):
    if not req.brand_description.strip():
        raise HTTPException(400, detail="brand_description required")

    with tracked_run("recommend"):
        q = embed_texts([req.brand_description])
        D, I = index.search(q, k=req.top_k)
        sims = D[0]
        idxs = I[0]
        candidates = [META[i] for i in idxs]
        order, scores = rank_candidates(sims, candidates, req.alpha, req.beta)

        out = []
        for j, pos in enumerate(order):
            m = candidates[pos]
            out.append({
                "rank": j + 1,
                "creator_id": m["creator_id"],
                "name": m["name"],
                "bio": m["bio"],
                "topics": m["topics"],
                "avg_engagement_rate": float(m["avg_engagement_rate"]),
                "followers": int(m["followers"]),
                "semantic_similarity": float(sims[pos]),
                "score": float(scores[j])
            })
        log_retrieval(req.top_k, float(np.mean(sims)))
        return {"results": out}

@app.post("/creators/upsert")
async def upsert_creator(creator: CreatorIn):
    creator_repo.upsert_creator(creator.model_dump())
    global index, X, META
    index, X, META = build_or_load_index(creator_repo)
    return {"status": "upserted", "index_size": index.ntotal()}
