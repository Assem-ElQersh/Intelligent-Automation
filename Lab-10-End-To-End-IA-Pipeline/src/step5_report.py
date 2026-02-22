"""
Lab 10 — End-to-End IA Pipeline
Step 5 (RPA): Generate an HTML summary report and export enriched data to CSV/Excel.
"""

import json
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from jinja2 import Environment, FileSystemLoader

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"

REPORT_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>IA Pipeline Report</title>
  <style>
    body { font-family: Arial, sans-serif; color: #1e293b; background: #f8faff; margin: 0; padding: 20px; }
    .container { max-width: 900px; margin: auto; background: #fff; border-radius: 12px;
                 padding: 32px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
    h1  { color: #1d4ed8; font-size: 26px; margin-bottom: 4px; }
    .meta { color: #64748b; font-size: 13px; margin-bottom: 28px; }
    h2  { color: #374151; font-size: 17px; border-left: 4px solid #2563eb; padding-left: 10px; margin: 24px 0 12px; }
    .stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 20px; }
    .stat { background: #f1f5fb; border-radius: 8px; padding: 14px 16px; }
    .stat .val { font-size: 28px; font-weight: 700; color: #2563eb; }
    .stat .lbl { font-size: 12px; color: #64748b; margin-top: 3px; }
    table { width: 100%; border-collapse: collapse; font-size: 13px; margin-top: 8px; }
    th { background: #1d4ed8; color: #fff; padding: 8px 12px; text-align: left; }
    td { padding: 7px 12px; border-bottom: 1px solid #e2e8f0; }
    tr:nth-child(even) td { background: #f7f9ff; }
    .badge { padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: bold; }
    .pos { background: #dcfce7; color: #166534; }
    .neg { background: #fee2e2; color: #991b1b; }
    .neu { background: #fef9c3; color: #713f12; }
    .hv  { background: #dbeafe; color: #1e40af; }
    img { max-width: 100%; border-radius: 8px; margin: 8px 0; }
    .footer { margin-top: 32px; font-size: 11px; color: #94a3b8; text-align: center; }
  </style>
</head>
<body><div class="container">
  <h1>Intelligent Automation Pipeline Report</h1>
  <p class="meta">Generated: {{ generated_at }} &nbsp;|&nbsp; Lab 10 — End-to-End IA Pipeline</p>

  <h2>Pipeline Summary</h2>
  <div class="stats">
    <div class="stat"><div class="val">{{ stats.total_books }}</div><div class="lbl">Books Scraped</div></div>
    <div class="stat"><div class="val">{{ stats.positive }}</div><div class="lbl">Positive Sentiment</div></div>
    <div class="stat"><div class="val">{{ stats.high_value }}</div><div class="lbl">High-Value Predicted</div></div>
    <div class="stat"><div class="val">{{ stats.workflow_tasks }}</div><div class="lbl">Workflow Tasks</div></div>
  </div>

  <h2>Pipeline Steps Executed</h2>
  <table>
    <thead><tr><th>#</th><th>Step</th><th>Pillar</th><th>Description</th><th>Status</th></tr></thead>
    <tbody>
      {% for step in steps %}
      <tr>
        <td>{{ loop.index }}</td>
        <td>{{ step.name }}</td>
        <td>{{ step.pillar }}</td>
        <td>{{ step.description }}</td>
        <td>✓ Completed</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>

  <h2>Top High-Value Books</h2>
  <table>
    <thead><tr><th>Title</th><th>Price (£)</th><th>Rating</th><th>Sentiment</th><th>HV Probability</th></tr></thead>
    <tbody>
      {% for row in top_books %}
      <tr>
        <td>{{ row.title[:50] }}</td>
        <td>£{{ "%.2f"|format(row.price_gbp) }}</td>
        <td>{{ row.rating }} / 5</td>
        <td>
          <span class="badge {{ 'pos' if row.sentiment == 'positive' else ('neg' if row.sentiment == 'negative' else 'neu') }}">
            {{ row.sentiment }}
          </span>
        </td>
        <td>{{ "%.1f"|format(row.high_value_probability * 100) }}%</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>

  <div class="footer">
    This report was generated automatically by the Intelligent Automation Lab 10 pipeline.
  </div>
</div></body></html>
"""


def _plot_summary(df: pd.DataFrame) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    fig.suptitle("IA Pipeline — Analysis Summary", fontsize=14, fontweight="bold")

    # Sentiment distribution
    sent_counts = df["sentiment"].value_counts()
    colors = {"positive": "#22c55e", "neutral": "#f59e0b", "negative": "#ef4444"}
    axes[0].bar(sent_counts.index, sent_counts.values,
                color=[colors.get(s, "#888") for s in sent_counts.index])
    axes[0].set_title("Sentiment Distribution")
    axes[0].set_ylabel("Count")

    # Price distribution
    axes[1].hist(df["price_gbp"], bins=20, color="#3b82f6", edgecolor="white")
    axes[1].set_title("Price Distribution (£)")
    axes[1].set_xlabel("Price (£)")
    axes[1].set_ylabel("Count")

    # Rating distribution
    rating_counts = df["rating"].value_counts().sort_index()
    axes[2].bar(rating_counts.index.astype(str), rating_counts.values, color="#8b5cf6")
    axes[2].set_title("Rating Distribution")
    axes[2].set_xlabel("Stars")
    axes[2].set_ylabel("Count")

    plt.tight_layout()
    path = OUTPUT_DIR / "pipeline_summary.png"
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def run(df: pd.DataFrame, workflow_results: list[dict], verbose: bool = True) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if verbose:
        print(f"  [Step 5] Generating report and exports...")

    # Plot
    _plot_summary(df)

    # Stats
    high_value_mask = df.get("high_value_prediction", pd.Series(0, index=df.index)) == 1
    stats = {
        "total_books": len(df),
        "positive": int((df.get("sentiment", "") == "positive").sum()),
        "negative": int((df.get("sentiment", "") == "negative").sum()),
        "neutral": int((df.get("sentiment", "") == "neutral").sum()),
        "high_value": int(high_value_mask.sum()),
        "workflow_tasks": len(workflow_results),
    }

    steps = [
        {"name": "Step 1: Web Scraping", "pillar": "RPA", "description": "Scraped books.toscrape.com"},
        {"name": "Step 2: Sentiment Analysis", "pillar": "AI/NLP", "description": "Analyzed title sentiment"},
        {"name": "Step 3: Predictive Model", "pillar": "AI/ML", "description": "Predicted high-value books"},
        {"name": "Step 4: Workflow Automation", "pillar": "BPM", "description": "Submitted purchase orders"},
        {"name": "Step 5: Report Generation", "pillar": "RPA", "description": "Generated HTML report + exports"},
    ]

    top_books = (
        df[high_value_mask]
        .sort_values("high_value_probability", ascending=False)
        .head(15)
        .to_dict("records")
    )

    # Render HTML report
    from jinja2 import Template
    html = Template(REPORT_TEMPLATE).render(
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        stats=stats,
        steps=steps,
        top_books=top_books,
    )
    html_path = OUTPUT_DIR / "pipeline_report.html"
    html_path.write_text(html, encoding="utf-8")

    # CSV + Excel export
    csv_path = OUTPUT_DIR / "enriched_books.csv"
    xlsx_path = OUTPUT_DIR / "enriched_books.xlsx"
    df.to_csv(csv_path, index=False)
    df.to_excel(xlsx_path, index=False, sheet_name="IA Pipeline Output")

    if verbose:
        print(f"  [Step 5] HTML report  → {html_path}")
        print(f"  [Step 5] CSV export   → {csv_path}")
        print(f"  [Step 5] Excel export → {xlsx_path}")
        print(f"  [Step 5] Chart        → {OUTPUT_DIR / 'pipeline_summary.png'}")
