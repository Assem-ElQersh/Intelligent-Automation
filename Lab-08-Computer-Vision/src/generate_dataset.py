"""
Lab 08 — Computer Vision
Generates a synthetic image dataset for a defect detection task.
Each image is a 64x64 grayscale "product surface" with or without a defect.

Classes:
  ok      — uniform texture
  defect  — has a scratch/spot pattern

Usage:
    python generate_dataset.py
"""

import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

BASE_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
CLASSES = {"ok": 120, "defect": 120}
IMG_SIZE = 64
RANDOM_SEED = 42

rng = np.random.RandomState(RANDOM_SEED)
random.seed(RANDOM_SEED)


def _make_ok_image() -> Image.Image:
    """Uniform textured surface — no defects."""
    base = rng.randint(180, 230)
    noise = rng.randint(-15, 15, (IMG_SIZE, IMG_SIZE)).astype(np.int32)
    arr = np.clip(base + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, mode="L")


def _make_defect_image() -> Image.Image:
    """Surface with a visible scratch or dark spot."""
    img = _make_ok_image()
    draw = ImageDraw.Draw(img)
    defect_type = random.choice(["scratch", "spot", "edge_crack"])

    if defect_type == "scratch":
        x0 = random.randint(5, 30)
        y0 = random.randint(5, 55)
        x1 = x0 + random.randint(15, 35)
        y1 = y0 + random.randint(-10, 10)
        width = random.randint(1, 3)
        draw.line([(x0, y0), (x1, y1)], fill=random.randint(20, 80), width=width)
    elif defect_type == "spot":
        cx = random.randint(10, 54)
        cy = random.randint(10, 54)
        r = random.randint(3, 9)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=random.randint(10, 70))
    else:  # edge_crack
        x = random.randint(0, 20)
        draw.line([(x, 0), (x + random.randint(5, 20), random.randint(10, 30))],
                  fill=random.randint(10, 60), width=2)

    return img


def main() -> None:
    for cls, count in CLASSES.items():
        out_dir = BASE_DIR / cls
        out_dir.mkdir(parents=True, exist_ok=True)
        fn = _make_ok_image if cls == "ok" else _make_defect_image
        for i in range(count):
            img = fn()
            img.save(out_dir / f"{cls}_{i:04d}.png")
        print(f"Generated {count} images → {out_dir}")
    print("Done.")


if __name__ == "__main__":
    main()
