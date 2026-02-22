# Lab 06 — ML Predictive Analytics Pipeline

**Pillar:** AI / Machine Learning  
**Difficulty:** Intermediate  
**Estimated Time:** 60–90 minutes

---

## Objective

Build an end-to-end ML pipeline that:
- Generates a synthetic employee churn dataset
- Applies feature engineering (imputation, scaling, one-hot encoding)
- Trains and compares three classifiers (Logistic Regression, Random Forest, Gradient Boosting)
- Evaluates using ROC-AUC, accuracy, and cross-validation
- Exports the best model and generates comparison plots

This demonstrates the full **ML workflow** at the heart of AI-driven automation.

---

## Concepts Covered

| Concept | Description |
|---------|-------------|
| Feature engineering | Numerical scaling, one-hot encoding, imputation |
| sklearn Pipelines | Chaining preprocessing + model in one object |
| ColumnTransformer | Applying different transforms to different features |
| Model comparison | Training multiple models and selecting the best |
| Cross-validation | StratifiedKFold for reliable performance estimates |
| Model persistence | Save/load with `joblib` |
| Visualization | ROC curves, model comparison charts, feature importances |

---

## Project Structure

```
Lab-06-ML-Predictive-Pipeline/
├── README.md
├── requirements.txt
├── src/
│   ├── generate_dataset.py   # Creates synthetic employee_churn.csv
│   ├── pipeline.py           # Builds LR / RF / GB sklearn pipelines
│   ├── evaluator.py          # Cross-validation, ROC-AUC, plots
│   └── main.py               # Entry point: train → compare → export
├── data/
│   └── employee_churn.csv    # 600-row synthetic dataset
└── output/
    ├── models/
    │   ├── logistic_regression.pkl
    │   ├── random_forest.pkl
    │   ├── gradient_boosting.pkl
    │   └── best_model.pkl
    └── plots/
        ├── model_comparison.png
        ├── roc_curves.png
        └── feature_importance_*.png
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

### Step 1: Generate the dataset

```bash
cd src
python generate_dataset.py
```

### Step 2: Train, compare, and export

```bash
python main.py
```

### Step 3: Inspect predictions

```bash
python main.py --predict
```

---

## Dataset: Employee Churn

| Feature | Type | Description |
|---------|------|-------------|
| `age` | numeric | Employee age |
| `tenure_years` | numeric | Years at the company |
| `satisfaction_score` | numeric | Job satisfaction (1–10) |
| `monthly_salary` | numeric | Monthly salary in USD |
| `projects_completed` | numeric | Completed projects |
| `avg_weekly_hours` | numeric | Average hours worked per week |
| `last_promotion_years` | numeric | Years since last promotion |
| `department` | categorical | Department name |
| `remote_work` | binary | 1 = remote, 0 = on-site |
| `churned` | **target** | 1 = left company, 0 = stayed |

---

## How It Works

```
data/employee_churn.csv
        │
        ▼ [pipeline.py — ColumnTransformer]
  Numeric → impute (median) → StandardScaler
  Categorical → impute (mode) → OneHotEncoder
  Binary → passthrough
        │
        ▼ [Three pipelines trained in parallel]
  Logistic Regression | Random Forest | Gradient Boosting
        │
        ▼ [evaluator.py]
  ROC-AUC + Accuracy + Classification Report
  → output/plots/ charts
        │
        ▼ [Best model saved]
  output/models/best_model.pkl
```

---

## Extension Challenge

1. Add **hyperparameter tuning** using `GridSearchCV` or `RandomizedSearchCV`
2. Try **SMOTE** (imbalanced-learn) to handle class imbalance
3. Deploy the best model as a REST endpoint (see Lab 07 for FastAPI patterns)
