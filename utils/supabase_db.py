# utils/supabase_db.py

import os
from supabase import create_client, Client
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUPABASE_TABLE = os.getenv("SUPABASE_TABLE", "hts_knowledge_chunks")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)


def get_all_chunks(limit=50):
    """Get all chunks from the database with a limit."""
    return supabase.table(SUPABASE_TABLE).select("*").limit(limit).execute()


def get_hts_page(page: int = 1, page_size: int = 20):
    """
    Get a paginated list of HTS codes from the database.
    
    Args:
        page: Page number (1-indexed)
        page_size: Number of results per page
    
    Returns:
        List of HTS code records
    """
    offset = (page - 1) * page_size
    
    try:
        response = supabase.table(SUPABASE_TABLE)\
            .select("id, hts_code, title, normalized_text")\
            .order("hts_code")\
            .range(offset, offset + page_size - 1)\
            .execute()
        
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching HTS page: {e}")
        return []


def count_hts_rows():
    """
    Count the total number of HTS codes in the database.
    
    Returns:
        Total count of records
    """
    try:
        # Supabase doesn't have a direct count, so we use select with count
        response = supabase.table(SUPABASE_TABLE)\
            .select("id", count="exact")\
            .limit(1)\
            .execute()
        
        return response.count if hasattr(response, 'count') else 0
    except Exception as e:
        print(f"Error counting HTS rows: {e}")
        # Return a reasonable default if count fails
        return 35000
