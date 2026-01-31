import os
import time
from supabase import create_client, Client
from utils.embeddings import embed_text
from dotenv import load_dotenv

# Try to load env vars from common locations
load_dotenv()
load_dotenv(".hts_dashboard/.env")

# Supabase configuration
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
SUPABASE_TABLE = os.environ.get("SUPABASE_TABLE", "hts_knowledge_chunks")
SUPABASE_MATCH_RPC = os.environ.get("SUPABASE_MATCH_RPC", "match_hts_chunks")

# Initialize Supabase client
if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    # This will be caught by the app, but we print for logs
    print("❌ ERROR: Supabase credentials missing in utils/search.py")
    supabase = None
else:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


def semantic_query(vector, limit=5, max_retries=3):
    """
    Query Supabase RPC function with vector similarity search.
    """
    if not supabase:
        raise Exception("Supabase client not initialized. Check your environment variables.")

    last_error = None
    
    for attempt in range(max_retries):
        try:
            # Call RPC with explicit parameter names
            # Alphabetical: match_count (m) comes before query_embedding (q)
            response = supabase.rpc(
                SUPABASE_MATCH_RPC,
                {
                    "match_count": int(limit),
                    "query_embedding": vector,
                }
            ).execute()
            
            return response.data if response.data else []
            
        except Exception as e:
            last_error = e
            print(f"⚠️ RPC attempt {attempt + 1} failed: {str(e)}")
            
            # Check for common configuration issues
            err_msg = str(e).lower()
            if "could not find the function" in err_msg or "schema cache" in err_msg:
                raise Exception(
                    f"RPC function '{SUPABASE_MATCH_RPC}' not found in Supabase. "
                    f"Please run the SQL script 'supabase_rpc_fix.sql' in your Supabase SQL Editor. "
                    "This is the most likely cause of search failure."
                ) from e
            
            if "dimensions of vector do not match" in err_msg:
                raise Exception(
                    f"Vector dimension mismatch. Check your EMBEDDING_DIM and 'vector(XXXX)' in SQL. "
                    f"Current vector length: {len(vector)}"
                ) from e

            # Retry on other errors (transient connection issues, etc.)
            if attempt < max_retries - 1:
                time.sleep(1)
            else:
                # Last attempt failed, raise with full context
                print(f"❌ RPC search failed after {max_retries} attempts.")
                raise e
    
    return []


def semantic_search_hts(query, limit=5):
    """
    Perform semantic search on HTS knowledge base.
    """
    try:
        vec = embed_text(query)
        return semantic_query(vec, limit)
    except Exception as e:
        # Re-raise to show in Streamlit UI
        raise e
