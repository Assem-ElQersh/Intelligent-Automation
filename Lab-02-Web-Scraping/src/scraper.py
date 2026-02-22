"""
Lab 02 — Web Scraping & Data Extraction
Scrapes books from http://books.toscrape.com across all pages,
extracts structured fields, and returns a list of dicts.
"""

import time
import re
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://books.toscrape.com/catalogue/"
START_URL = "http://books.toscrape.com/catalogue/page-1.html"

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def _parse_price(raw: str) -> float:
    """Strip currency symbols and return float price."""
    cleaned = re.sub(r"[^\d.]", "", raw)
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def _parse_rating(word_rating: str) -> int:
    return RATING_MAP.get(word_rating, 0)


def _parse_page(soup: BeautifulSoup) -> list[dict]:
    books = []
    for article in soup.select("article.product_pod"):
        title = article.h3.a["title"]
        price = _parse_price(article.select_one("p.price_color").text)
        rating = _parse_rating(article.p["class"][1])
        availability = article.select_one("p.availability").text.strip()
        relative_url = article.h3.a["href"].replace("../", "")
        books.append({
            "title": title,
            "price_gbp": price,
            "rating": rating,
            "availability": availability,
            "url": BASE_URL + relative_url,
        })
    return books


def _next_page_url(soup: BeautifulSoup, current_url: str) -> str | None:
    next_btn = soup.select_one("li.next a")
    if not next_btn:
        return None
    href = next_btn["href"]
    return BASE_URL + href


def scrape_all_books(
    max_pages: int | None = None,
    delay: float = 0.5,
    verbose: bool = True,
) -> list[dict]:
    """
    Scrape all books from books.toscrape.com.

    Args:
        max_pages: Limit number of pages scraped (None = all 50 pages).
        delay: Seconds to wait between requests (be polite to the server).
        verbose: Print progress.

    Returns:
        List of book dicts with title, price, rating, availability, url.
    """
    all_books = []
    url = START_URL
    page = 1

    while url:
        if max_pages and page > max_pages:
            break

        if verbose:
            print(f"Scraping page {page}: {url}")

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")

        books = _parse_page(soup)
        all_books.extend(books)

        url = _next_page_url(soup, url)
        page += 1
        time.sleep(delay)

    if verbose:
        print(f"\nTotal books scraped: {len(all_books)}")

    return all_books
