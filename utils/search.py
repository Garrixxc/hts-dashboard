import os
import time
from supabase import create_client
from utils.embeddings import embed_text

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_ROLE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
SUPABASE_TABLE = os.environ["SUPABASE_TABLE"]
# Default changed to match_hts_chunks based on error message
SUPABASE_MATCH_RPC = os.getenv("SUPABASE_MATCH_RPC", "match_hts_chunks")


supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


def semantic_query(vector, limit=5, max_retries=3):
    """
    Query Supabase RPC function with vector similarity search.
    
    CRITICAL: Supabase Python client passes parameters in ALPHABETICAL order.
    The function signature must be: function_name(match_count, query_embedding)
    even though we define them as {match_count, query_embedding} in the dict.
    
    Args:
        vector: Embedding vector (list of floats)
        limit: Number of results to return
        max_retries: Number of retry attempts on failure
    
    Returns:
        List of matching results from Supabase
    """
    last_error = None
    
    for attempt in range(max_retries):
        try:
            # IMPORTANT: Parameters are passed in alphabetical order by Supabase client
            # So this dict order doesn't matter - it will be called as (match_count, query_embedding)
            response = supabase.rpc(
                SUPABASE_MATCH_RPC,
                {
                    "match_count": int(limit),  # Explicit type casting
                    "query_embedding": vector,  # Already a list from OpenAI
                }
            ).execute()
            
            return response.data if response.data else []
            
        except Exception as e:
            last_error = e
            error_msg = str(e).lower()
            
            # Check for schema cache errors
            if "could not find the function" in error_msg or "schema cache" in error_msg:
                print(f"⚠️  RPC function '{SUPABASE_MATCH_RPC}' not found in schema cache.")
                print(f"   Error: {e}")
                print(f"   Verify the function exists in Supabase and parameters match alphabetical order.")
                
                # Don't retry on schema errors - they won't resolve automatically
                raise Exception(
                    f"RPC function '{SUPABASE_MATCH_RPC}' not found. "
                    f"Ensure it exists in Supabase with signature: "
                    f"(match_count int, query_embedding vector)"
                ) from e
            
            # Retry on transient errors
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"⚠️  RPC call failed (attempt {attempt + 1}/{max_retries}). Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"❌ RPC call failed after {max_retries} attempts: {e}")
                raise Exception(f"Failed to query Supabase RPC after {max_retries} attempts") from last_error
    
    return []


def semantic_search_hts(query, limit=5):
    """
    Perform semantic search on HTS knowledge base.
    
    Args:
        query: Search query string
        limit: Number of results to return
    
    Returns:
        List of matching HTS codes with metadata
    """
    vec = embed_text(query)
    return semantic_query(vec, limit)
