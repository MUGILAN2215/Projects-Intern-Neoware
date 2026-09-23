import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))


def describe_image(image_path, retries=3):
    """
    Sends an image to Gemini Vision, asks it to describe the image
    AND extract any visible text (OCR-style) in one go.
    Returns a text description.
    """
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    ext = image_path.split(".")[-1].lower()
    mime_type = f"image/{'jpeg' if ext == 'jpg' else ext}"

    prompt = """Describe what this image shows in 2-3 sentences.
If there is any readable text in the image, include it exactly as written.
Focus on information that would be useful to someone searching a document."""

    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                    prompt
                ],
                config=types.GenerateContentConfig(tools=[])
            )
            return response.text
        except Exception as e:
            print(f"Image description attempt {attempt + 1} failed: {e}")

    raise Exception("Image description failed after retries")


def process_images(image_paths):
    """
    Takes a list of image file paths, returns a list of dicts:
    [{ "text": <description>, "source_image": <path>, "type": "image_caption" }]
    """
    results = []
    for path in image_paths:
        print(f"Processing image: {path}")
        description = describe_image(path)
        results.append({
            "text": description,
            "source_image": path,
            "type": "image_caption"
        })
    return results


if __name__ == "__main__":
    from loader import load_pdf_images

    pdf_path = "sample.pdf"
    image_paths = load_pdf_images(pdf_path)
    print(f"Found {len(image_paths)} images to process\n")

    image_data = process_images(image_paths)

    for item in image_data:
        print(f"\n--- {item['source_image']} ---")
        print(item['text'])
