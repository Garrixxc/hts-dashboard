from .embeddings import embed_text
from .supabase_db import supabase

def semantic_query(vector, limit=5):
    return supabase.rpc(
        "match_chunks",
        {
            "query_embedding": vector,
            "match_count": limit
        }
    ).execute()

def semantic_search_hts(query: str, limit: int):
    vector = embed_text(query)
    return semantic_query(vector, limit)
