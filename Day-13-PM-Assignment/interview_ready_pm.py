"""
Day 13 PM Part C: Interview Ready — Q2 standardize_column(), Q3 fixed buggy code.
Q1 conceptual answer is in interview_answers_pm.md.
"""

import re
from pathlib import Path

import pandas as pd


def standardize_column(series: pd.Series) -> pd.Series:
    """
    Clean messy text: strip whitespace, lowercase, multiple spaces → single space,
    special characters removed. Handles NaN (keeps as NaN).
    """
    out = series.astype(str).str.strip().str.lower()
    out = out.str.replace(r"\s+", " ", regex=True)
    # Remove non-alphanumeric and non-space (keep letters, digits, space)
    out = out.str.replace(r"[^a-z0-9\s]", "", regex=True)
    out = out.str.strip()
    # Restore NaN where original was null or became empty
    out = out.replace("", pd.NA).replace("nan", pd.NA)
    return out


def demo_standardize() -> None:
    """Test standardize_column with the assignment example."""
    test = pd.Series([
        "  Hello  World!! ",
        "  NEW YORK  ",
        "san--francisco",
        "   MUMBAI   ",
    ])
    result = standardize_column(test)
    print("Input:")
    print(test)
    print("Output:")
    print(result)


# ---------------------------------------------------------------------------
# Q3: Fixed 4 bugs in the data cleaning code
# ---------------------------------------------------------------------------
# Bug 1: Replace hidden NaN (N/A, etc.) before to_numeric.
# Bug 2: Use (df["price"] > 1000) & (df["category"] != "") not "and".
# Bug 3: .str.contains on column with NaN → use na=False or fillna before.
# Bug 4: to_datetime with mixed formats → use errors='coerce' or format.
# ---------------------------------------------------------------------------


def demo_fixed_bugs() -> None:
    """Corrected version of the assignment's buggy code."""
    df = pd.DataFrame({
        "price": ["1,500", "2000", "N/A", "3,200", "abc"],
        "category": ["  Electronics ", "CLOTHING", "electronics", " Books", ""],
        "date": ["15/03/2024", "2024-07-01", "22-Nov-2024", "01/10/2024", None],
    })

    # Bug 1: Replace hidden NaN before to_numeric
    df["price"] = df["price"].replace(["N/A", "n/a", "NA", ""], pd.NA)
    df["price"] = df["price"].astype(str).str.replace(",", "", regex=False)
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    # Bug 2: Use & with parentheses for element-wise boolean
    clean = df[(df["price"] > 1000) & (df["category"].str.strip() != "")]

    # Bug 3: .str.contains with na=False to avoid NaN in boolean result
    electronics = df[df["category"].str.contains("electronics", case=False, na=False)]

    # Bug 4: to_datetime with errors='coerce' for mixed/invalid formats
    df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)

    print("Fixed df:")
    print(df)


if __name__ == "__main__":
    print("--- Q2: standardize_column() ---\n")
    demo_standardize()
    print("\n--- Q3: Fixed 4 bugs ---\n")
    demo_fixed_bugs()
