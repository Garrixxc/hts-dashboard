import os
import time
import numpy as np
from tqdm import tqdm
from supabase import create_client
from openai import OpenAI

from dotenv import load_dotenv

# -------------------------------
#  CONFIG
# -------------------------------
load_dotenv(".hts_dashboard/.env")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

TABLE_NAME = os.getenv("SUPABASE_TABLE", "hts_knowledge_chunks")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", "1536"))
BATCH_SIZE = 50  # number of rows to update per batch

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY or not OPENAI_API_KEY:
    raise RuntimeError("Set SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, OPENAI_API_KEY env vars before running.")


# -------------------------------
#  INIT CLIENTS
# -------------------------------
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)


def normalize(vec):
    arr = np.array(vec, dtype=np.float32)
    norm = np.linalg.norm(arr)
    if norm == 0:
        return arr.tolist()
    return (arr / norm).tolist()


def fetch_total_rows():
    # just get count
    resp = supabase.table(TABLE_NAME).select("id", count="exact").limit(1).execute()
    return resp.count


def fetch_batch(offset, limit):
    """
    Returns list of rows with fields: id, normalized_text
    """
    resp = (
        supabase.table(TABLE_NAME)
        .select("id, normalized_text")
        .order("id", desc=False)
        .range(offset, offset + limit - 1)
        .execute()
    )
    return resp.data


def embed_texts(texts):
    """
    Call OpenAI embeddings in batch.
    """
    resp = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts,
    )
    return [item.embedding for item in resp.data]


def main():
    total = fetch_total_rows()
    print(f"Found {total} rows in {TABLE_NAME} to (re)embed.")

    num_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE

    for batch_idx in tqdm(range(num_batches), desc="Rebuilding embeddings"):
        offset = batch_idx * BATCH_SIZE
        rows = fetch_batch(offset, BATCH_SIZE)
        if not rows:
            continue

        texts = [row["normalized_text"] or "" for row in rows]
        ids = [row["id"] for row in rows]

        try:
            raw_embeddings = embed_texts(texts)
        except Exception as e:
            print(f"\n❌ Embedding API error at batch {batch_idx}: {e}")
            time.sleep(3)
            continue

        updates = []
        for rid, emb in zip(ids, raw_embeddings):
            emb_norm = normalize(emb)
            if len(emb_norm) != EMBEDDING_DIM:
                print(
                    f"⚠️ Dimension mismatch for id {rid}: "
                    f"got {len(emb_norm)}, expected {EMBEDDING_DIM}"
                )
            updates.append(
                {
                    "id": rid,
                    "embedding": emb_norm,
                }
            )

        # Bulk update (Supabase client handles batch upserts/updates)
        try:
            supabase.table(TABLE_NAME).upsert(updates).execute()
        except Exception as e:
            print(f"\n❌ Bulk update error for batch {batch_idx}: {e}")
            # Fallback to individual updates if bulk fails
            for row in updates:
                try:
                    supabase.table(TABLE_NAME).update(
                        {"embedding": row["embedding"]}
                    ).eq("id", row["id"]).execute()
                except Exception as e:
                    print(f"❌ Individual update error for id {row['id']}: {e}")
                time.sleep(1)

        # small sleep to avoid hammering the DB
        time.sleep(0.1)

    print("\n✅ Finished rebuilding embeddings.")


if __name__ == "__main__":
    main()
