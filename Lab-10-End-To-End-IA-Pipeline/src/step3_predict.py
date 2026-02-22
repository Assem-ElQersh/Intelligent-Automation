"""
Lab 10 — End-to-End IA Pipeline
Step 3 (AI/ML): Predict whether a book is "high value" (rating ≥ 4 AND price ≤ 20)
using a Random Forest classifier trained on the scraped data itself.
Adds `high_value_prediction` and `high_value_probability` columns.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


def run(df: pd.DataFrame, verbose: bool = True) -> pd.DataFrame:
    """Train a quick classifier and predict 'high value' label for each book."""
    if verbose:
        print(f"  [Step 3] Running predictive model on {len(df)} books...")

    work = df.copy()

    # Target: high value = top-rated + affordable
    work["target"] = ((work["rating"] >= 4) & (work["price_gbp"] <= 20)).astype(int)

    # Features
    le = LabelEncoder()
    work["sentiment_enc"] = le.fit_transform(work.get("sentiment", pd.Series(["neutral"] * len(work))))

    X = work[["price_gbp", "rating", "sentiment_score", "sentiment_enc"]].fillna(0)
    y = work["target"]

    if len(y.unique()) < 2 or len(X) < 10:
        df["high_value_prediction"] = 0
        df["high_value_probability"] = 0.0
        return df

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=50, random_state=42)
    clf.fit(X_train, y_train)

    train_acc = clf.score(X_train, y_train)
    test_acc = clf.score(X_test, y_test)

    if verbose:
        print(f"  [Step 3] Train accuracy: {train_acc:.2%} | Test accuracy: {test_acc:.2%}")

    preds = clf.predict(X)
    probas = clf.predict_proba(X)[:, 1]

    df = df.copy()
    df["high_value_prediction"] = preds
    df["high_value_probability"] = probas.round(3)

    if verbose:
        n_high = preds.sum()
        print(f"  [Step 3] {n_high} books predicted as high-value.")

    return df
