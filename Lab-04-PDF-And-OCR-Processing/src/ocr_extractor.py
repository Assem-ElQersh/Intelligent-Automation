"""
Lab 04 — PDF & OCR Processing
Extracts text from scanned/image-based PDFs and image files using pytesseract OCR.
"""

from pathlib import Path
from PIL import Image
import pytesseract

try:
    from pdf2image import convert_from_path
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False


def _preprocess_image(img: Image.Image) -> Image.Image:
    """Convert to grayscale for better OCR accuracy."""
    return img.convert("L")


def ocr_image(image_path: Path) -> str:
    """Run OCR on a single image file."""
    img = Image.open(image_path)
    img = _preprocess_image(img)
    text = pytesseract.image_to_string(img, config="--psm 6")
    return text.strip()


def ocr_pdf(pdf_path: Path, dpi: int = 200) -> str:
    """
    Convert each page of a PDF to an image and run OCR.
    Requires poppler to be installed (pdf2image dependency).
    """
    if not PDF2IMAGE_AVAILABLE:
        raise RuntimeError(
            "pdf2image is not installed or poppler is missing. "
            "Install with: pip install pdf2image\n"
            "And on Linux: sudo apt install poppler-utils"
        )

    pages = convert_from_path(str(pdf_path), dpi=dpi)
    all_text = []
    for i, page_img in enumerate(pages, start=1):
        processed = _preprocess_image(page_img)
        page_text = pytesseract.image_to_string(processed, config="--psm 6")
        if page_text.strip():
            all_text.append(f"--- Page {i} ---\n{page_text.strip()}")

    return "\n\n".join(all_text)


def is_scanned_pdf(pdf_path: Path) -> bool:
    """
    Heuristic: if pdfplumber extracts < 50 chars, assume it's a scanned PDF.
    """
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            text = "".join(
                (p.extract_text() or "") for p in pdf.pages
            )
        return len(text.strip()) < 50
    except Exception:
        return True
