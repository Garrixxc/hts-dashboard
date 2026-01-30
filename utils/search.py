import os
from supabase import create_client
from utils.embeddings import embed_text

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_ROLE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
SUPABASE_TABLE = os.environ["SUPABASE_TABLE"]
SUPABASE_MATCH_RPC = os.getenv("SUPABASE_MATCH_RPC", "match_chunks")


supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


def semantic_query(vector, limit=5):
    response = supabase.rpc(
        SUPABASE_MATCH_RPC,
        {
            "query_embedding": vector,
            "match_count": limit
        }
    ).execute()

    return response.data


def semantic_search_hts(query, limit=5):
    vec = embed_text(query)
    return semantic_query(vec, limit)
