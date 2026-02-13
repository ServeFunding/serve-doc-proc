import io

import fitz  # PyMuPDF
import pytesseract
from PIL import Image


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract text from a PDF. Falls back to OCR for scanned/image PDFs."""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    pages_text: list[str] = []

    for page in doc:
        text = page.get_text()
        if text.strip():
            pages_text.append(text.strip())
        else:
            # Scanned page — render to image and OCR
            pix = page.get_pixmap(dpi=300)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            ocr_text = pytesseract.image_to_string(img)
            if ocr_text.strip():
                pages_text.append(ocr_text.strip())

    doc.close()
    return "\n\n".join(pages_text)


def extract_text_from_image(image_bytes: bytes) -> str:
    """Extract text from an image file using Tesseract OCR."""
    img = Image.open(io.BytesIO(image_bytes))
    return pytesseract.image_to_string(img).strip()


def extract_text(file_bytes: bytes, content_type: str) -> str:
    """Route to the correct extraction method based on content type."""
    if content_type == "application/pdf":
        return extract_text_from_pdf(file_bytes)
    elif content_type in ("image/png", "image/jpeg", "image/tiff", "image/bmp"):
        return extract_text_from_image(file_bytes)
    else:
        raise ValueError(f"Unsupported file type: {content_type}")
