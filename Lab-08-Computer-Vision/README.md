# Lab 08 — Computer Vision & Image Processing

**Pillar:** AI / Computer Vision  
**Difficulty:** Intermediate  
**Estimated Time:** 60–90 minutes

---

## Objective

Build a computer vision pipeline that:
- Generates a synthetic "product surface" image dataset (ok vs defect)
- Preprocesses images: resize, denoise (Gaussian blur), normalize
- Extracts features: raw pixels + statistical features + edge density (Canny)
- Trains an SVM classifier and evaluates performance
- Visualizes predictions on a test image grid with annotated results

This demonstrates **AI-driven visual quality inspection** — a key IA use case in manufacturing.

---

## Concepts Covered

| Concept | Description |
|---------|-------------|
| Image preprocessing | Resize, Gaussian blur, normalization |
| Feature extraction | Pixel flattening, statistics, Canny edge detection |
| SVM classification | RBF-kernel SVM for image classification |
| Cross-validation | 5-fold CV for robust accuracy estimates |
| Visualization | Sample grids, confusion matrix, annotated predictions |

---

## Project Structure

```
Lab-08-Computer-Vision/
├── README.md
├── requirements.txt
├── src/
│   ├── generate_dataset.py  # Synthetic ok/defect image generator
│   ├── preprocessor.py      # Load → resize → denoise → feature extract
│   ├── trainer.py           # SVM training, evaluation, model save
│   ├── visualizer.py        # Sample images, confusion matrix, prediction grid
│   └── main.py              # Entry point
├── data/
│   └── raw/
│       ├── ok/              # 120 clean surface images
│       └── defect/          # 120 defect surface images
└── output/
    ├── models/
    │   └── defect_classifier.pkl
    └── plots/
        ├── sample_images.png
        ├── confusion_matrix.png
        └── prediction_grid.png
```

---

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Usage

### Step 1: Generate the image dataset

```bash
cd src
python generate_dataset.py
```

Generates 240 synthetic grayscale images (120 `ok`, 120 `defect`).

### Step 2: Train and evaluate

```bash
python main.py
```

### Step 3: Classify a single image

```bash
python main.py --classify ../data/raw/defect/defect_0005.png
# → Prediction: DEFECT | Confidence: 92.3%
```

---

## How It Works

```
data/raw/ok/*.png  +  data/raw/defect/*.png
        │
        ▼ [preprocessor.py]
  load (grayscale)
  → resize to 64×64
  → Gaussian blur (3×3)
  → normalize to [0,1]
  → feature vector: [4096 pixels | 6 stats | 1 edge density] = 4103 features
        │
        ▼ [trainer.py]
  StandardScaler + SVM (RBF kernel, C=1.0)
  80/20 split + 5-fold cross-validation
        │
        ▼ [visualizer.py]
  sample_images.png
  confusion_matrix.png
  prediction_grid.png
```

---

## Feature Engineering

| Feature Group | Count | Description |
|---------------|-------|-------------|
| Raw pixels | 4096 | Flattened 64×64 grayscale values |
| Statistics | 6 | mean, std, min, max, Q25, Q75 |
| Edge density | 1 | Fraction of edge pixels (Canny) |
| **Total** | **4103** | Per image |

---

## Extension Challenge

1. Replace the SVM with a **CNN** using TensorFlow/Keras for higher accuracy
2. Add a new defect class (e.g., `corrosion`) and retrain as multi-class
3. Build a real-time camera feed classifier using `cv2.VideoCapture`
