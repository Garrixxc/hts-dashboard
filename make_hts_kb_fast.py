import os
import json
import time
from typing import List, Dict

from openai import OpenAI
from supabase import create_client, Client

# ---------- Config ----------
MODEL = "text-embedding-3-large"   # 3072-dim
BATCH_SIZE = 128                   # tune between 64–256
JSON_PATH = "hts_2026_basic_edition_json.json"

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# ---------- Helpers ----------

def flatten_hts_item(item: Dict) -> str:
    """Turn one HTS JSON object into a single text string."""
    parts = [
        f"HTS: {item.get('htsno', '')}",
        f"Indent: {item.get('indent', '')}",
        f"Description: {item.get('description', '')}",
        f"General Duty: {item.get('general', '')}",
        f"Special Duty: {item.get('special', '')}",
        f"Other Duty: {item.get('other', '')}",
    ]

    # Optional footnotes
    fns = item.get("footnotes") or []
    if isinstance(fns, list) and len(fns) > 0:
        fn_texts = [fn.get("value", "") for fn in fns if isinstance(fn, dict)]
        if fn_texts:
            parts.append("Footnotes: " + " | ".join(fn_texts))

    return " | ".join(p for p in parts if p and str(p).strip() != "")


def chunk_list(seq: List, size: int):
    """Yield successive chunks from a list."""
    for i in range(0, len(seq), size):
        yield i, seq[i:i + size]


def embed_batch(texts: List[str]) -> List[List[float]]:
    """Call OpenAI once for a batch of texts, with retry."""
    for attempt in range(5):
        try:
            resp = client.embeddings.create(
                model=MODEL,
                input=texts,
            )
            # resp.data is in same order as input
            return [d.embedding for d in resp.data]
        except Exception as e:
            wait = 2 ** attempt
            print(f"[embed_batch] Error: {e}. Retrying in {wait}s...")
            time.sleep(wait)
    raise RuntimeError("Failed to embed batch after 5 attempts")


def insert_batch(rows: List[Dict]):
    """Bulk insert into Supabase with basic retry."""
    if not rows:
        return
    for attempt in range(5):
        try:
            supabase.table("hts_knowledge_chunks").insert(rows).execute()
            return
        except Exception as e:
            wait = 2 ** attempt
            print(f"[insert_batch] Error: {e}. Retrying in {wait}s...")
            time.sleep(wait)
    raise RuntimeError("Failed to insert batch after 5 attempts")


# ---------- Main ----------

def main():
    # 1) Load JSON
    with open(JSON_PATH, "r") as f:
        data = json.load(f)

    total = len(data)
    print(f"Loaded {total} HTS records from {JSON_PATH}")

    # 2) Process in batches
    for start_idx, batch_items in chunk_list(data, BATCH_SIZE):
        # Prepare texts
        texts = [flatten_hts_item(item) for item in batch_items]

        # 2a) Get embeddings for this batch
        embeddings = embed_batch(texts)

        # 2b) Build rows for Supabase
        rows = []
        for item, emb, text in zip(batch_items, embeddings, texts):
            code = item.get("htsno", None)
            title = (item.get("description") or "").strip()

            rows.append({
                "hts_code": code,
                "title": title,
                "source_type": "hts",
                "source_ref": code,
                "normalized_text": text,
                "embedding": emb,
            })

        # 2c) Insert rows
        insert_batch(rows)

        done = start_idx + len(batch_items)
        print(f"Inserted {done}/{total} rows ({done * 100 / total:.2f}%)")

    print("✅ Finished building HTS knowledge base.")


if __name__ == "__main__":
    main()

