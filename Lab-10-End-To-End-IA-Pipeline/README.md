# Lab 10 — End-to-End Intelligent Automation Pipeline

**Pillar:** AI + BPM + RPA (Integration)  
**Difficulty:** Advanced  
**Estimated Time:** 60–90 minutes

---

## Objective

Orchestrate a complete **Intelligent Automation pipeline** that combines all three IA pillars in sequence:

1. **RPA** — Scrape product data from the web
2. **AI/NLP** — Analyze sentiment of product titles
3. **AI/ML** — Predict which products are "high-value"
4. **BPM** — Submit high-value products to a workflow API as purchase orders
5. **RPA** — Generate an HTML report, CSV/Excel export, and summary chart

This is the capstone lab — it shows how isolated automation modules connect into a **real-world IA system**.

---

## Concepts Covered

| Concept | Description |
|---------|-------------|
| Pipeline orchestration | Chaining 5 independent modules into one flow |
| Data enrichment | Each step adds new columns to the shared DataFrame |
| Graceful degradation | Workflow step falls back to simulation if API is offline |
| Inter-module communication | Shared DataFrame passed between all steps |
| Reporting | Automated HTML report, CSV/Excel, and charts |

---

## Project Structure

```
Lab-10-End-To-End-IA-Pipeline/
├── README.md
├── requirements.txt
├── src/
│   ├── step1_scrape.py      # RPA: Web scraping (from Lab 02 pattern)
│   ├── step2_sentiment.py   # AI/NLP: Sentiment analysis (from Lab 05 pattern)
│   ├── step3_predict.py     # AI/ML: High-value prediction (from Lab 06 pattern)
│   ├── step4_workflow.py    # BPM: Workflow API submission (from Lab 07 pattern)
│   ├── step5_report.py      # RPA: HTML report + CSV/Excel export
│   ├── pipeline.py          # Orchestrator: runs all steps with timing
│   └── main.py              # Entry point with CLI
├── data/
│   └── input/               # (optional) local input files
├── logs/
│   └── workflow_results.jsonl
└── output/
    ├── pipeline_report.html   # Interactive HTML report
    ├── enriched_books.csv
    ├── enriched_books.xlsx
    ├── pipeline_summary.json  # Timing and counts
    └── pipeline_summary.png   # Charts
```

---

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Usage

### Run the full pipeline

```bash
cd src
python main.py
```

### Quick demo (2 pages, 5 tasks)

```bash
python main.py --pages 2 --max-tasks 5
```

### With Lab 07 API running (optional)

Start the Lab 07 server first for live workflow submission:

```bash
# In another terminal:
cd ../Lab-07-API-Process-Automation/src
uvicorn server:app --port 8007

# Then run the pipeline:
cd ../../Lab-10-End-To-End-IA-Pipeline/src
python main.py
```

If the API is not running, Step 4 automatically falls back to local simulation.

---

## Pipeline Flow

```
 ┌─────────────────────────────────────────────────────────┐
 │  Step 1 — RPA (Web Scraping)                            │
 │  books.toscrape.com → DataFrame [title, price, rating]  │
 └────────────────────────┬────────────────────────────────┘
                          │ DataFrame
 ┌────────────────────────▼────────────────────────────────┐
 │  Step 2 — AI/NLP (Sentiment Analysis)                   │
 │  Title text → [+ sentiment, sentiment_score]            │
 └────────────────────────┬────────────────────────────────┘
                          │ Enriched DataFrame
 ┌────────────────────────▼────────────────────────────────┐
 │  Step 3 — AI/ML (Predictive Model)                      │
 │  Features → [+ high_value_prediction, high_value_prob]  │
 └────────────────────────┬────────────────────────────────┘
                          │ Top high-value books
 ┌────────────────────────▼────────────────────────────────┐
 │  Step 4 — BPM (Workflow API)                            │
 │  Submit purchase orders → workflow_results.jsonl        │
 └────────────────────────┬────────────────────────────────┘
                          │ Full DataFrame + results
 ┌────────────────────────▼────────────────────────────────┐
 │  Step 5 — RPA (Report Generation)                       │
 │  → pipeline_report.html                                 │
 │  → enriched_books.csv / .xlsx                           │
 │  → pipeline_summary.png                                 │
 └─────────────────────────────────────────────────────────┘
```

---

## Output Files

| File | Description |
|------|-------------|
| `output/pipeline_report.html` | Full HTML report with stats and top books table |
| `output/enriched_books.csv` | All scraped books with all enriched columns |
| `output/enriched_books.xlsx` | Same as CSV in Excel format |
| `output/pipeline_summary.png` | 3-panel chart: sentiment, price, rating distributions |
| `output/pipeline_summary.json` | Timing and counts per step |
| `logs/workflow_results.jsonl` | Append-only log of all workflow submissions |

---

## Connecting the Labs

| Step | Builds On |
|------|-----------|
| Step 1 | Lab 02 — Web Scraping |
| Step 2 | Lab 05 — Sentiment Analysis |
| Step 3 | Lab 06 — ML Pipeline |
| Step 4 | Lab 07 — API Process Automation |
| Step 5 | Lab 03 — Email Automation (report generation pattern) |

---

## Extension Challenge

1. Add Step 0: use **Lab 01** to watch a folder and trigger the pipeline when a new CSV drops
2. Add the **email step** (Lab 03) to send the HTML report automatically at the end
3. Add **Lab 04** to process scanned PDF invoices as the data source instead of web scraping
