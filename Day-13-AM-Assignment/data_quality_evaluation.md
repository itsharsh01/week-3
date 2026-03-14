# Part D: AI-Augmented Task — Data Quality Report

## Documented prompt

**Exact prompt used (for AI):**

> Write a Python function that takes a Pandas DataFrame and generates an automated data quality report including: shape, dtypes, missing values percentage, duplicate rows, unique value counts per column, and basic stats. Return the report as a dict and also print a formatted summary.

## Implementation (function behavior)

The implemented function `data_quality_report(df)` in `data_quality_report.py`:

- Returns a dict with: `shape`, `dtypes`, `missing_pct`, `duplicate_rows`, `unique_counts`, `memory_mb`, `numeric_stats`, and `single_value_columns`.
- Prints a formatted summary with section headers.
- Uses `df.memory_usage(deep=True)` for memory and identifies columns with only one unique value (candidate useless features).

## Tests

**Test 1 — Clean DataFrame:** 3 rows × 3 columns, no nulls, no duplicates. Report shows shape, dtypes, 0% missing, 0 duplicates, unique counts, and numeric describe.

**Test 2 — Messy DataFrame:** 5 rows, nulls in `y`, duplicate rows, and a column `constant` with a single value. Report shows missing %, duplicate count, and flags `constant` in `single_value_columns`.

Run: `python data_quality_report.py`

## Critical evaluation (~200 words)

**Edge cases:** The function handles an empty DataFrame by returning a minimal report and avoiding describe/memory on empty columns. All-null columns appear correctly in `missing_pct` (100%) and in `unique_counts` (0). So empty and all-null cases are covered.

**Memory:** The implementation uses `df.memory_usage(deep=True).sum()` and reports `memory_mb`, so memory is included as required.

**Single-value columns:** The report includes `single_value_columns` (columns with ≤1 unique value), which helps spot useless or constant features that are often dropped before modeling.

**Improvements:** (1) For very wide DataFrames, printing every column’s dtype/unique might be truncated or noisy — could add a `max_cols` or summary-by-dtype. (2) No explicit handling of infinite values in numeric columns; adding a check for `np.isinf` would improve robustness. (3) Categorical columns could get value distribution (e.g. value_counts) in the report. (4) Optional export of the report to JSON or YAML would help automation. (5) Duplicate *columns* (same values across two columns) are not detected; that could be an extra check.

Overall, the function meets the brief, handles empty and messy data, uses `memory_usage()`, and identifies single-value columns; the suggested improvements would make it more production-ready.
