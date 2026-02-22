# Lab 02 — Web Scraping & Data Extraction

**Pillar:** RPA (Robotic Process Automation)  
**Difficulty:** Beginner  
**Estimated Time:** 30–45 minutes

---

## Objective

Build a web scraper that:
- Crawls all 50 pages of [books.toscrape.com](http://books.toscrape.com)
- Extracts book title, price, star rating, and availability
- Cleans and enriches the data (price tiers, sorting)
- Exports results to both CSV and Excel

This demonstrates **automated data extraction** — one of the most common RPA use cases.

---

## Concepts Covered

| Concept | Description |
|---------|-------------|
| HTTP requests | Fetching web pages with `requests` |
| HTML parsing | Extracting structured data using `BeautifulSoup` |
| Pagination | Following "next page" links automatically |
| Data cleaning | Normalizing, deduplicating, and enriching raw data |
| Export | Writing structured output to CSV and Excel |

---

## Project Structure

```
Lab-02-Web-Scraping/
├── README.md
├── requirements.txt
├── src/
│   ├── scraper.py     # Page fetching, HTML parsing, pagination
│   ├── cleaner.py     # DataFrame cleaning and enrichment
│   ├── exporter.py    # CSV and Excel export
│   └── main.py        # Entry point with CLI arguments
└── data/
    └── output/
        ├── books.csv
        └── books.xlsx
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

```bash
cd src

# Scrape all 50 pages (~1000 books)
python main.py

# Quick demo — scrape just 3 pages (~60 books)
python main.py --pages 3

# Control request delay (be polite to the server)
python main.py --pages 5 --delay 1.0
```

Output files are saved to `data/output/books.csv` and `data/output/books.xlsx`.

---

## How It Works

```
books.toscrape.com/page-1.html
        │
        ▼ [scraper.py]
  Parse 20 books per page
  Follow "next" link → page-2.html → ... → page-50.html
        │
        ▼ [cleaner.py]
  Drop duplicates
  Add price_tier (budget / mid / premium)
  Sort by rating ↓, price ↑
        │
        ▼ [exporter.py]
  data/output/books.csv
  data/output/books.xlsx
```

### Extracted Fields

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Full book title |
| `price_gbp` | float | Price in GBP |
| `rating` | int (1–5) | Star rating |
| `availability` | string | "In stock" / "Out of stock" |
| `url` | string | Direct link to the book page |
| `price_tier` | category | budget / mid / premium |

---

## Extension Challenge

1. Scrape the **book detail page** (follow `url` field) to extract genre and description
2. Add a `--genre` filter argument to only export books from a specific category
3. Visualize price vs. rating with a scatter plot using `matplotlib`
