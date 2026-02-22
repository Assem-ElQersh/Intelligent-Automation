"""
Lab 04 — PDF & OCR Processing
Entry point: processes all PDFs and images in data/input/,
extracts invoice fields, and exports results to data/output/invoices.csv.

Usage:
    # First generate sample invoices:
    python generate_sample_invoice.py

    # Then process them:
    python main.py
    python main.py --input ../data/input --output ../data/output
"""

import argparse
from pathlib import Path
import pandas as pd

from pdf_extractor import extract_text_from_pdf, parse_invoice_fields
from ocr_extractor import ocr_image, is_scanned_pdf, ocr_pdf

SUPPORTED_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif"}

BASE_DIR = Path(__file__).resolve().parent.parent


def process_file(path: Path) -> dict:
    """Process a single file (PDF or image) and return extracted fields."""
    print(f"  Processing: {path.name}")
    ext = path.suffix.lower()

    if ext == ".pdf":
        if is_scanned_pdf(path):
            print(f"    → Scanned PDF detected, using OCR...")
            text = ocr_pdf(path)
        else:
            print(f"    → Native PDF, using pdfplumber...")
            text = extract_text_from_pdf(path)
    elif ext in SUPPORTED_IMAGE_EXTS:
        print(f"    → Image file, using OCR...")
        text = ocr_image(path)
    else:
        print(f"    → Unsupported format, skipping.")
        return {}

    fields = parse_invoice_fields(text)
    fields["source_file"] = path.name
    return fields


def main() -> None:
    parser = argparse.ArgumentParser(description="Lab 04 — PDF & OCR Invoice Extractor")
    parser.add_argument("--input", type=Path, default=BASE_DIR / "data" / "input")
    parser.add_argument("--output", type=Path, default=BASE_DIR / "data" / "output")
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)

    input_files = [
        f for f in args.input.iterdir()
        if f.is_file() and f.suffix.lower() in {".pdf"} | SUPPORTED_IMAGE_EXTS
    ]

    if not input_files:
        print(f"No supported files found in {args.input}")
        print("Run 'python generate_sample_invoice.py' first.")
        return

    print(f"\n=== Lab 04: PDF & OCR Processing ===")
    print(f"Found {len(input_files)} file(s) to process.\n")

    records = []
    for f in sorted(input_files):
        result = process_file(f)
        if result:
            records.append(result)

    if records:
        df = pd.DataFrame(records)
        out_path = args.output / "invoices.csv"
        df.to_csv(out_path, index=False)
        print(f"\nExtracted {len(records)} record(s).")
        print(f"Results saved to: {out_path}")
        print("\n--- Preview ---")
        print(df[["source_file", "invoice_number", "date", "vendor", "total_due"]].to_string(index=False))
    else:
        print("No data extracted.")


if __name__ == "__main__":
    main()
