"""
Day 13 AM Part D: Automated data quality report.
Generates report dict and formatted summary (shape, dtypes, missing %, duplicates,
unique counts, basic stats). Uses df.memory_usage() where applicable.
"""

from typing import Any

import pandas as pd


def data_quality_report(df: pd.DataFrame) -> dict[str, Any]:
    """
    Generate an automated data quality report for a DataFrame.

    Includes: shape, dtypes, missing values percentage, duplicate rows,
    unique value counts per column, basic stats. Return the report as a dict
    and print a formatted summary.
    """
    if df.empty:
        report = {
            "shape": (0, 0),
            "dtypes": {},
            "missing_pct": {},
            "duplicate_rows": 0,
            "unique_counts": {},
            "memory_mb": 0.0,
            "numeric_stats": {},
            "single_value_columns": [],
        }
        print("(Empty DataFrame — no columns)")
        return report

    # Shape and dtypes
    shape = df.shape
    dtypes = df.dtypes.astype(str).to_dict()

    # Missing values percentage
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2).to_dict()

    # Duplicate rows
    duplicate_rows = int(df.duplicated().sum())

    # Unique value counts per column
    unique_counts = df.nunique().to_dict()

    # Memory (using memory_usage)
    memory_bytes = df.memory_usage(deep=True).sum()
    memory_mb = round(memory_bytes / (1024 * 1024), 4)

    # Basic stats for numeric columns
    numeric = df.select_dtypes(include=["number"])
    numeric_stats = numeric.describe().to_dict() if not numeric.empty else {}

    # Columns with single unique value (useless for many analyses)
    single_value_columns = [c for c in df.columns if df[c].nunique() <= 1]

    report = {
        "shape": shape,
        "dtypes": dtypes,
        "missing_pct": missing_pct,
        "duplicate_rows": duplicate_rows,
        "unique_counts": unique_counts,
        "memory_mb": memory_mb,
        "numeric_stats": numeric_stats,
        "single_value_columns": single_value_columns,
    }

    # Formatted print
    print("=" * 50)
    print("DATA QUALITY REPORT")
    print("=" * 50)
    print(f"Shape: {shape[0]} rows × {shape[1]} columns")
    print(f"Memory: {memory_mb} MB")
    print(f"Duplicate rows: {duplicate_rows}")
    print("\nDtypes:")
    for col, dt in dtypes.items():
        print(f"  {col}: {dt}")
    print("\nMissing %:")
    for col, pct in missing_pct.items():
        if pct > 0:
            print(f"  {col}: {pct}%")
    if not any(missing_pct.values()):
        print("  (none)")
    print("\nUnique counts:")
    for col, n in unique_counts.items():
        print(f"  {col}: {n}")
    if single_value_columns:
        print(f"\nSingle-value columns (consider dropping): {single_value_columns}")
    if numeric_stats:
        print("\nNumeric summary (sample):")
        print(numeric.describe().round(2))
    print("=" * 50)

    return report


if __name__ == "__main__":
    # Test 1: Clean DataFrame
    clean = pd.DataFrame({
        "id": [1, 2, 3],
        "name": ["A", "B", "C"],
        "value": [10.0, 20.0, 30.0],
    })
    print("--- Test 1: Clean DataFrame ---\n")
    data_quality_report(clean)

    # Test 2: Messy DataFrame (nulls, duplicates, single-value col)
    messy = pd.DataFrame({
        "x": [1, 1, 2, 2, 2],
        "y": [10, None, 20, None, 20],
        "constant": ["same"] * 5,
    })
    print("\n--- Test 2: Messy DataFrame ---\n")
    data_quality_report(messy)
