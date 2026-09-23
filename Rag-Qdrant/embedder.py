import os
import time
from google import genai

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))

EMBED_MODEL = "gemini-embedding-001"


def get_embedding(text, retries=3):
    """
    Converts a piece of text into a 3072-dimension vector using Gemini's
    embedding model. Retries with backoff on transient failures (e.g. 503s).
    """
    for attempt in range(retries):
        try:
            result = client.models.embed_content(model=EMBED_MODEL, contents=text)
            return result.embeddings[0].values
        except Exception as e:
            print(f"Embedding attempt {attempt + 1} failed: {e}")
            time.sleep(2 ** attempt)  # exponential backoff: 1s, 2s, 4s

    raise Exception("Embedding failed after retries")


def embed_chunks(chunks):
    """
    Takes a list of chunk dicts (each with a "text" key) and adds
    an "embedding" key to each one, in place. Returns the same list.
    """
    for i, chunk in enumerate(chunks):
        print(f"Embedding chunk {i + 1}/{len(chunks)} (type: {chunk.get('type', 'text')})")
        chunk["embedding"] = get_embedding(chunk["text"])
    return chunks


if __name__ == "__main__":
    # quick standalone test
    sample_chunks = [
        {"text": "Kubernetes is an open-source container orchestration platform.", "type": "text"},
        {"text": "AKS is a managed Kubernetes service.", "type": "text"},
    ]
    result = embed_chunks(sample_chunks)
    for c in result:
        print(f"\nText: {c['text'][:60]}...")
        print(f"Vector length: {len(c['embedding'])}")
