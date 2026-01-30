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
BATCH_SIZE = 128
JSON_PATH = "../hts_2026_basic_edition_json.json" # Adjusting path for local execution

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---- Helpers ----

def flatten_hts_item(item: Dict) -> str:
    parts = [
        f"HTS: {item.get('htsno','')}",
        f"Indent: {item.get('indent','')}",
        f"Description: {item.get('description','')}",
        f"General Duty: {item.get('general','')}",
        f"Special Duty: {item.get('special','')}",
        f"Other Duty: {item.get('other','')}",
    ]
    return " | ".join([p for p in parts if p.strip() != ""])

def chunk_list(seq: List, size: int):
    for i in range(0, len(seq), size):
        yield i, seq[i:i+size]

def embed_batch(texts: List[str]):
    for attempt in range(5):
        try:
            resp = client.embeddings.create(
                model=MODEL,
                input=texts
            )
            return [d.embedding for d in resp.data]
        except Exception as e:
            wait = 2 ** attempt
            print(f"[embed_batch] Error: {e}. Retrying in {wait}s...")
            time.sleep(wait)
    raise RuntimeError("Failed to embed after retries")

def insert_batch(rows: List[Dict]):
    for attempt in range(5):
        try:
            supabase.table("hts_knowledge_chunks").insert(rows).execute()
            return
        except Exception as e:
            wait = 2 ** attempt
            print(f"[insert_batch] Error: {e}. Retrying in {wait}s...")
            time.sleep(wait)
    raise RuntimeError("Insert failed")

# ---- Main ----

def main():
    with open(JSON_PATH, "r") as f:
        data = json.load(f)

    total = len(data)
    print(f"Loaded {total} HTS records.")

    for start, batch_items in chunk_list(data, BATCH_SIZE):

        texts = [flatten_hts_item(item) for item in batch_items]
        embeddings = embed_batch(texts)

        rows = []
        for item, emb, txt in zip(batch_items, embeddings, texts):
            rows.append({
                "hts_code": item.get("htsno",""),
                "title": (item.get("description") or "").strip(),
                "normalized_text": txt,
                "embedding": emb,
            })

        insert_batch(rows)

        done = start + len(batch_items)
        print(f"Inserted {done}/{total} rows ({done*100/total:.2f}%)")

    print("Done! KB built successfully.")

if __name__ == "__main__":
    main()

