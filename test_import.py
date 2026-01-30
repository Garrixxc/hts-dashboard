import os
import json
import time
from typing import List, Dict
from openai import OpenAI
from supabase import create_client, Client
from dotenv import load_dotenv

# ---- Config ----
load_dotenv(".hts_dashboard/.env")
MODEL = os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small")
JSON_PATH = "../hts_2026_basic_edition_json.json"

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def flatten_hts_item(item: Dict) -> str:
    parts = [
        f"HTS: {item.get('htsno','')}",
        f"Indent: {item.get('indent','')}",
        f"Description: {item.get('description','')}",
        f"General Duty: {item.get('general','')}",
        f"Special Duty: {item.get('special','')}",
        f"Other Duty: {item.get('other','')}",
    ]
    return " | ".join([p for p in parts if str(p).strip() != ""])

def embed_test_batch(texts: List[str]):
    resp = client.embeddings.create(model=MODEL, input=texts)
    return [d.embedding for d in resp.data]

def test_import():
    print("🚀 Starting Test Import (5 rows)...")
    try:
        with open(JSON_PATH, "r") as f:
            data = json.load(f)
        
        test_items = data[:5]
        texts = [flatten_hts_item(item) for item in test_items]
        embeddings = embed_test_batch(texts)
        
        rows = []
        for item, emb, txt in zip(test_items, embeddings, texts):
            rows.append({
                "hts_code": item.get("htsno",""),
                "title": (item.get("description") or "").strip(),
                "normalized_text": txt,
                "embedding": emb,
            })
            
        print(f"📦 Inserting {len(rows)} rows into Supabase...")
        resp = supabase.table("hts_knowledge_chunks").insert(rows).execute()
        print(f"✅ Success! Response data length: {len(resp.data)}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_import()
