import os
from supabase import create_client
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(".hts_dashboard/.env")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)

def run_test_search():
    query = "live horses"
    print(f"🔍 Testing semantic search for: '{query}'")
    
    # 1. Embed text
    try:
        resp = client.embeddings.create(
            model="text-embedding-3-small",
            input=query
        )
        vec = resp.data[0].embedding
        print(f"✅ Generated embedding (dim: {len(vec)})")
    except Exception as e:
        print(f"❌ OpenAI embedding failed: {e}")
        return

    # 2. Call RPC
    try:
        # Try both common names
        for rpc_name in ["match_hts_chunks", "match_chunks"]:
            print(f"\n📡 Calling RPC: {rpc_name}...")
            try:
                response = supabase.rpc(
                    rpc_name,
                    {
                        "query_embedding": vec,
                        "match_count": 5,
                    }
                ).execute()
                
                if response.data:
                    print(f"✅ Found {len(response.data)} results using '{rpc_name}':")
                    for i, r in enumerate(response.data):
                        print(f"  {i+1}. [{r.get('hts_code', 'N/A')}] {r.get('title', 'N/A')[:100]}")
                else:
                    print(f"⚠️ No results found using '{rpc_name}'.")
            except Exception as e:
                print(f"❌ RPC error with '{rpc_name}': {e}")
                
    except Exception as e:
        print(f"❌ Search logic failed: {e}")

if __name__ == "__main__":
    run_test_search()
