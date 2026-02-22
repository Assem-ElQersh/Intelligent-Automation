"""
Lab 02 — Web Scraping & Data Extraction
Data cleaning and enrichment for raw scraped book data.
"""

import pandas as pd


def clean(records: list[dict]) -> pd.DataFrame:
    """
    Convert raw scrape records to a clean DataFrame.

    Steps:
    - Drop duplicates by title
    - Add a price tier column (budget / mid / premium)
    - Sort by rating desc, price asc
    """
    df = pd.DataFrame(records)
    df.drop_duplicates(subset="title", inplace=True)
    df.reset_index(drop=True, inplace=True)

    df["price_tier"] = pd.cut(
        df["price_gbp"],
        bins=[0, 10, 30, float("inf")],
        labels=["budget", "mid", "premium"],
    )

    df.sort_values(["rating", "price_gbp"], ascending=[False, True], inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df


def summary(df: pd.DataFrame) -> None:
    """Print a quick statistical summary of the scraped dataset."""
    print("\n=== Dataset Summary ===")
    print(f"Total books : {len(df)}")
    print(f"Avg price   : £{df['price_gbp'].mean():.2f}")
    print(f"Avg rating  : {df['rating'].mean():.2f} / 5")
    print(f"\nPrice tier distribution:")
    print(df["price_tier"].value_counts().to_string())
    print(f"\nTop 5 highest-rated (cheapest first):")
    print(df[["title", "price_gbp", "rating"]].head().to_string(index=False))
