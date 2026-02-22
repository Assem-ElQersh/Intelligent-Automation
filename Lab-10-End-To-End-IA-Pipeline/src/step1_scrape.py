"""
Lab 10 — End-to-End IA Pipeline
Step 1 (RPA): Scrape product data from books.toscrape.com.
Returns a DataFrame of books for downstream processing.
"""

import time
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "http://books.toscrape.com/catalogue/"
START_URL = "http://books.toscrape.com/catalogue/page-1.html"
RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def _parse_page(soup: BeautifulSoup) -> list[dict]:
    books = []
    for article in soup.select("article.product_pod"):
        title = article.h3.a["title"]
        raw_price = article.select_one("p.price_color").text
        price = float(re.sub(r"[^\d.]", "", raw_price) or 0)
        rating = RATING_MAP.get(article.p["class"][1], 0)
        availability = article.select_one("p.availability").text.strip()
        books.append({
            "title": title,
            "price_gbp": price,
            "rating": rating,
            "availability": availability,
        })
    return books


def _next_url(soup: BeautifulSoup) -> str | None:
    btn = soup.select_one("li.next a")
    return BASE_URL + btn["href"] if btn else None


def run(max_pages: int = 3, delay: float = 0.3, verbose: bool = True) -> pd.DataFrame:
    """Scrape up to `max_pages` pages and return a DataFrame."""
    all_books, url, page = [], START_URL, 1
    while url and page <= max_pages:
        if verbose:
            print(f"  [Step 1] Scraping page {page}...")
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")
        all_books.extend(_parse_page(soup))
        url = _next_url(soup)
        page += 1
        time.sleep(delay)

    df = pd.DataFrame(all_books)
    if verbose:
        print(f"  [Step 1] Scraped {len(df)} books.")
    return df
