import os
from supabase import create_client, Client
from openai import OpenAI
from dotenv import load_dotenv

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EMBED_MODEL = "text-embedding-3-small"   # 1536-dim


# ----------------------------------------------------------------
# Create embedding for text
# ----------------------------------------------------------------
def embed(text: str):
    resp = client.embeddings.create(
        model=EMBED_MODEL,
        input=text,
    )
    return resp.data[0].embedding


# ----------------------------------------------------------------
# Vector search query
# ----------------------------------------------------------------
def semantic_query(embedding, limit=5):
    """
    Uses pgvector similarity search.
    """
    response = (
        supabase.table("hts_knowledge_chunks")
        .select(
            "hts_code, title, normalized_text, embedding <-> {}".format(embedding)
        )
        .order("embedding", desc=False)  # vector distance asc
        .limit(limit)
        .execute()
    )

    return response.data


# ----------------------------------------------------------------
# Pagination
# ----------------------------------------------------------------
def get_hts_page(page=1, page_size=20):
    offset = (page - 1) * page_size
    res = (
        supabase.table("hts_knowledge_chunks")
        .select("hts_code, title, normalized_text")
        .range(offset, offset + page_size - 1)
        .execute()
    )
    return res.data


# ----------------------------------------------------------------
# Count total rows
# ----------------------------------------------------------------
def count_hts_rows():
    res = (
        supabase.table("hts_knowledge_chunks")
        .select("*", count="exact", head=True)
        .execute()
    )
    return res.count
