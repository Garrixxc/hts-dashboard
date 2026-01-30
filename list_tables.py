import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv(".hts_dashboard/.env")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def list_schema():
    print("📋 Listing tables in public schema...")
    try:
        # We can't easily list tables via the client without a direct Postgres query
        # but we can try to hit some likely names and see what works, 
        # or use a generic select from pg_catalog if we have enough permissions.
        # However, the easiest way with the client is to try a known table.
        
        tables = ["hts_knowledge_chunks", "hts_chunks", "knowledge_chunks", "hts"]
        for t in tables:
            try:
                resp = supabase.table(t).select("id", count="exact").limit(1).execute()
                print(f"✅ Table '{t}' found. Row count: {resp.count}")
            except Exception as e:
                if "does not exist" in str(e):
                    print(f"❌ Table '{t}' does not exist.")
                else:
                    print(f"⚠️ Table '{t}' error: {e}")
                    
    except Exception as e:
        print(f"❌ Schema check failed: {e}")

if __name__ == "__main__":
    list_schema()
