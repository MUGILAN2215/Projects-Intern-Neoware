import os
import time
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))

GEN_MODEL = "gemini-2.5-flash"


def generate_answer(question, retrieved_chunks, retries=3):
    """
    Takes the question + retrieved chunks, builds a grounded prompt,
    and asks Gemini to answer using ONLY that context.
    tools=[] prevents automatic function calling from silently
    ignoring the provided context (the grounding-failure bug from
    the original project).
    """
    print("\n--- RETRIEVED CHUNKS (debug) ---")
    for i, chunk in enumerate(retrieved_chunks):
        print(f"[{i}] ({chunk.get('type', 'text')}) {chunk['text'][:100]}...")

    context = "\n\n".join(c["text"] for c in retrieved_chunks)

    prompt = f"""Answer the question using ONLY the context below.
If the answer isn't in the context, say "I don't have that information."

Context:
{context}

Question: {question}

Answer:"""

    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=GEN_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0, tools=[])
            )
            return response.text
        except Exception as e:
            print(f"Generation attempt {attempt + 1} failed: {e}")
            time.sleep(2 ** attempt)

    raise Exception("Generation failed after retries")


if __name__ == "__main__":
    # quick standalone test with fake retrieved chunks
    fake_chunks = [
        {"text": "AKS is a managed Kubernetes service that simplifies deploying, managing, and scaling containerized applications.", "type": "text"}
    ]
    answer = generate_answer("What is AKS?", fake_chunks)
    print("\n--- ANSWER ---")
    print(answer)
