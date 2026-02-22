"""
Lab 10 — End-to-End IA Pipeline
Entry point with CLI arguments.

Usage:
    python main.py                          # Full run (3 pages)
    python main.py --pages 5               # Scrape 5 pages
    python main.py --pages 2 --max-tasks 5 # Quick demo
"""

import argparse
import json
from pathlib import Path

from pipeline import run

SUMMARY_PATH = Path(__file__).resolve().parent.parent / "output" / "pipeline_summary.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lab 10 — End-to-End Intelligent Automation Pipeline")
    parser.add_argument("--pages", type=int, default=3,
                        help="Number of pages to scrape from books.toscrape.com (default: 3)")
    parser.add_argument("--max-tasks", type=int, default=10,
                        help="Max workflow tasks to submit (default: 10)")
    parser.add_argument("--quiet", action="store_true", help="Suppress step-level output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run(
        max_pages=args.pages,
        max_workflow_tasks=args.max_tasks,
        verbose=not args.quiet,
    )

    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"Summary JSON saved: {SUMMARY_PATH}")


if __name__ == "__main__":
    main()
