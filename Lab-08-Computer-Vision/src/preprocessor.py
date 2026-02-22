"""
Lab 08 — Computer Vision
Image preprocessing pipeline: load → resize → denoise → threshold → feature extraction.
"""

from pathlib import Path
import cv2
import numpy as np
from PIL import Image

IMG_SIZE = 64


def load_image(path: Path) -> np.ndarray:
    """Load image as grayscale numpy array."""
    img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Could not load image: {path}")
    return img


def resize(img: np.ndarray, size: int = IMG_SIZE) -> np.ndarray:
    return cv2.resize(img, (size, size), interpolation=cv2.INTER_AREA)


def denoise(img: np.ndarray) -> np.ndarray:
    """Apply Gaussian blur to reduce noise."""
    return cv2.GaussianBlur(img, (3, 3), 0)


def normalize(img: np.ndarray) -> np.ndarray:
    """Normalize pixel values to [0, 1]."""
    return img.astype(np.float32) / 255.0


def extract_features(img: np.ndarray) -> np.ndarray:
    """
    Extract a feature vector from a preprocessed image:
      - Flattened pixel values (raw features)
      - Statistical features (mean, std, min, max, percentiles)
      - Edge density via Canny
    """
    img_uint8 = (img * 255).astype(np.uint8) if img.max() <= 1.0 else img

    # Flatten raw pixels
    flat = img_uint8.flatten().astype(np.float32) / 255.0

    # Statistical features
    stats = np.array([
        img_uint8.mean() / 255.0,
        img_uint8.std() / 255.0,
        img_uint8.min() / 255.0,
        img_uint8.max() / 255.0,
        np.percentile(img_uint8, 25) / 255.0,
        np.percentile(img_uint8, 75) / 255.0,
    ], dtype=np.float32)

    # Edge density
    edges = cv2.Canny(img_uint8, 50, 150)
    edge_density = edges.sum() / (edges.size * 255.0)
    edge_feature = np.array([edge_density], dtype=np.float32)

    return np.concatenate([flat, stats, edge_feature])


def preprocess_pipeline(path: Path) -> np.ndarray:
    """Full preprocessing: load → resize → denoise → normalize → features."""
    img = load_image(path)
    img = resize(img)
    img = denoise(img)
    img = normalize(img)
    return extract_features(img)


def load_dataset(data_dir: Path, classes: list[str]) -> tuple[np.ndarray, np.ndarray, list[str]]:
    """
    Load all images from class subdirectories.

    Returns:
        X: Feature matrix (n_samples, n_features)
        y: Label array (n_samples,)
        label_names: Class names in label order
    """
    X, y = [], []
    label_map = {cls: idx for idx, cls in enumerate(classes)}

    for cls in classes:
        cls_dir = data_dir / cls
        if not cls_dir.exists():
            raise FileNotFoundError(f"Class directory not found: {cls_dir}")
        for img_path in sorted(cls_dir.glob("*.png")):
            features = preprocess_pipeline(img_path)
            X.append(features)
            y.append(label_map[cls])

    return np.array(X), np.array(y), classes
