import numpy as np
from typing import List, Dict

def rank_candidates(similarities: np.ndarray, meta: List[Dict], alpha: float = 0.8, beta: float = 0.2):
    scores = []
    for sim, m in zip(similarities, meta):
        engagement = float(m.get("avg_engagement_rate", 0))
        score = alpha * float(sim) + beta * engagement
        scores.append(score)
    order = np.argsort(scores)[::-1]
    return order, np.array(scores)[order]
