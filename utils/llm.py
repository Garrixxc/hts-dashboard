# utils/llm.py

from utils.search import semantic_search_hts


def classify_hts(description: str, limit: int = 5):
    """
    Classify a product description by finding nearest HTS knowledge chunks.
    Returns list of dicts with fields needed by UI.
    """

    response = semantic_search_hts(description, limit)

    # response.data is a list of returned rows
    rows = response.data

    results = []
    for row in rows:
        results.append({
            "hts_code": row.get("hts_code"),
            "title": row.get("title"),
            "normalized_text": row.get("normalized_text"),
            "distance": row.get("distance")
        })

    return results
