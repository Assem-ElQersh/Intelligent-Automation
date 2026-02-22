"""
Lab 05 — NLP Sentiment Analysis
Visualization: sentiment distribution, word cloud, confusion matrix.
"""

from pathlib import Path
from collections import Counter

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for saving to files
import seaborn as sns
import pandas as pd
from wordcloud import WordCloud
from sklearn.metrics import confusion_matrix

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"


def plot_sentiment_distribution(df: pd.DataFrame) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    colors = {"positive": "#22c55e", "neutral": "#f59e0b", "negative": "#ef4444"}
    counts = df["sentiment"].value_counts()

    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(counts.index, counts.values,
                  color=[colors.get(s, "#888") for s in counts.index])
    ax.set_title("Sentiment Distribution", fontsize=15, fontweight="bold")
    ax.set_xlabel("Sentiment")
    ax.set_ylabel("Count")
    for bar, val in zip(bars, counts.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                str(val), ha="center", fontsize=11)
    plt.tight_layout()
    path = OUTPUT_DIR / "sentiment_distribution.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved: {path}")


def plot_wordcloud(df: pd.DataFrame, sentiment: str) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    text = " ".join(df[df["sentiment"] == sentiment]["clean_review"].tolist())
    if not text.strip():
        return

    wc = WordCloud(
        width=800, height=400,
        background_color="white",
        colormap="RdYlGn" if sentiment == "positive" else "Reds" if sentiment == "negative" else "Blues",
        max_words=100,
    ).generate(text)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    ax.set_title(f"Word Cloud — {sentiment.capitalize()} Reviews", fontsize=14, fontweight="bold")
    plt.tight_layout()
    path = OUTPUT_DIR / f"wordcloud_{sentiment}.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved: {path}")


def plot_confusion_matrix(y_true: list, y_pred: list, labels: list) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    cm = confusion_matrix(y_true, y_pred, labels=labels)

    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=labels, yticklabels=labels, ax=ax)
    ax.set_title("Confusion Matrix", fontsize=14, fontweight="bold")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    plt.tight_layout()
    path = OUTPUT_DIR / "confusion_matrix.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved: {path}")
