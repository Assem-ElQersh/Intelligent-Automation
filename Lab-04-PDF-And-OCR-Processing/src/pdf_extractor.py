"""
Lab 04 — PDF & OCR Processing
Extracts text from native (text-based) PDFs using pdfplumber.
"""

import re
from pathlib import Path
import pdfplumber


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract all text from a native PDF file."""
    text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
    return "\n".join(text)


def extract_tables_from_pdf(pdf_path: Path) -> list[list[list]]:
    """Extract tables from a PDF (returns list of tables per page)."""
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_tables = page.extract_tables()
            if page_tables:
                tables.extend(page_tables)
    return tables


def parse_invoice_fields(text: str) -> dict:
    """
    Use regex patterns to extract key invoice fields from raw text.
    Handles common invoice formats.
    """
    def find(patterns: list[str], default: str = "N/A") -> str:
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()
        return default

    invoice_number = find([
        r"invoice\s*#?\s*:?\s*([A-Z0-9\-]+)",
        r"inv[#\-\s]+([A-Z0-9\-]+)",
    ])
    date = find([
        r"date\s*:?\s*(\d{4}[-/]\d{2}[-/]\d{2})",
        r"date\s*:?\s*(\d{2}[-/]\d{2}[-/]\d{4})",
        r"invoice date\s*:?\s*(\S+)",
    ])
    due_date = find([
        r"due\s*date\s*:?\s*(\d{4}[-/]\d{2}[-/]\d{2})",
        r"due\s*date\s*:?\s*(\d{2}[-/]\d{2}[-/]\d{4})",
        r"due\s*date\s*:?\s*(\S+)",
    ])
    vendor = find([
        r"^([A-Z][A-Za-z\s&\.]+(?:Ltd|Inc|Corp|LLC|Systems|Co)\.?)\b",
        r"from\s*:?\s*(.+)",
        r"bill\s*from\s*:?\s*(.+)",
    ])
    client = find([
        r"bill\s*to\s*:?\n?\s*(.+)",
        r"client\s*:?\s*(.+)",
    ])
    total = find([
        r"total\s*due\s*:?\s*\$?([\d,\.]+)",
        r"total\s*:?\s*\$?([\d,\.]+)",
        r"amount\s*due\s*:?\s*\$?([\d,\.]+)",
    ])

    return {
        "invoice_number": invoice_number,
        "date": date,
        "due_date": due_date,
        "vendor": vendor,
        "client": client,
        "total_due": total,
    }
