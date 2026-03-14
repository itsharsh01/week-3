"""
Day 13 AM Part C: Interview Ready — Q2 (analyze_csv), Q3 (fixed buggy code).
Q1 conceptual answer is in interview_answers.md.
"""

from pathlib import Path
from typing import Any

import pandas as pd


# ---------------------------------------------------------------------------
# Q2: analyze_csv(filepath) — load CSV, First 5 Minutes checklist, return dict
# ---------------------------------------------------------------------------


def analyze_csv(filepath: str | Path) -> dict[str, Any]:
    """
    Load a CSV, print the 'First 5 Minutes' checklist, and return a summary dict.

    Returns:
        dict with: num_rows, num_cols, numeric_cols, categorical_cols,
                   null_counts, memory_mb
    """
    path = Path(filepath)
    df = pd.read_csv(path)

    # First 5 Minutes checklist (print)
    print("=== First 5 Minutes Checklist ===\n")
    print("1. Shape:", df.shape)
    print("\n2. df.info():")
    df.info()
    print("\n3. df.describe():")
    print(df.describe())

    # Build return dict
    numeric_cols = list(df.select_dtypes(include=["number"]).columns)
    categorical_cols = [c for c in df.columns if c not in numeric_cols]
    null_counts = df.isnull().sum().to_dict()
    memory_bytes = df.memory_usage(deep=True).sum()
    memory_mb = round(memory_bytes / (1024 * 1024), 4)

    return {
        "num_rows": len(df),
        "num_cols": len(df.columns),
        "numeric_cols": numeric_cols,
        "categorical_cols": categorical_cols,
        "null_counts": null_counts,
        "memory_mb": memory_mb,
    }


# ---------------------------------------------------------------------------
# Q3: Fixed buggy code (3 bugs)
# ---------------------------------------------------------------------------
# Bug 1: df["age"] > 25 and df["salary"] > 55000 — use & and parentheses for
#        element-wise boolean; "and" is wrong and causes error.
# Bug 2: df["age"][0] = 26 — chained indexing; use df.loc[0, "age"] = 26.
# Bug 3: iloc[0:2] gives 2 rows (0,1); comment expected 3 rows — use iloc[0:3].
# ---------------------------------------------------------------------------


def demo_fixed_bugs() -> None:
    """Corrected version of the assignment's buggy code."""
    import pandas as pd

    df = pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35],
        "salary": [50000, 60000, 70000],
    })

    # Bug 1 fix: use & with parentheses for compound condition
    high_earners = df[(df["age"] > 25) & (df["salary"] > 55000)]

    # Bug 2 fix: use .loc[] for assignment instead of chained indexing
    df.loc[0, "age"] = 26

    # Bug 3 fix: iloc[0:2] gives 2 rows; for 3 rows (0,1,2) use iloc[0:3]
    first_three = df.iloc[0:3]  # Expecting 3 rows (0, 1, 2)
    print(f"Got {len(first_three)} rows, expected 3")


if __name__ == "__main__":
    # Demo Q2 on one of our CSVs
    csv_path = Path(__file__).resolve().parent / "budget_products.csv"
    if csv_path.exists():
        print("--- Q2: analyze_csv() demo ---\n")
        result = analyze_csv(csv_path)
        print("\nReturned dict:", result)

    print("\n--- Q3: Fixed bugs demo ---\n")
    demo_fixed_bugs()
