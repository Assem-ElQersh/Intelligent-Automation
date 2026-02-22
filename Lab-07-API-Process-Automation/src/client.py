"""
Lab 07 — API-Driven Process Automation
Automated client: submits tasks to the workflow API on a schedule.

Usage:
    # Make sure the server is running first:
    #   uvicorn server:app --port 8007
    python client.py
    python client.py --once       # Submit one batch and exit
    python client.py --interval 5 # Submit every 5 seconds
"""

import argparse
import random
import time
import httpx

BASE_URL = "http://localhost:8007"

TASK_TEMPLATES = [
    {
        "task_type": "invoice_approval",
        "payload_fn": lambda: {
            "vendor": random.choice(["Acme Corp", "Tech Supplies Ltd", "Office Depot"]),
            "amount": round(random.uniform(50, 5000), 2),
            "currency": "USD",
            "description": "Quarterly supply order",
        },
    },
    {
        "task_type": "leave_request",
        "payload_fn": lambda: {
            "start_date": "2025-02-10",
            "end_date": "2025-02-14",
            "reason": random.choice(["Annual leave", "Medical", "Family event"]),
            "days": 5,
        },
    },
    {
        "task_type": "it_support",
        "payload_fn": lambda: {
            "issue_description": random.choice([
                "Laptop screen flickering during video calls",
                "Unable to access shared drive after password reset",
                "Urgent: VPN connection dropping every 10 minutes",
                "Printer on floor 3 not responding to network jobs",
            ]),
            "affected_system": random.choice(["laptop", "network", "printer", "vpn"]),
        },
    },
    {
        "task_type": "purchase_order",
        "payload_fn": lambda: {
            "item": random.choice(["USB Hub", "Mechanical Keyboard", "Monitor Stand", "HDMI Cable"]),
            "quantity": random.randint(1, 10),
            "budget_code": f"BC-{random.randint(100, 999)}",
        },
    },
]

REQUESTERS = ["alice@company.com", "bob@company.com", "carol@company.com", "dave@company.com"]


def submit_batch(n: int = 3) -> None:
    with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
        for _ in range(n):
            template = random.choice(TASK_TEMPLATES)
            payload = {
                "task_type": template["task_type"],
                "requester": random.choice(REQUESTERS),
                "payload": template["payload_fn"](),
                "priority": random.randint(1, 5),
            }
            try:
                resp = client.post("/tasks", json=payload)
                resp.raise_for_status()
                data = resp.json()
                status_icon = "✓" if data["status"] == "completed" else "✗"
                print(f"  {status_icon} {data['task_id']} | {data['task_type']} | {data['status']}")
            except httpx.HTTPError as e:
                print(f"  [ERROR] {e}")


def show_stats() -> None:
    try:
        with httpx.Client(base_url=BASE_URL, timeout=5.0) as client:
            stats = client.get("/stats").json()
            print(f"\n  Stats: {stats['total_tasks']} total | {stats['by_status']}")
    except Exception:
        pass


def main() -> None:
    parser = argparse.ArgumentParser(description="Lab 07 — Automated Task Client")
    parser.add_argument("--once", action="store_true", help="Submit one batch and exit")
    parser.add_argument("--interval", type=int, default=10, help="Seconds between batches")
    parser.add_argument("--batch-size", type=int, default=3, help="Tasks per batch")
    args = parser.parse_args()

    print(f"Workflow API client → {BASE_URL}")
    print(f"Batch size: {args.batch_size} | Interval: {args.interval}s\n")

    batch_num = 0
    while True:
        batch_num += 1
        print(f"[Batch {batch_num}]")
        submit_batch(args.batch_size)
        show_stats()

        if args.once:
            break
        print(f"  Next batch in {args.interval}s...")
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
