import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv(".hts_dashboard/.env")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def deep_check():
    print("🔬 Deep Checking 'hts_knowledge_chunks'...")
    try:
        # Try a direct select without count
        resp = supabase.table("hts_knowledge_chunks").select("id").limit(10).execute()
        print(f"✅ Select response data length: {len(resp.data)}")
        if resp.data:
            print(f"✅ Samples: {resp.data}")
        else:
            print("⚠️ Select returned empty list.")
            
        # Try to guess other table names
        possible_tables = ["hts_codes", "hts_data", "hts_chunks_v2", "hts_vectors"]
        for t in possible_tables:
            try:
                r = supabase.table(t).select("id").limit(1).execute()
                print(f"✅ Table '{t}' FOUND with {len(r.data)} rows in sample.")
            except:
                pass

    except Exception as e:
        print(f"❌ Deep check failed: {e}")

if __name__ == "__main__":
    deep_check()
