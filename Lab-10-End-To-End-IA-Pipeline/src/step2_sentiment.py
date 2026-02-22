"""
Lab 10 — End-to-End IA Pipeline
Step 2 (AI/NLP): Analyze sentiment of book titles (simulated review text).
Applies TF-IDF + Logistic Regression trained inline on a small labeled corpus.
Returns the DataFrame enriched with a `sentiment` column.
"""

import re
import pandas as pd
import numpy as np
import nltk

for resource in ["stopwords", "wordnet", "punkt", "punkt_tab"]:
    try:
        nltk.data.find(f"tokenizers/{resource}")
    except LookupError:
        nltk.download(resource, quiet=True)

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

STOP_WORDS = set(stopwords.words("english"))
LEMMATIZER = WordNetLemmatizer()

# Minimal inline training corpus for keyword-seeded sentiment
_TRAINING_DATA = [
    ("amazing wonderful excellent fantastic love perfect brilliant outstanding", "positive"),
    ("great good nice well solid recommend enjoy pleasant happy", "positive"),
    ("terrible awful horrible bad worst broken useless disappointing waste", "negative"),
    ("poor weak slow fail broken dead wrong missing ugly", "negative"),
    ("okay average decent moderate fair acceptable ordinary standard", "neutral"),
    ("normal typical common usual regular general basic simple", "neutral"),
]


def _preprocess(text: str) -> str:
    text = re.sub(r"[^a-z\s]", " ", text.lower())
    tokens = [LEMMATIZER.lemmatize(t) for t in text.split() if t not in STOP_WORDS and len(t) > 1]
    return " ".join(tokens)


def _build_model() -> Pipeline:
    X = [_preprocess(t) for t, _ in _TRAINING_DATA]
    y = [label for _, label in _TRAINING_DATA]
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
        ("clf", LogisticRegression(max_iter=500, C=1.0)),
    ])
    pipeline.fit(X, y)
    return pipeline


def run(df: pd.DataFrame, verbose: bool = True) -> pd.DataFrame:
    """Add `sentiment` and `sentiment_score` columns to the DataFrame."""
    if verbose:
        print(f"  [Step 2] Running sentiment analysis on {len(df)} titles...")

    model = _build_model()
    processed = df["title"].apply(_preprocess)
    df["sentiment"] = model.predict(processed)
    proba = model.predict_proba(processed)
    classes = model.classes_
    df["sentiment_score"] = proba.max(axis=1).round(3)

    if verbose:
        counts = df["sentiment"].value_counts().to_dict()
        print(f"  [Step 2] Sentiment distribution: {counts}")

    return df
