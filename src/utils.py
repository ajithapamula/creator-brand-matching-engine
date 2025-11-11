from typing import List

def safe_text(x) -> str:
    return (x or "").strip()

def topics_to_list(topics: str) -> List[str]:
    return [t.strip() for t in (topics or "").split("|") if t.strip()]
