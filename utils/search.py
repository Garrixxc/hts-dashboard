# utils/search.py

from .supabase_db import supabase
from .embeddings import embed_text

def semantic_query(vector, limit=5):
    return (
        supabase.rpc(
            "match_chunks",
            {
                "query_embedding": vector,
                "match_count": limit
            }
        ).execute()
    )

def semantic_search_hts(query: str, limit: int):
    vector = embed_text(query)  # now always 1536
    return semantic_query(vector, limit)
