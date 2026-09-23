import re
import os
import numpy as np
from google import genai

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))


def split_into_sentences(text):
    """Simple sentence splitter."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def get_embedding(text):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return np.array(result.embeddings[0].values)


def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def chunk_semantically(text, similarity_threshold=0.65):
    """
    Splits text into chunks based on meaning shifts.
    Consecutive sentences are grouped together as long as they stay
    semantically similar. A drop in similarity below the threshold
    starts a new chunk.
    """
    sentences = split_into_sentences(text)
    if len(sentences) == 0:
        return []

    print(f"Total sentences: {len(sentences)}")
    print("Embedding sentences... (this calls the API, may take a bit)")

    embeddings = [get_embedding(s) for s in sentences]

    chunks = []
    current_chunk = [sentences[0]]

    for i in range(1, len(sentences)):
        sim = cosine_similarity(embeddings[i - 1], embeddings[i])

        if sim < similarity_threshold:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentences[i]]
        else:
            current_chunk.append(sentences[i])

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


if __name__ == "__main__":
    from loader import load_pdf_text

    pdf_path = "sample.pdf"
    text = load_pdf_text(pdf_path)

    chunks = chunk_semantically(text)

    print(f"\nTotal chunks created: {len(chunks)}")
    print(f"Total characters in original text: {len(text)}")
    print(f"Total characters across all chunks: {sum(len(c) for c in chunks)}")

    for i, chunk in enumerate(chunks):
        print(f"\n--- Chunk {i} (length: {len(chunk)}) ---")
        print(chunk[:150])
