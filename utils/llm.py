from utils.search import semantic_search_hts

def classify_hts(description: str, k: int):
    return semantic_search_hts(description, k)
