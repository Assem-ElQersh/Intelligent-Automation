"""
Lab 08 — Computer Vision
Entry point.

Usage:
    python generate_dataset.py     # Generate synthetic images
    python main.py                 # Train and evaluate
    python main.py --classify path/to/image.png  # Classify a single image
"""

import argparse
from pathlib import Path
import numpy as np
from sklearn.model_selection import train_test_split

from preprocessor import load_dataset, preprocess_pipeline
from trainer import train, load_model
from visualizer import plot_sample_images, plot_confusion_matrix, plot_prediction_grid

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
CLASSES = ["ok", "defect"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Lab 08 — Computer Vision: Defect Detection")
    parser.add_argument("--classify", type=Path, default=None,
                        help="Path to a single image to classify")
    args = parser.parse_args()

    if args.classify:
        model, labels = load_model()
        features = preprocess_pipeline(args.classify).reshape(1, -1)
        pred = model.predict(features)[0]
        proba = model.predict_proba(features)[0]
        print(f"\nImage: {args.classify}")
        print(f"Prediction: {labels[pred].upper()}")
        print(f"Confidence: {proba[pred]:.1%}")
        return

    print("=== Lab 08: Computer Vision — Defect Detection ===\n")

    # Check dataset exists
    if not (DATA_DIR / CLASSES[0]).exists():
        print("Dataset not found. Run 'python generate_dataset.py' first.")
        return

    print("Loading and preprocessing images...")
    X, y, label_names = load_dataset(DATA_DIR, CLASSES)
    print(f"Dataset: {X.shape[0]} images | {X.shape[1]} features each")
    print(f"Classes: {dict(zip(label_names, [int((y == i).sum()) for i in range(len(label_names))]))} ")

    # Visualize samples
    print("\nGenerating sample image grid...")
    plot_sample_images(DATA_DIR, CLASSES)

    # Train
    print("\nTraining SVM classifier...")
    model, X_test, y_test, y_pred = train(X, y, label_names)

    # Visualize results
    print("\nGenerating visualizations...")
    plot_confusion_matrix(y_test, y_pred, label_names)

    # Build test image paths for prediction grid
    X_train_idx, X_test_idx = train_test_split(
        range(len(X)), test_size=0.2, random_state=42, stratify=y
    )
    all_paths = []
    all_labels = []
    for cls in CLASSES:
        for p in sorted((DATA_DIR / cls).glob("*.png")):
            all_paths.append(p)
            all_labels.append(cls)

    test_paths = [all_paths[i] for i in X_test_idx][:10]
    test_true = [all_labels[i] for i in X_test_idx][:10]
    test_pred = [label_names[p] for p in y_pred[:10]]

    plot_prediction_grid(test_paths, test_pred, test_true)

    print("\nDone. Check output/ for models and plots.")


if __name__ == "__main__":
    main()
