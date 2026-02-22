"""
Lab 04 — PDF & OCR Processing
Generates sample native PDF invoices for testing the extractor.
Requires: reportlab

Usage:
    python generate_sample_invoice.py
"""

from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "input"

INVOICES = [
    {
        "filename": "invoice_001.pdf",
        "invoice_number": "INV-2024-001",
        "date": "2024-11-15",
        "due_date": "2024-12-15",
        "vendor": "Acme Corp Ltd.",
        "vendor_address": "42 Innovation Drive, Tech City, TC1 2AB",
        "client": "Global Solutions Inc.",
        "items": [
            ("Software License — Annual", 1, 1200.00),
            ("Support & Maintenance", 12, 75.00),
            ("Onboarding Services", 3, 250.00),
        ],
        "tax_rate": 0.20,
    },
    {
        "filename": "invoice_002.pdf",
        "invoice_number": "INV-2024-002",
        "date": "2024-12-01",
        "due_date": "2024-12-31",
        "vendor": "DataFlow Systems",
        "vendor_address": "88 Pipeline Road, Data Park, DP3 4CD",
        "client": "Retail Chain Co.",
        "items": [
            ("Data Processing — 1TB", 5, 399.00),
            ("API Access — Premium Tier", 1, 599.00),
        ],
        "tax_rate": 0.20,
    },
]


def _draw_invoice(c: canvas.Canvas, inv: dict) -> None:
    w, h = A4

    # Header
    c.setFont("Helvetica-Bold", 22)
    c.drawString(2 * cm, h - 2.5 * cm, "INVOICE")

    c.setFont("Helvetica", 10)
    c.drawString(2 * cm, h - 3.2 * cm, inv["vendor"])
    c.drawString(2 * cm, h - 3.7 * cm, inv["vendor_address"])

    # Invoice metadata
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(w - 2 * cm, h - 2.5 * cm, f"Invoice #: {inv['invoice_number']}")
    c.setFont("Helvetica", 10)
    c.drawRightString(w - 2 * cm, h - 3.0 * cm, f"Date: {inv['date']}")
    c.drawRightString(w - 2 * cm, h - 3.5 * cm, f"Due Date: {inv['due_date']}")

    # Bill To
    c.setFont("Helvetica-Bold", 10)
    c.drawString(2 * cm, h - 5.0 * cm, "Bill To:")
    c.setFont("Helvetica", 10)
    c.drawString(2 * cm, h - 5.5 * cm, inv["client"])

    # Table header
    y = h - 7 * cm
    c.setFont("Helvetica-Bold", 10)
    c.drawString(2 * cm, y, "Description")
    c.drawString(11 * cm, y, "Qty")
    c.drawString(13 * cm, y, "Unit Price")
    c.drawString(16 * cm, y, "Amount")
    c.line(2 * cm, y - 0.3 * cm, w - 2 * cm, y - 0.3 * cm)

    # Table rows
    y -= 0.8 * cm
    subtotal = 0.0
    c.setFont("Helvetica", 10)
    for desc, qty, unit_price in inv["items"]:
        amount = qty * unit_price
        subtotal += amount
        c.drawString(2 * cm, y, desc)
        c.drawString(11 * cm, y, str(qty))
        c.drawRightString(15 * cm, y, f"${unit_price:,.2f}")
        c.drawRightString(18.5 * cm, y, f"${amount:,.2f}")
        y -= 0.6 * cm

    # Totals
    tax = subtotal * inv["tax_rate"]
    total = subtotal + tax
    c.line(2 * cm, y - 0.2 * cm, w - 2 * cm, y - 0.2 * cm)
    y -= 0.8 * cm
    c.drawRightString(15 * cm, y, "Subtotal:")
    c.drawRightString(18.5 * cm, y, f"${subtotal:,.2f}")
    y -= 0.6 * cm
    c.drawRightString(15 * cm, y, f"Tax ({int(inv['tax_rate'] * 100)}%):")
    c.drawRightString(18.5 * cm, y, f"${tax:,.2f}")
    y -= 0.6 * cm
    c.setFont("Helvetica-Bold", 11)
    c.drawRightString(15 * cm, y, "TOTAL DUE:")
    c.drawRightString(18.5 * cm, y, f"${total:,.2f}")

    # Footer
    c.setFont("Helvetica", 8)
    c.drawCentredString(w / 2, 1.5 * cm, "Thank you for your business. Payment terms: 30 days net.")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for inv in INVOICES:
        path = OUTPUT_DIR / inv["filename"]
        c = canvas.Canvas(str(path), pagesize=A4)
        _draw_invoice(c, inv)
        c.save()
        print(f"Generated: {path}")
    print(f"\n{len(INVOICES)} sample invoices created in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
