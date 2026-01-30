# utils/llm.py

from .search import semantic_search_hts

def classify_hts(description: str, limit: int):
    return semantic_search_hts(description, limit)
