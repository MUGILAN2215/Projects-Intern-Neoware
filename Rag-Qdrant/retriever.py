from embedder import get_embedding
from qdrant_store import search


def retrieve(question, top_k=5, doc_id=None):
    """
    Embeds the question, searches Qdrant, and returns a list of
    dicts: [{ "text": ..., "score": ..., "type": ..., "filename": ... }]
    """
    query_vector = get_embedding(question)
    results = search(query_vector, top_k=top_k, doc_id=doc_id)

    retrieved = []
    for r in results:
        retrieved.append({
            "text": r.payload["text"],
            "score": r.score,
            "type": r.payload.get("type", "text"),
            "filename": r.payload.get("filename", "unknown"),
        })
    return retrieved


if __name__ == "__main__":
    question = "What is AKS?"
    results = retrieve(question, top_k=3)

    print(f"Question: {question}\n")
    for i, r in enumerate(results):
        print(f"--- Match {i + 1} (score: {r['score']:.4f}, type: {r['type']}) ---")
        print(r["text"][:200])
        print()
