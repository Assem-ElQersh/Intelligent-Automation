"""
Lab 06 — ML Predictive Pipeline
Model evaluation: cross-validation, ROC-AUC, and visualization.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import cross_val_score, StratifiedKFold

PLOTS_DIR = Path(__file__).resolve().parent.parent / "output" / "plots"


def cross_validate(pipeline, X, y, cv: int = 5) -> dict:
    cv_strategy = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)
    acc = cross_val_score(pipeline, X, y, cv=cv_strategy, scoring="accuracy")
    f1 = cross_val_score(pipeline, X, y, cv=cv_strategy, scoring="f1")
    roc = cross_val_score(pipeline, X, y, cv=cv_strategy, scoring="roc_auc")
    return {
        "accuracy": acc,
        "f1": f1,
        "roc_auc": roc,
    }


def evaluate(pipeline, X_test, y_test, model_name: str) -> dict:
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    report = classification_report(y_test, y_pred, output_dict=True)
    auc = roc_auc_score(y_test, y_proba)

    print(f"\n=== {model_name} ===")
    print(classification_report(y_test, y_pred))
    print(f"ROC-AUC: {auc:.4f}")

    return {"model": model_name, "roc_auc": auc, "report": report, "y_proba": y_proba}


def plot_model_comparison(results: list[dict]) -> None:
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    names = [r["model"] for r in results]
    aucs = [r["roc_auc"] for r in results]
    accs = [r["report"]["accuracy"] for r in results]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].barh(names, aucs, color=["#3b82f6", "#10b981", "#f59e0b"])
    axes[0].set_xlabel("ROC-AUC")
    axes[0].set_title("Model Comparison — ROC-AUC", fontweight="bold")
    axes[0].set_xlim(0.5, 1.0)
    for i, v in enumerate(aucs):
        axes[0].text(v + 0.005, i, f"{v:.3f}", va="center")

    axes[1].barh(names, accs, color=["#3b82f6", "#10b981", "#f59e0b"])
    axes[1].set_xlabel("Accuracy")
    axes[1].set_title("Model Comparison — Accuracy", fontweight="bold")
    axes[1].set_xlim(0.5, 1.0)
    for i, v in enumerate(accs):
        axes[1].text(v + 0.005, i, f"{v:.3f}", va="center")

    plt.tight_layout()
    path = PLOTS_DIR / "model_comparison.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved: {path}")


def plot_roc_curves(results: list[dict], y_test) -> None:
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7, 6))
    colors = ["#3b82f6", "#10b981", "#f59e0b"]

    for r, color in zip(results, colors):
        fpr, tpr, _ = roc_curve(y_test, r["y_proba"])
        ax.plot(fpr, tpr, label=f"{r['model']} (AUC={r['roc_auc']:.3f})", color=color, lw=2)

    ax.plot([0, 1], [0, 1], "k--", lw=1, label="Random")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curves — Model Comparison", fontweight="bold")
    ax.legend(loc="lower right")
    plt.tight_layout()
    path = PLOTS_DIR / "roc_curves.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved: {path}")


def plot_feature_importance(pipeline, feature_names: list[str], model_name: str) -> None:
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    clf = pipeline.named_steps["clf"]
    if not hasattr(clf, "feature_importances_"):
        return

    importances = clf.feature_importances_
    # Get the transformed feature names from the preprocessor
    preprocessor = pipeline.named_steps["preprocessor"]
    try:
        cat_names = (preprocessor
                     .named_transformers_["cat"]
                     .named_steps["encoder"]
                     .get_feature_names_out(["department"])
                     .tolist())
        full_names = (
            [f for f in feature_names if f not in ["department", "remote_work"]]
            + cat_names
            + ["remote_work"]
        )
    except Exception:
        full_names = [f"feature_{i}" for i in range(len(importances))]

    if len(importances) != len(full_names):
        full_names = [f"feature_{i}" for i in range(len(importances))]

    indices = np.argsort(importances)[-15:]
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh([full_names[i] for i in indices], importances[indices], color="#3b82f6")
    ax.set_xlabel("Importance")
    ax.set_title(f"Feature Importances — {model_name}", fontweight="bold")
    plt.tight_layout()
    path = PLOTS_DIR / f"feature_importance_{model_name.replace(' ', '_').lower()}.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved: {path}")
