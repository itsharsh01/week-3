"""
Day 13 PM Part A: End-to-End Data Cleaning Pipeline.
Creates messy survey data, detect_issues(), clean_data(), before/after comparison, exports.
"""

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


SURVEY_COLUMNS = [
    "respondent_id", "age", "income", "satisfaction_score", "region",
    "feedback", "date_submitted", "contact_email",
]


def create_messy_survey() -> pd.DataFrame:
    """
    Create survey dataset: 50+ rows, 8+ columns, with at least 8 data quality issues:
    NaN, None, empty strings, duplicates, wrong dtypes, inconsistent casing,
    extra whitespace, invalid values (e.g. age -5 or 200).
    """
    n = 55
    np.random.seed(42)
    # Intentionally mix types and bad values
    age_raw = [25, 30, -5, 35, 200, 28, None, 40, 22, 45, np.nan, 31, 19, 999, 33] * 4
    age_raw = age_raw[:n]
    income_raw = ["50000", " 60000 ", "N/A", 72000, "null", "55000", "", "80000", None, "45,000"] * 6
    income_raw = income_raw[:n]
    satisfaction = [1, 2, 3, 4, 5, np.nan, 4, 3, "", 5, 2, 4, None, 3, 5] * 4
    satisfaction = satisfaction[:n]
    region_raw = ["  NORTH  ", "SOUTH", "east", "WEST", "  North  ", "", "SOUTH", "East", " west "] * 7
    region_raw = region_raw[:n]
    feedback_raw = ["Good!!", "  Great service  ", "OK", "", None, "Bad", "  EXCELLENT  "] * 8
    feedback_raw = feedback_raw[:n]
    date_raw = ["2024-01-15", "15/02/2024", "invalid", "2024-03-01", None, "2024-04-10", ""] * 8
    date_raw = date_raw[:n]
    email_raw = ["a@b.com", "  b@c.co  ", "invalid", "", None, "d@e.com"] * 10
    email_raw = email_raw[:n]

    df = pd.DataFrame({
        "respondent_id": list(range(1, n + 1)),
        "age": age_raw,
        "income": income_raw,
        "satisfaction_score": satisfaction,
        "region": region_raw,
        "feedback": feedback_raw,
        "date_submitted": date_raw,
        "contact_email": email_raw,
    })
    # Force wrong dtypes: age as object in some rows
    df["age"] = df["age"].astype(object)
    # Add duplicate rows
    df = pd.concat([df, df.iloc[:3]], ignore_index=True)
    return df


def detect_issues(df: pd.DataFrame) -> dict[str, Any]:
    """
    Return comprehensive data quality report: total_rows, total_missing,
    missing_per_column, duplicate_count, wrong_types, invalid_values.
    """
    missing_per_column = df.isnull().sum().to_dict()
    # Also count empty string as missing for object columns
    for col in df.columns:
        if col not in df.select_dtypes(include=["number"]).columns:
        empty_count = (df[col].astype(str).str.strip() == "").sum()
        missing_per_column[col] = missing_per_column.get(col, 0) + int(empty_count)
    total_missing = sum(missing_per_column.values())

    # Columns that should be numeric but are object
    numeric_expected = ["age", "income", "satisfaction_score"]
    wrong_types = []
    for col in numeric_expected:
        if col in df.columns and df[col].dtype == object:
            wrong_types.append(col)

    # Invalid values: age outside 0-120, satisfaction outside 1-5
    invalid_values = {}
    if "age" in df.columns:
        try:
            age_numeric = pd.to_numeric(df["age"], errors="coerce")
            invalid = (age_numeric < 0) | (age_numeric > 120)
            invalid_values["age"] = int(invalid.sum())
        except Exception:
            invalid_values["age"] = 0
    if "satisfaction_score" in df.columns:
        try:
            sat_numeric = pd.to_numeric(df["satisfaction_score"], errors="coerce")
            invalid = (sat_numeric < 1) | (sat_numeric > 5)
            invalid_values["satisfaction_score"] = int(invalid.sum())
        except Exception:
            invalid_values["satisfaction_score"] = 0

    return {
        "total_rows": len(df),
        "total_missing": total_missing,
        "missing_per_column": missing_per_column,
        "duplicate_count": int(df.duplicated().sum()),
        "wrong_types": wrong_types,
        "invalid_values": invalid_values,
    }


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Replace hidden NaN markers, fix types (to_numeric), standardize text (.str),
    fill missing (strategy per column in comments), drop unfixable rows, remove duplicates.
    """
    out = df.copy()

    # Replace hidden NaN markers before any numeric conversion
    hidden_nan = ["", "N/A", "n/a", "NA", "null", "NULL", "None", "nan", "-", " "]
    for col in out.columns:
        if out[col].dtype == object:
            out[col] = out[col].replace(hidden_nan, np.nan)

    # Fix types with to_numeric(errors='coerce')
    out["age"] = pd.to_numeric(out["age"], errors="coerce")
    out["income"] = out["income"].astype(str).str.replace(",", "", regex=False)
    out["income"] = pd.to_numeric(out["income"], errors="coerce")
    out["satisfaction_score"] = pd.to_numeric(out["satisfaction_score"], errors="coerce")

    # Standardize text: strip, lower, collapse multiple spaces
    for col in ["region", "feedback", "contact_email"]:
        if col in out.columns and out[col].dtype == object:
            out[col] = (
                out[col]
                .astype(str)
                .str.strip()
                .str.lower()
                .str.replace(r"\s+", " ", regex=True)
            )
            out[col] = out[col].replace("nan", np.nan)

    # Fill strategy per column (justified in comments):
    # age: median — robust to outliers; invalid ages will be NaN and filled with median.
    # income: median — same reason for skewed income.
    # satisfaction_score: mode/median (3 or 4) — ordinal, median is reasonable.
    # region/feedback/contact_email: fill with placeholder or drop rows; we use "unknown" for categorical.
    age_median = out["age"].median()
    out["age"] = out["age"].fillna(age_median)
    out["income"] = out["income"].fillna(out["income"].median())
    out["satisfaction_score"] = out["satisfaction_score"].fillna(out["satisfaction_score"].median()).clip(1, 5)
    out["region"] = out["region"].fillna("unknown")
    out["feedback"] = out["feedback"].fillna("")
    out["contact_email"] = out["contact_email"].replace("", np.nan)  # keep email NaN if empty

    # Clip invalid ages to valid range
    out["age"] = out["age"].clip(0, 120)

    # Drop unfixable rows: e.g. rows where critical columns are still null after fill
    out = out.dropna(subset=["respondent_id", "age", "satisfaction_score"])
    # Remove duplicates
    out = out.drop_duplicates()

    return out.reset_index(drop=True)


def main() -> None:
    out_dir = Path(__file__).resolve().parent
    out_dir.mkdir(parents=True, exist_ok=True)

    # Create and (optionally) save raw survey
    raw = create_messy_survey()
    raw_path = out_dir / "survey_results.csv"
    raw.to_csv(raw_path, index=False)

    # Detect issues
    report_before = detect_issues(raw)
    print("=== Data quality report (before) ===\n")
    print(json.dumps(report_before, indent=2))

    # Clean
    cleaned = clean_data(raw)
    report_after = detect_issues(cleaned)

    # Before/after comparison: rows, nulls, dtypes, memory
    mem_before = raw.memory_usage(deep=True).sum() / (1024 * 1024)
    mem_after = cleaned.memory_usage(deep=True).sum() / (1024 * 1024)
    print("\n=== Before / After comparison ===")
    print(f"Rows:     {len(raw):>6}  ->  {len(cleaned):>6}")
    print(f"Nulls:    {raw.isnull().sum().sum():>6}  ->  {cleaned.isnull().sum().sum():>6}")
    print(f"Memory:   {mem_before:.4f} MB  ->  {mem_after:.4f} MB")
    print("\nDtypes (before):")
    print(raw.dtypes)
    print("\nDtypes (after):")
    print(cleaned.dtypes)

    # Export
    cleaned_path = out_dir / "cleaned_survey.csv"
    cleaned.to_csv(cleaned_path, index=False)
    report_path = out_dir / "data_quality_report.json"
    export_report = {
        "before": report_before,
        "after": report_after,
        "rows_before": len(raw),
        "rows_after": len(cleaned),
    }
    with open(report_path, "w") as f:
        json.dump(export_report, f, indent=2)
    print(f"\nExported: {cleaned_path.name}, {report_path.name}")


if __name__ == "__main__":
    main()
