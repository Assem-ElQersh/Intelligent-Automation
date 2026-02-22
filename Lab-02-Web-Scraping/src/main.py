"""
Lab 02 — Web Scraping & Data Extraction
Entry point.

Usage:
    python main.py              # scrape all 50 pages
    python main.py --pages 3    # scrape first 3 pages only (fast demo)
"""

import argparse
from pathlib import Path

from scraper import scrape_all_books
from cleaner import clean, summary
from exporter import export

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "output"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scrape books.toscrape.com")
    parser.add_argument(
        "--pages",
        type=int,
        default=None,
        help="Number of pages to scrape (default: all)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="Delay in seconds between requests (default: 0.5)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print("=== Lab 02: Web Scraping & Data Extraction ===\n")
    records = scrape_all_books(max_pages=args.pages, delay=args.delay)

    df = clean(records)
    summary(df)
    export(df, OUTPUT_DIR)

    print("\nDone.")


if __name__ == "__main__":
    main()
