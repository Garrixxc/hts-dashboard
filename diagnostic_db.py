import os
from supabase import create_client
import numpy as np

from dotenv import load_dotenv

# Use the same env vars as the app
load_dotenv(".hts_dashboard/.env")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    print("❌ Error: SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY not set.")
    exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def run_diagnostic():
    print("🚀 Starting HTS Database Diagnostic...")
    
    # 1. Check Table Schema & Sample Row
    print("\n🔍 Checking 'hts_knowledge_chunks' schema...")
    try:
        # Get one row to check structure
        resp = supabase.table("hts_knowledge_chunks").select("*").limit(1).execute()
        if not resp.data:
            print("❌ Error: No data found in 'hts_knowledge_chunks'")
            return
        
        row = resp.data[0]
        print(f"✅ Table exists. Columns found: {list(row.keys())}")
        
        # 2. Check Embedding Type & Dimension
        emb = row.get("embedding")
        if emb is None:
            print("❌ Error: 'embedding' column is NULL in sample row.")
        else:
            if isinstance(emb, str):
                # If it's a string representation of a vector
                import json
                try:
                    emb_list = json.loads(emb)
                    print(f"✅ Embedding is a JSON string. Dimension: {len(emb_list)}")
                except:
                    print(f"⚠️ Embedding is a string but not JSON: {emb[:50]}...")
            elif isinstance(emb, list):
                print(f"✅ Embedding is a list. Dimension: {len(emb)}")
            else:
                print(f"⚠️ Embedding is unknown type: {type(emb)}")

        # 3. Row Counts
        print("\n📊 Checking row counts...")
        count_resp = supabase.table("hts_knowledge_chunks").select("id", count="exact").limit(1).execute()
        total_rows = count_resp.count
        print(f"✅ Total rows: {total_rows}")

        # 4. Dimension Consistency Check
        print("\n📏 Checking for dimension inconsistencies...")
        # Check for rows that are NOT 1536
        # Note: Supabase/Postgres vector extension doesn't easily allow len(vector) in the basic select
        # but we can try to fetch a few to see if they vary
        samples = supabase.table("hts_knowledge_chunks").select("id, embedding").limit(10).execute()
        dims = []
        for s in samples.data:
            e = s.get("embedding")
            if e:
                # Supabase Python client usually returns list for vector
                dims.append(len(e) if isinstance(e, list) else -1)
        
        print(f"✅ Sample dimensions: {set(dims)}")
        if len(set(dims)) > 1:
            print("⚠️ WARNING: Multiple embedding dimensions found in samples!")

    except Exception as e:
        print(f"❌ Diagnostic failed: {e}")

if __name__ == "__main__":
    run_diagnostic()
