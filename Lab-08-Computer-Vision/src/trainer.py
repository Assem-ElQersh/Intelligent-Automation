"""
Lab 08 — Computer Vision
Trains an SVM classifier on extracted image features.
"""

from pathlib import Path

import joblib
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix

MODEL_PATH = Path(__file__).resolve().parent.parent / "output" / "models" / "defect_classifier.pkl"


def build_model() -> Pipeline:
    return Pipeline([
        ("scaler", StandardScaler()),
        ("svm", SVC(kernel="rbf", C=1.0, gamma="scale", probability=True, random_state=42)),
    ])


def train(X: np.ndarray, y: np.ndarray, label_names: list[str]) -> Pipeline:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = build_model()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("=== Classification Report ===")
    print(classification_report(y_test, y_pred, target_names=label_names))

    cv = cross_val_score(model, X, y, cv=5, scoring="accuracy")
    print(f"5-fold CV accuracy: {cv.mean():.3f} ± {cv.std():.3f}")

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "labels": label_names}, MODEL_PATH)
    print(f"\nModel saved: {MODEL_PATH}")

    return model, X_test, y_test, y_pred


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError("No trained model. Run main.py first.")
    data = joblib.load(MODEL_PATH)
    return data["model"], data["labels"]
