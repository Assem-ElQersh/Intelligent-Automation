"""
Lab 03 — Email Automation
Scheduled HTML report sender with CSV attachment.
Generates a fake sales summary report and emails it.
"""

import csv
import io
import random
from datetime import datetime, timedelta
from pathlib import Path

import schedule
import time
from jinja2 import Environment, FileSystemLoader

import config
from sender import send_email

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
ATTACHMENT_DIR = Path(__file__).resolve().parent.parent / "data" / "attachments"


def _generate_sales_data(days: int = 7) -> tuple[list[str], list[list], dict]:
    """Generate synthetic weekly sales data."""
    columns = ["Date", "Product", "Units Sold", "Revenue (USD)"]
    rows = []
    products = ["Widget A", "Widget B", "Gadget X", "Gadget Y", "Premium Pack"]
    total_revenue = 0.0
    total_units = 0

    today = datetime.today()
    for i in range(days):
        date = (today - timedelta(days=days - i - 1)).strftime("%Y-%m-%d")
        product = random.choice(products)
        units = random.randint(10, 200)
        revenue = round(units * random.uniform(9.99, 49.99), 2)
        rows.append([date, product, units, f"${revenue:,.2f}"])
        total_revenue += revenue
        total_units += units

    stats = [
        {"label": "Total Revenue", "value": f"${total_revenue:,.2f}"},
        {"label": "Units Sold", "value": f"{total_units:,}"},
        {"label": "Avg Daily Revenue", "value": f"${total_revenue / days:,.2f}"},
        {"label": "Days Covered", "value": str(days)},
    ]
    return columns, rows, stats


def _save_csv_attachment(columns: list, rows: list) -> Path:
    ATTACHMENT_DIR.mkdir(parents=True, exist_ok=True)
    path = ATTACHMENT_DIR / f"sales_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(rows)
    return path


def send_report(recipient: str) -> None:
    columns, rows, stats = _generate_sales_data(days=7)
    csv_path = _save_csv_attachment(columns, rows)

    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("report.html")
    html_body = template.render(
        report_title="Weekly Sales Summary",
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        period="Last 7 Days",
        stats=stats,
        columns=columns,
        rows=rows,
    )

    send_email(
        to=recipient,
        subject=f"[Automated] Weekly Sales Report — {datetime.now().strftime('%Y-%m-%d')}",
        body_text="Please view this email in an HTML-capable client.",
        body_html=html_body,
        attachments=[csv_path],
    )

    print(f"[REPORT SENT] → {recipient}")


def schedule_weekly_report(recipient: str, day: str = "monday", time_str: str = "08:00") -> None:
    """
    Schedule a weekly report email.

    Args:
        recipient: Email address to send the report to.
        day: Day of the week (e.g., "monday").
        time_str: Time in HH:MM format (24h).
    """
    getattr(schedule.every(), day).at(time_str).do(send_report, recipient=recipient)
    print(f"Report scheduled every {day.capitalize()} at {time_str} → {recipient}")
    print("Running scheduler... (Ctrl+C to stop)\n")

    while True:
        schedule.run_pending()
        time.sleep(30)
