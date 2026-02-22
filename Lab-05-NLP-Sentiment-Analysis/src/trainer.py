"""
Lab 05 — NLP Sentiment Analysis
Model training: TF-IDF vectorizer + Logistic Regression classifier pipeline.
"""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix

from preprocessor import preprocess

MODEL_PATH = Path(__file__).resolve().parent.parent / "output" / "sentiment_model.pkl"


def load_data(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df.dropna(subset=["review", "sentiment"], inplace=True)
    df["clean_review"] = df["review"].apply(preprocess)
    return df


def build_pipeline() -> Pipeline:
    return Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=5000,
            sublinear_tf=True,
        )),
        ("clf", LogisticRegression(
            max_iter=1000,
            C=1.0,
            multi_class="multinomial",
            solver="lbfgs",
        )),
    ])


def train(csv_path: Path, test_size: float = 0.2) -> Pipeline:
    """Train the sentiment classifier and save the model."""
    df = load_data(csv_path)

    X = df["clean_review"]
    y = df["sentiment"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )

    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    # Evaluation
    y_pred = pipeline.predict(X_test)
    print("=== Classification Report ===")
    print(classification_report(y_test, y_pred))

    cv_scores = cross_val_score(pipeline, X, y, cv=5, scoring="accuracy")
    print(f"Cross-validation accuracy: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")

    # Persist
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    print(f"\nModel saved to: {MODEL_PATH}")

    return pipeline


def load_model() -> Pipeline:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"No trained model found at {MODEL_PATH}. Run trainer.py first.")
    return joblib.load(MODEL_PATH)


def predict(texts: list[str], pipeline: Pipeline | None = None) -> list[str]:
    if pipeline is None:
        pipeline = load_model()
    cleaned = [preprocess(t) for t in texts]
    return pipeline.predict(cleaned).tolist()
