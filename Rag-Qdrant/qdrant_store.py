from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, Filter, FieldCondition, MatchValue

COLLECTION_NAME = "documents"
VECTOR_SIZE = 3072  # matches gemini-embedding-001 output size

client = QdrantClient(host="localhost", port=6333)


def ensure_collection():
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in existing:
        print(f"Creating collection '{COLLECTION_NAME}'...")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
        )
        return False  # collection is new, needs data
    else:
        print(f"Collection '{COLLECTION_NAME}' already exists — reusing it.")
        return True  # collection already has data


def store_chunks(chunks, doc_id, filename, start_id=0):
    """
    Upserts a list of chunk dicts (each must have "text", "embedding", "type")
    into Qdrant, tagged with doc_id and filename metadata.
    Returns the next available id (so multiple documents don't overwrite each other).
    """
    points = []
    for i, chunk in enumerate(chunks):
        point_id = start_id + i
        payload = {
            "text": chunk["text"],
            "doc_id": doc_id,
            "filename": filename,
            "type": chunk.get("type", "text"),
        }
        if "source_image" in chunk:
            payload["source_image"] = chunk["source_image"]

        points.append(
            PointStruct(id=point_id, vector=chunk["embedding"], payload=payload)
        )

    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"Stored {len(points)} points for doc_id='{doc_id}'")
    return start_id + len(points)


def search(query_vector, top_k=5, doc_id=None):
    """
    Searches Qdrant for the top_k closest points to query_vector.
    Optionally filter to a single doc_id.
    Uses query_points (the current API) instead of the deprecated search().
    """
    query_filter = None
    if doc_id:
        query_filter = Filter(
            must=[FieldCondition(key="doc_id", match=MatchValue(value=doc_id))]
        )

    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        query_filter=query_filter,
        limit=top_k
    )
    return response.points


if __name__ == "__main__":
    # quick standalone check — confirms Qdrant is reachable and collection exists
    ensure_collection()
    info = client.get_collection(COLLECTION_NAME)
    print(f"\nCollection '{COLLECTION_NAME}' ready.")
    print(f"Vector size: {info.config.params.vectors.size}")
    print(f"Points stored so far: {info.points_count}")
