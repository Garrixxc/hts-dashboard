import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

EMBEDDING_MODEL = os.environ["EMBEDDING_MODEL"]
EMBEDDING_DIM = int(os.environ["EMBEDDING_DIM"])

def embed_text(text: str):
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    vector = response.data[0].embedding

    # safety check
    if len(vector) != EMBEDDING_DIM:
        raise ValueError(f"Embedding dimension mismatch: expected {EMBEDDING_DIM}, got {len(vector)}")

    return vector
