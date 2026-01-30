import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv(".hts_dashboard/.env")
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_ROLE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def check_db_health():
    print("🏥 Checking Database Health...")
    
    # 1. Check Row Count
    resp = supabase.table("hts_knowledge_chunks").select("id", count="exact").limit(1).execute()
    print(f"✅ Total Rows: {resp.count}")
    
    # 2. Check for HNSW Index (indirectly via a fast search)
    # We'll try a search and see if it's fast (ms) or slow (s)
    dummy_vec = [0.1] * 1536
    
    import time
    start = time.time()
    try:
        resp = supabase.rpc("match_hts_chunks", {"match_count": 5, "query_embedding": dummy_vec}).execute()
        duration = time.time() - start
        print(f"⚡ Search Speed: {duration:.4f}s")
        if duration < 0.2:
            print("🚀 Index appears to be active (Fast search!)")
        else:
            print("🐢 Search is slow. Index might be missing or still building.")
    except Exception as e:
        print(f"❌ Search failed: {e}")

if __name__ == "__main__":
    check_db_health()
