# Lab 04 — PDF & OCR Document Processing

**Pillar:** RPA + AI  
**Difficulty:** Intermediate  
**Estimated Time:** 45–60 minutes

---

## Objective

Build an intelligent document processor that:
- Automatically detects whether a PDF is native (text-based) or scanned (image-based)
- Extracts text using `pdfplumber` (native) or `pytesseract` OCR (scanned)
- Parses invoice fields (invoice number, date, vendor, total) using regex
- Exports all extracted data to a structured CSV

This demonstrates **Intelligent Document Processing (IDP)** — the bridge between RPA and AI.

---

## Concepts Covered

| Concept | Description |
|---------|-------------|
| PDF text extraction | Extracting structured text from native PDFs |
| OCR | Converting scanned images/PDFs to machine-readable text |
| Regex parsing | Extracting named fields from unstructured text |
| Document heuristics | Auto-detecting PDF type (native vs. scanned) |
| Batch processing | Processing a folder of documents automatically |

---

## Project Structure

```
Lab-04-PDF-And-OCR-Processing/
├── README.md
├── requirements.txt
├── src/
│   ├── generate_sample_invoice.py  # Creates test PDF invoices
│   ├── pdf_extractor.py            # pdfplumber text + table extraction
│   ├── ocr_extractor.py            # pytesseract OCR for images and scanned PDFs
│   └── main.py                     # Entry point: process folder → CSV
└── data/
    ├── input/                      # Place PDF/image files here
    └── output/
        └── invoices.csv            # Extracted invoice data
```

---

## System Requirements

```bash
# Tesseract OCR engine (required for OCR)
sudo apt install tesseract-ocr

# Poppler utilities (required for PDF → image conversion)
sudo apt install poppler-utils
```

---

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Usage

### Step 1: Generate sample invoices

```bash
cd src
python generate_sample_invoice.py
```

This creates two PDF invoices in `data/input/`.

### Step 2: Extract invoice data

```bash
python main.py
```

The script:
1. Scans `data/input/` for PDF and image files
2. Auto-detects native vs. scanned PDFs
3. Extracts text with the appropriate method
4. Parses invoice fields with regex
5. Saves results to `data/output/invoices.csv`

### Custom input/output directories

```bash
python main.py --input /path/to/docs --output /path/to/results
```

---

## How It Works

```
data/input/invoice_001.pdf
        │
        ▼ [ocr_extractor.is_scanned_pdf()]
   Native PDF? → pdfplumber   OR   Scanned? → pdf2image + pytesseract
        │
        ▼ [pdf_extractor.parse_invoice_fields()]
   regex → invoice_number, date, due_date, vendor, client, total_due
        │
        ▼ pandas DataFrame
   data/output/invoices.csv
```

### Extracted Fields

| Field | Description |
|-------|-------------|
| `invoice_number` | INV-2024-001 |
| `date` | Invoice issue date |
| `due_date` | Payment due date |
| `vendor` | Issuing company name |
| `client` | Billed company name |
| `total_due` | Total amount |
| `source_file` | Source filename |

---

## Extension Challenge

1. Add support for extracting **line items** from the invoice table using `pdfplumber.extract_tables()`
2. Add a confidence score based on how many fields were successfully extracted
3. Try scanning a real invoice image and test the OCR extraction
