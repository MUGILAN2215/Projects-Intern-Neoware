"""
main.py — runs the full RAG pipeline end to end:

    Load (text + images) -> Chunk (text) + Caption (images)
    -> Combine -> Embed -> Store (Qdrant) -> Retrieve -> Generate

Run this after Qdrant is up (docker run ... qdrant/qdrant) and
GEMINI_API_KEY is set in your .env file.
"""

import os
from dotenv import load_dotenv

load_dotenv()  # reads .env and sets environment variables

from loader import load_pdf_text, load_pdf_images
from chunker import chunk_semantically
from image_processor import process_images
from embedder import embed_chunks
from qdrant_store import ensure_collection, store_chunks
from retriever import retrieve
from generator import generate_answer

PDF_PATH = "sample.pdf"
DOC_ID = "sample_doc"  # change this per document once you support multiple PDFs


def build_pipeline():
    """
    Load -> Chunk -> Caption -> Combine -> Embed -> Store.
    Run this once per new document.
    """
    print("=" * 50)
    print("PHASE 1: LOAD")
    print("=" * 50)
    text = load_pdf_text(PDF_PATH)
    image_paths = load_pdf_images(PDF_PATH)
    print(f"Loaded {len(text)} characters of text and {len(image_paths)} images")

    print("\n" + "=" * 50)
    print("PHASE 2: CHUNK (text) + CAPTION (images)")
    print("=" * 50)
    text_chunks_raw = chunk_semantically(text)
    text_chunks = [{"text": t, "type": "text"} for t in text_chunks_raw]
    print(f"Created {len(text_chunks)} text chunks")

    image_chunks = process_images(image_paths)
    print(f"Created {len(image_chunks)} image caption chunks")

    print("\n" + "=" * 50)
    print("COMBINE")
    print("=" * 50)
    all_chunks = text_chunks + image_chunks
    print(f"Total combined chunks: {len(all_chunks)}")

    print("\n" + "=" * 50)
    print("PHASE 3: EMBED")
    print("=" * 50)
    all_chunks = embed_chunks(all_chunks)

    print("\n" + "=" * 50)
    print("PHASE 4: STORE (Qdrant)")
    print("=" * 50)
    ensure_collection()
    store_chunks(all_chunks, doc_id=DOC_ID, filename=PDF_PATH)

    print("\nPipeline build complete. Data is now in Qdrant.")


def ask(question, top_k=5):
    """
    Phase 5 + 6: Retrieve -> Generate.
    Call this as many times as you want once build_pipeline() has run.
    """
    print("=" * 50)
    print("PHASE 5: RETRIEVE")
    print("=" * 50)
    results = retrieve(question, top_k=top_k, doc_id=DOC_ID)
    for i, r in enumerate(results):
        print(f"[{i}] (score: {r['score']:.4f}, type: {r['type']}) {r['text'][:100]}...")

    print("\n" + "=" * 50)
    print("PHASE 6: GENERATE")
    print("=" * 50)
    answer = generate_answer(question, results)

    print("\n--- FINAL ANSWER ---")
    print(answer)
    return answer

from qdrant_store import ensure_collection

if __name__ == "__main__":
    already_exists = ensure_collection()
    if not already_exists:
        build_pipeline()
    else:
        print("Skipping build — data already in Qdrant.")

    # ask("What components are shown in the control plane diagram?")
    # ask("What is Kubernetes?")
    # ask("What operating systems does AKS support for Linux node pools?")
    # ask("What does the namespace diagram show?")
    # ask("What storage options does a container connect to in the node architecture?")
    # ask("What is the price of AKS per month?")
    ask("Who is the CEO of Microsoft?")