"""
Lab 03 — Email Automation
Entry point with two modes:
  monitor   — scan inbox and send keyword-based auto-replies
  report    — send a report immediately (useful for testing)
  schedule  — start the weekly scheduled report

Usage:
    python main.py monitor
    python main.py report --to you@example.com
    python main.py schedule --to you@example.com --day monday --time 08:00
"""

import argparse
import sys

from inbox_monitor import check_and_reply
from report_sender import send_report, schedule_weekly_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lab 03 — Email Automation")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("monitor", help="Check inbox and auto-reply to unread emails")

    rp = sub.add_parser("report", help="Send a report email immediately")
    rp.add_argument("--to", required=True, help="Recipient email address")

    sp = sub.add_parser("schedule", help="Start scheduled weekly report")
    sp.add_argument("--to", required=True, help="Recipient email address")
    sp.add_argument("--day", default="monday", help="Day of week (default: monday)")
    sp.add_argument("--time", default="08:00", help="Time HH:MM 24h (default: 08:00)")

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.command == "monitor":
        print("=== Lab 03: Inbox Monitor ===")
        n = check_and_reply()
        print(f"Processed {n} email(s).")

    elif args.command == "report":
        print("=== Lab 03: Sending Report ===")
        send_report(args.to)

    elif args.command == "schedule":
        print("=== Lab 03: Scheduled Report ===")
        schedule_weekly_report(args.to, day=args.day, time_str=args.time)

    else:
        print("No command given. Use: monitor | report | schedule")
        sys.exit(1)


if __name__ == "__main__":
    main()
