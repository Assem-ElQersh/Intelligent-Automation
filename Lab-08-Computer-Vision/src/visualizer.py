"""
Lab 08 — Computer Vision
Visualizations: sample images, confusion matrix, annotated predictions.
"""

from pathlib import Path

import cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import confusion_matrix

PLOTS_DIR = Path(__file__).resolve().parent.parent / "output" / "plots"


def plot_sample_images(data_dir: Path, classes: list[str], n: int = 5) -> None:
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(len(classes), n, figsize=(n * 2, len(classes) * 2.5))
    fig.suptitle("Sample Images by Class", fontsize=14, fontweight="bold")

    for row, cls in enumerate(classes):
        cls_dir = data_dir / cls
        images = sorted(cls_dir.glob("*.png"))[:n]
        for col, img_path in enumerate(images):
            ax = axes[row][col] if len(classes) > 1 else axes[col]
            img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
            ax.imshow(img, cmap="gray", vmin=0, vmax=255)
            ax.axis("off")
            if col == 0:
                ax.set_ylabel(cls.upper(), fontsize=10, fontweight="bold")

    plt.tight_layout()
    path = PLOTS_DIR / "sample_images.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved: {path}")


def plot_confusion_matrix(y_test: np.ndarray, y_pred: np.ndarray, labels: list[str]) -> None:
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    cm = confusion_matrix(y_test, y_pred)

    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=labels, yticklabels=labels, ax=ax)
    ax.set_title("Confusion Matrix — Defect Detection", fontweight="bold")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    plt.tight_layout()
    path = PLOTS_DIR / "confusion_matrix.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved: {path}")


def plot_prediction_grid(image_paths: list[Path], predictions: list[str],
                         true_labels: list[str], n: int = 10) -> None:
    """Show a grid of test images with predicted vs actual labels."""
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    n = min(n, len(image_paths))
    cols = 5
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 2.5, rows * 3))
    axes = axes.flatten()

    for i in range(n):
        img = cv2.imread(str(image_paths[i]), cv2.IMREAD_GRAYSCALE)
        axes[i].imshow(img, cmap="gray")
        correct = predictions[i] == true_labels[i]
        color = "#22c55e" if correct else "#ef4444"
        axes[i].set_title(f"Pred: {predictions[i]}\nTrue: {true_labels[i]}",
                          fontsize=8, color=color)
        axes[i].axis("off")

    for j in range(n, len(axes)):
        axes[j].axis("off")

    fig.suptitle("Predictions on Test Images", fontsize=13, fontweight="bold")
    plt.tight_layout()
    path = PLOTS_DIR / "prediction_grid.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved: {path}")
