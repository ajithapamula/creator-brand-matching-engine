import time
import mlflow
from contextlib import contextmanager
from .config import Config

mlflow.set_tracking_uri(Config.MLFLOW_TRACKING_URI)

@contextmanager
def tracked_run(run_name: str):
    mlflow.set_experiment(Config.MLFLOW_EXPERIMENT_NAME)
    with mlflow.start_run(run_name=run_name):
        t0 = time.time()
        try:
            yield
        finally:
            mlflow.log_metric("wall_clock_s", time.time() - t0)

def log_retrieval(k: int, avg_sim: float):
    mlflow.log_metric("topk", k)
    mlflow.log_metric("avg_similarity", avg_sim)
