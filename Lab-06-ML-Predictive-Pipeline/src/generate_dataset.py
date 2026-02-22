"""
Lab 06 — ML Predictive Pipeline
Generates a synthetic employee churn dataset for training.

Features:
  age, tenure_years, satisfaction_score, monthly_salary,
  projects_completed, avg_weekly_hours, last_promotion_years,
  department, remote_work

Target: churned (0 = stayed, 1 = left)

Usage:
    python generate_dataset.py
"""

import random
from pathlib import Path
import pandas as pd
import numpy as np

OUTPUT = Path(__file__).resolve().parent.parent / "data" / "employee_churn.csv"
RANDOM_SEED = 42
N_SAMPLES = 600


def main() -> None:
    rng = np.random.RandomState(RANDOM_SEED)
    random.seed(RANDOM_SEED)

    departments = ["Engineering", "Sales", "Marketing", "HR", "Finance", "Operations"]

    records = []
    for _ in range(N_SAMPLES):
        age = int(rng.normal(35, 8))
        age = max(22, min(60, age))
        tenure = round(rng.exponential(4), 1)
        tenure = max(0.1, min(25, tenure))
        satisfaction = round(rng.uniform(1.0, 10.0), 1)
        salary = int(rng.normal(5500, 1800))
        salary = max(2000, min(12000, salary))
        projects = int(rng.normal(8, 3))
        projects = max(1, min(20, projects))
        hours = int(rng.normal(42, 7))
        hours = max(25, min(70, hours))
        last_promo = int(rng.exponential(2.5))
        last_promo = max(0, min(10, last_promo))
        dept = random.choice(departments)
        remote = rng.choice([0, 1], p=[0.55, 0.45])

        # Churn probability model
        churn_score = (
            -0.05 * satisfaction
            + 0.03 * (hours - 40)
            + 0.04 * last_promo
            - 0.02 * (salary / 1000)
            + 0.01 * (age - 35)
            - 0.03 * tenure
            + (0.1 if remote == 0 else -0.1)
        )
        churn_prob = 1 / (1 + np.exp(-churn_score))
        churned = int(rng.uniform() < churn_prob)

        records.append({
            "age": age,
            "tenure_years": tenure,
            "satisfaction_score": satisfaction,
            "monthly_salary": salary,
            "projects_completed": projects,
            "avg_weekly_hours": hours,
            "last_promotion_years": last_promo,
            "department": dept,
            "remote_work": remote,
            "churned": churned,
        })

    df = pd.DataFrame(records)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT, index=False)
    print(f"Dataset saved: {OUTPUT}")
    print(f"Shape: {df.shape}")
    print(f"Churn rate: {df['churned'].mean():.1%}")


if __name__ == "__main__":
    main()
