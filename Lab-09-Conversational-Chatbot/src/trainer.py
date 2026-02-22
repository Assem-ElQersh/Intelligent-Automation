"""
Lab 09 — Conversational Chatbot
Intent classifier: TF-IDF + SVM trained on intents.json patterns.
"""

import json
import random
from pathlib import Path

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder

import nltk
for resource in ["stopwords", "wordnet", "punkt", "punkt_tab"]:
    try:
        nltk.data.find(f"tokenizers/{resource}")
    except LookupError:
        nltk.download(resource, quiet=True)

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

INTENTS_PATH = Path(__file__).resolve().parent.parent / "data" / "intents.json"
MODEL_PATH = Path(__file__).resolve().parent.parent / "output" / "chatbot_model.pkl"

STOP_WORDS = set(stopwords.words("english"))
LEMMATIZER = WordNetLemmatizer()


def _preprocess(text: str) -> str:
    import re
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    tokens = [LEMMATIZER.lemmatize(t) for t in text.split() if t not in STOP_WORDS and len(t) > 1]
    return " ".join(tokens)


def load_intents(path: Path = INTENTS_PATH) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def prepare_training_data(intents: dict) -> tuple[list[str], list[str]]:
    """Expand intents into (text, tag) pairs, skipping fallback."""
    X, y = [], []
    for intent in intents["intents"]:
        if intent["tag"] == "fallback":
            continue
        for pattern in intent["patterns"]:
            X.append(_preprocess(pattern))
            y.append(intent["tag"])
    return X, y


def train() -> None:
    intents = load_intents()
    X, y = prepare_training_data(intents)

    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=3000, sublinear_tf=True)),
        ("clf", SVC(kernel="linear", C=1.0, probability=True, random_state=42)),
    ])

    pipeline.fit(X, y_enc)

    cv = cross_val_score(pipeline, X, y_enc, cv=min(5, len(set(y))), scoring="accuracy")
    print(f"Training samples: {len(X)}")
    print(f"Intents: {len(set(y))}")
    print(f"CV Accuracy: {cv.mean():.3f} ± {cv.std():.3f}")

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({
        "pipeline": pipeline,
        "label_encoder": le,
        "intents": intents,
        "preprocess_fn": _preprocess,
    }, MODEL_PATH)
    print(f"Model saved: {MODEL_PATH}")


if __name__ == "__main__":
    train()
