"""
Lab 05 — NLP Sentiment Analysis Pipeline
Entry point.

Usage:
    python main.py                      # Train and visualize
    python main.py --predict "Great product, love it!"
"""

import argparse
from pathlib import Path

from trainer import train, predict, load_data
from visualizer import (
    plot_sentiment_distribution,
    plot_wordcloud,
    plot_confusion_matrix,
)
from sklearn.model_selection import train_test_split

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "reviews.csv"


def main() -> None:
    parser = argparse.ArgumentParser(description="Lab 05 — Sentiment Analysis")
    parser.add_argument("--predict", type=str, default=None,
                        help="Predict sentiment of a custom text string")
    args = parser.parse_args()

    if args.predict:
        result = predict([args.predict])
        print(f"\nText    : {args.predict}")
        print(f"Sentiment: {result[0].upper()}")
        return

    print("=== Lab 05: NLP Sentiment Analysis Pipeline ===\n")

    # Load and display dataset info
    from trainer import load_data
    df = load_data(DATA_PATH)
    print(f"Dataset loaded: {len(df)} reviews")
    print(df["sentiment"].value_counts().to_string())

    # Train model
    print("\n--- Training ---")
    pipeline = train(DATA_PATH)

    # Generate predictions for visualizations
    X = df["clean_review"]
    y = df["sentiment"]
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    y_pred = pipeline.predict(X_test)

    # Visualizations
    print("\n--- Generating Visualizations ---")
    plot_sentiment_distribution(df)
    for sentiment in ["positive", "neutral", "negative"]:
        plot_wordcloud(df, sentiment)
    plot_confusion_matrix(y_test.tolist(), y_pred.tolist(), ["positive", "neutral", "negative"])

    print("\nDone. Check the output/ directory for charts and the trained model.")


if __name__ == "__main__":
    main()
