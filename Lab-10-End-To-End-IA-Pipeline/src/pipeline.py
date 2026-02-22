"""
Lab 10 — End-to-End IA Pipeline
Orchestrator: runs all 5 steps in sequence with timing and error handling.
"""

import sys
import time
from datetime import datetime
from pathlib import Path

import step1_scrape
import step2_sentiment
import step3_predict
import step4_workflow
import step5_report


def _banner(step: str, n: int, total: int) -> None:
    bar = "█" * n + "░" * (total - n)
    print(f"\n{'='*60}")
    print(f"  [{bar}] Step {n}/{total}: {step}")
    print(f"{'='*60}")


def run(
    max_pages: int = 3,
    max_workflow_tasks: int = 10,
    verbose: bool = True,
) -> dict:
    """
    Execute the full IA pipeline.

    Returns a summary dict with timings and counts.
    """
    overall_start = time.time()
    summary = {
        "started_at": datetime.now().isoformat(),
        "steps": {},
    }

    print(f"\n{'#'*60}")
    print(f"  INTELLIGENT AUTOMATION — END-TO-END PIPELINE")
    print(f"  Lab 10 | Started: {summary['started_at']}")
    print(f"{'#'*60}")

    # ── Step 1: Scrape ────────────────────────────────────────
    _banner("Web Scraping (RPA)", 1, 5)
    t0 = time.time()
    df = step1_scrape.run(max_pages=max_pages, verbose=verbose)
    summary["steps"]["step1_scrape"] = {
        "duration_s": round(time.time() - t0, 2),
        "books_scraped": len(df),
    }
    if df.empty:
        print("ERROR: No data scraped. Check network connection.")
        return summary

    # ── Step 2: Sentiment Analysis ────────────────────────────
    _banner("Sentiment Analysis (AI/NLP)", 2, 5)
    t0 = time.time()
    df = step2_sentiment.run(df, verbose=verbose)
    summary["steps"]["step2_sentiment"] = {
        "duration_s": round(time.time() - t0, 2),
        "distribution": df["sentiment"].value_counts().to_dict(),
    }

    # ── Step 3: Predictive Model ──────────────────────────────
    _banner("Predictive Model (AI/ML)", 3, 5)
    t0 = time.time()
    df = step3_predict.run(df, verbose=verbose)
    n_high_value = int(df.get("high_value_prediction", 0).sum())
    summary["steps"]["step3_predict"] = {
        "duration_s": round(time.time() - t0, 2),
        "high_value_books": n_high_value,
    }

    # ── Step 4: Workflow Automation ───────────────────────────
    _banner("Workflow Automation (BPM)", 4, 5)
    t0 = time.time()
    workflow_results = step4_workflow.run(df, max_tasks=max_workflow_tasks, verbose=verbose)
    summary["steps"]["step4_workflow"] = {
        "duration_s": round(time.time() - t0, 2),
        "tasks_submitted": len(workflow_results),
    }

    # ── Step 5: Report Generation ─────────────────────────────
    _banner("Report Generation (RPA)", 5, 5)
    t0 = time.time()
    step5_report.run(df, workflow_results, verbose=verbose)
    summary["steps"]["step5_report"] = {
        "duration_s": round(time.time() - t0, 2),
    }

    # ── Final Summary ─────────────────────────────────────────
    total_time = round(time.time() - overall_start, 2)
    summary["total_duration_s"] = total_time

    print(f"\n{'#'*60}")
    print(f"  PIPELINE COMPLETE in {total_time}s")
    print(f"  Books scraped      : {summary['steps']['step1_scrape']['books_scraped']}")
    print(f"  High-value books   : {n_high_value}")
    print(f"  Workflow tasks     : {len(workflow_results)}")
    print(f"  Report             : output/pipeline_report.html")
    print(f"{'#'*60}\n")

    return summary
