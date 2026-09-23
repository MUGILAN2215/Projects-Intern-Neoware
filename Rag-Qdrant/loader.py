import pymupdf as fitz  # package installed is "pymupdf", this avoids the deprecated `fitz` import warning
import os


def load_pdf_text(pdf_path):
    """
    Opens a PDF and extracts all text, page by page.
    Returns one big string of raw text.
    """
    doc = fitz.open(pdf_path)
    full_text = ""

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        full_text += text + "\n"

    doc.close()
    return full_text


def load_pdf_images(pdf_path, output_folder="extracted_images"):
    """
    Extracts embedded images from a PDF, saves them as image files.
    Returns a list of saved image file paths.
    """
    os.makedirs(output_folder, exist_ok=True)

    doc = fitz.open(pdf_path)
    image_paths = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        images = page.get_images(full=True)

        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]

            image_filename = f"{output_folder}/page{page_num}_img{img_index}.{ext}"
            with open(image_filename, "wb") as f:
                f.write(image_bytes)

            image_paths.append(image_filename)

    doc.close()
    return image_paths


if __name__ == "__main__":
    pdf_path = "sample.pdf"

    text = load_pdf_text(pdf_path)
    print(f"Extracted {len(text)} characters of text")

    images = load_pdf_images(pdf_path)
    print(f"Extracted {len(images)} images")
    for img_path in images:
        print(f" - {img_path}")
