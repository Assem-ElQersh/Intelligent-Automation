"""
Lab 06 — ML Predictive Pipeline
Builds sklearn pipelines for three models:
  - Logistic Regression
  - Random Forest
  - Gradient Boosting

Each pipeline handles imputation, encoding, scaling, and classification.
"""

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

NUMERIC_FEATURES = [
    "age", "tenure_years", "satisfaction_score",
    "monthly_salary", "projects_completed",
    "avg_weekly_hours", "last_promotion_years",
]
CATEGORICAL_FEATURES = ["department"]
BINARY_FEATURES = ["remote_work"]

ALL_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES + BINARY_FEATURES


def _build_preprocessor() -> ColumnTransformer:
    numeric_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    categorical_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])
    return ColumnTransformer([
        ("num", numeric_pipe, NUMERIC_FEATURES),
        ("cat", categorical_pipe, CATEGORICAL_FEATURES),
        ("bin", "passthrough", BINARY_FEATURES),
    ])


def build_logistic_regression() -> Pipeline:
    return Pipeline([
        ("preprocessor", _build_preprocessor()),
        ("clf", LogisticRegression(max_iter=1000, C=1.0, random_state=42)),
    ])


def build_random_forest() -> Pipeline:
    return Pipeline([
        ("preprocessor", _build_preprocessor()),
        ("clf", RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)),
    ])


def build_gradient_boosting() -> Pipeline:
    return Pipeline([
        ("preprocessor", _build_preprocessor()),
        ("clf", GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, random_state=42)),
    ])


MODELS = {
    "Logistic Regression": build_logistic_regression,
    "Random Forest": build_random_forest,
    "Gradient Boosting": build_gradient_boosting,
}
