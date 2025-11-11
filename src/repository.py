import pandas as pd
from pathlib import Path
from typing import Dict, Any

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

class CreatorRepository:
    def __init__(self, csv_path: str | None = None):
        self.csv_path = Path(csv_path) if csv_path else DATA_DIR / "sample_creators.csv"
        self.df = pd.read_csv(self.csv_path)

    def all_creators(self) -> pd.DataFrame:
        return self.df.copy()

    def upsert_creator(self, row: Dict[str, Any]):
        df = self.df
        if (df["creator_id"] == row["creator_id"]).any():
            self.df.loc[df["creator_id"] == row["creator_id"], :] = row
        else:
            self.df = pd.concat([self.df, pd.DataFrame([row])], ignore_index=True)
        self.df.to_csv(self.csv_path, index=False)

class BrandRepository:
    def __init__(self, csv_path: str | None = None):
        self.csv_path = Path(csv_path) if csv_path else DATA_DIR / "sample_brands.csv"
        self.df = pd.read_csv(self.csv_path)

    def find_by_name_or_desc(self, query: str) -> dict | None:
        q = query.lower()
        for _, r in self.df.iterrows():
            if q in str(r["name"]).lower() or q in str(r["description"]).lower():
                return r.to_dict()
        return None
