"""
Lab 06 — ML Predictive Pipeline
End-to-end pipeline: load → feature engineer → train models → compare → export best.

Usage:
    python generate_dataset.py     # Create synthetic dataset first
    python main.py                 # Train, compare, and export the best model
    python main.py --predict       # Run inference with the saved model
"""

import argparse
from pathlib import Path

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split

from pipeline import MODELS, ALL_FEATURES
from evaluator import evaluate, plot_model_comparison, plot_roc_curves, plot_feature_importance

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "employee_churn.csv"
MODELS_DIR = Path(__file__).resolve().parent.parent / "output" / "models"
TARGET = "churned"


def load_and_split(path: Path):
    df = pd.read_csv(path)
    X = df[ALL_FEATURES]
    y = df[TARGET]
    return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


def train_all(X_train, X_test, y_train, y_test) -> list[dict]:
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    trained_pipelines = {}

    for name, builder in MODELS.items():
        print(f"\nTraining: {name}...")
        pipeline = builder()
        pipeline.fit(X_train, y_train)
        result = evaluate(pipeline, X_test, y_test, name)
        results.append(result)
        trained_pipelines[name] = pipeline

        model_path = MODELS_DIR / f"{name.replace(' ', '_').lower()}.pkl"
        joblib.dump(pipeline, model_path)
        print(f"Model saved: {model_path}")

    return results, trained_pipelines


def main() -> None:
    parser = argparse.ArgumentParser(description="Lab 06 — ML Predictive Pipeline")
    parser.add_argument("--predict", action="store_true",
                        help="Run inference with the best saved model")
    args = parser.parse_args()

    if not DATA_PATH.exists():
        print("Dataset not found. Run 'python generate_dataset.py' first.")
        return

    print("=== Lab 06: ML Predictive Analytics Pipeline ===\n")

    X_train, X_test, y_train, y_test = load_and_split(DATA_PATH)
    print(f"Train: {len(X_train)} | Test: {len(X_test)}")
    print(f"Churn rate (train): {y_train.mean():.1%}")

    results, trained_pipelines = train_all(X_train, X_test, y_train, y_test)

    # Compare and select best
    best = max(results, key=lambda r: r["roc_auc"])
    print(f"\n=== Best Model: {best['model']} (ROC-AUC: {best['roc_auc']:.4f}) ===")

    best_path = MODELS_DIR / "best_model.pkl"
    joblib.dump(trained_pipelines[best["model"]], best_path)
    print(f"Best model saved: {best_path}")

    # Visualizations
    print("\n--- Generating Plots ---")
    plot_model_comparison(results)
    plot_roc_curves(results, y_test)
    best_pipeline = trained_pipelines[best["model"]]
    plot_feature_importance(best_pipeline, ALL_FEATURES, best["model"])

    if args.predict:
        print("\n--- Sample Predictions ---")
        model = joblib.load(best_path)
        sample = X_test.head(5).copy()
        sample["actual"] = y_test.head(5).values
        sample["predicted"] = model.predict(X_test.head(5))
        sample["churn_probability"] = model.predict_proba(X_test.head(5))[:, 1].round(3)
        print(sample[["age", "satisfaction_score", "actual", "predicted", "churn_probability"]].to_string())

    print("\nDone. Check output/ for models and plots.")


if __name__ == "__main__":
    main()
