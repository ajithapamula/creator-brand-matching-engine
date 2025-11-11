import numpy as np
from src.ranker import rank_candidates

def test_ranker_orders_by_score():
    sims = np.array([0.9, 0.6, 0.7])
    meta = [
        {"avg_engagement_rate": 0.01},
        {"avg_engagement_rate": 0.10},
        {"avg_engagement_rate": 0.02},
    ]
    order, scores = rank_candidates(sims, meta)
    assert order[0] in (0, 1)
    assert len(scores) == 3
