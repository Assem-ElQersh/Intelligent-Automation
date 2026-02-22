"""
Lab 10 — End-to-End IA Pipeline
Step 4 (BPM): Submit high-value books to the workflow API (Lab 07) as
purchase_order tasks. Falls back to a local simulation if the API is offline.
Returns a list of workflow results.
"""

import json
import uuid
from datetime import datetime
from pathlib import Path

import pandas as pd

LOG_PATH = Path(__file__).resolve().parent.parent / "logs" / "workflow_results.jsonl"

try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False

API_URL = "http://localhost:8007/tasks"


def _simulate_workflow(book: dict) -> dict:
    """Local simulation when the Lab 07 API is not running."""
    return {
        "task_id": f"TASK-{uuid.uuid4().hex[:10].upper()}",
        "task_type": "purchase_order",
        "status": "completed",
        "requester": "ia-pipeline@automation.lab",
        "submitted_at": datetime.utcnow().isoformat(),
        "result": {
            "item": book["title"][:60],
            "quantity": 1,
            "po_number": f"PO-{uuid.uuid4().hex[:8].upper()}",
            "estimated_delivery": "3-5 business days",
        },
        "source": "simulated",
    }


def _submit_to_api(book: dict) -> dict:
    payload = {
        "task_type": "purchase_order",
        "requester": "ia-pipeline@automation.lab",
        "payload": {
            "item": book["title"][:60],
            "quantity": 1,
            "price_gbp": book["price_gbp"],
            "rating": book["rating"],
        },
        "priority": 2,
    }
    with httpx.Client(timeout=5.0) as client:
        resp = client.post(API_URL, json=payload)
        resp.raise_for_status()
        result = resp.json()
        result["source"] = "api"
        return result


def _log(results: list[dict]) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")


def run(df: pd.DataFrame, max_tasks: int = 10, verbose: bool = True) -> list[dict]:
    """Submit top high-value books to the workflow engine."""
    high_value = df[df.get("high_value_prediction", pd.Series(0, index=df.index)) == 1].head(max_tasks)

    if high_value.empty:
        if verbose:
            print("  [Step 4] No high-value books to submit.")
        return []

    if verbose:
        print(f"  [Step 4] Submitting {len(high_value)} purchase orders to workflow...")

    results = []
    use_api = HTTPX_AVAILABLE

    for _, row in high_value.iterrows():
        book = row.to_dict()
        try:
            if use_api:
                result = _submit_to_api(book)
            else:
                result = _simulate_workflow(book)
        except Exception:
            result = _simulate_workflow(book)
            result["note"] = "API unavailable, used simulation"

        results.append(result)
        if verbose:
            status = result.get("status", "?")
            task_id = result.get("task_id", "?")
            print(f"    → {task_id} | {book['title'][:40]!r} | {status}")

    _log(results)
    if verbose:
        print(f"  [Step 4] {len(results)} tasks processed. Log: {LOG_PATH}")

    return results
