"""
Day 13 PM Part D: Auto-clean messy DataFrame.
Detect/replace hidden missing, convert types, standardize text, remove duplicates.
Returns cleaned DataFrame and summary of changes.
"""

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

HIDDEN_MISSING = ["N/A", "n/a", "NA", "null", "NULL", "None", "nan", "", " ", "-"]


def auto_clean_dataframe(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    """
    Clean a messy DataFrame: replace hidden missing, convert types, standardize text,
    remove duplicates. Returns (cleaned_df, summary_dict).
    """
    summary: dict[str, Any] = {
        "hidden_missing_replaced": 0,
        "columns_converted": [],
        "text_standardized": [],
        "duplicates_removed": 0,
        "rows_before": len(df),
        "rows_after": None,
    }
    out = df.copy()

    # 1. Replace hidden missing
    for col in out.columns:
        if out[col].dtype == object or out[col].dtype.name == "string":
            before = out[col].isna().sum()
            out[col] = out[col].replace(HIDDEN_MISSING, np.nan)
            summary["hidden_missing_replaced"] += int(out[col].isna().sum() - before)

    # 2. Convert object columns to numeric or datetime where possible
    for col in out.columns:
        if out[col].dtype not in ["int64", "float64", "bool"]:
            ser = out[col].dropna()
            if len(ser) == 0:
                continue
            # Try numeric
            try:
                cleaned = ser.astype(str).str.replace(",", "", regex=False)
                converted = pd.to_numeric(cleaned, errors="coerce")
                if converted.notna().sum() / len(ser) > 0.5:
                    out[col] = pd.to_numeric(out[col].astype(str).str.replace(",", "", regex=False), errors="coerce")
                    summary["columns_converted"].append((col, "numeric"))
                    continue
            except Exception:
                pass
            # Try datetime
            try:
                converted = pd.to_datetime(out[col], errors="coerce")
                if converted.notna().sum() / len(out) > 0.3:
                    out[col] = converted
                    summary["columns_converted"].append((col, "datetime"))
            except Exception:
                pass

    # 3. Standardize text (strip, lower)
    for col in out.columns:
        if out[col].dtype == object or out[col].dtype.name == "string":
            out[col] = out[col].astype(str).str.strip().str.lower().str.replace(r"\s+", " ", regex=True)
            out[col] = out[col].replace("nan", np.nan)
            summary["text_standardized"].append(col)

    # 4. Remove duplicate rows
    n_before = len(out)
    out = out.drop_duplicates()
    summary["duplicates_removed"] = n_before - len(out)
    summary["rows_after"] = len(out)

    return out, summary


def main() -> None:
    base = Path(__file__).resolve().parent

    # Test 1: messy survey (use raw from survey_cleaner or load survey_results)
    survey_path = base / "survey_results.csv"
    if survey_path.is_file():
        df = pd.read_csv(survey_path)
        cleaned, summary = auto_clean_dataframe(df)
        print("=== Test 1: survey_results.csv ===\n")
        print("Summary:", summary)
        print("\nCleaned shape:", cleaned.shape)
    else:
        print("Run survey_cleaner.py first to create survey_results.csv")

    # Test 2: messy_data.csv (create minimal if not present)
    messy_path = base / "messy_data.csv"
    if messy_path.is_file():
        df2 = pd.read_csv(messy_path)
        cleaned2, summary2 = auto_clean_dataframe(df2)
        print("\n=== Test 2: messy_data.csv ===\n")
        print("Summary:", summary2)
    else:
        # Create a small messy_data.csv for testing
        small = pd.DataFrame({
            "id": [1, 2, 3],
            "value": ["1,000", "N/A", "2000"],
            "name": ["  Alice  ", "BOB", ""],
        })
        small.to_csv(messy_path, index=False)
        cleaned2, summary2 = auto_clean_dataframe(small)
        print("\n=== Test 2: generated messy_data.csv ===\n")
        print("Summary:", summary2)
        print("Cleaned:\n", cleaned2)


if __name__ == "__main__":
    main()
