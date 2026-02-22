"""
Lab 02 — Web Scraping & Data Extraction
Export cleaned DataFrame to CSV and Excel.
"""

from pathlib import Path
import pandas as pd


def export(df: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "books.csv"
    excel_path = output_dir / "books.xlsx"

    df.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"CSV saved  → {csv_path}")

    df.to_excel(excel_path, index=False, sheet_name="Books")
    print(f"Excel saved → {excel_path}")
