# Part D: AI-Augmented Task — Auto-Clean DataFrame

## Documented prompt

**Exact prompt used:**

> Write a Python function that takes a messy Pandas DataFrame and automatically cleans it: detect and replace hidden missing values ('N/A', '', 'null', 'None'), convert object columns to appropriate types (numeric or datetime), standardize text columns (strip, lower), and remove duplicate rows. Return the cleaned DataFrame and a summary of all changes made.

## Implementation

The function `auto_clean_dataframe(df)` in `auto_clean_dataframe.py` does the following:

1. **Hidden missing:** Replaces a fixed list (N/A, n/a, NA, null, None, nan, empty string, space, '-') with `np.nan` in object/string columns.
2. **Type conversion:** For each object column, tries `pd.to_numeric` (after removing commas) and then `pd.to_datetime`; converts if a majority of non-null values parse successfully.
3. **Text standardize:** For object/string columns: strip, lower, collapse multiple spaces.
4. **Duplicates:** Drops duplicate rows.
5. **Summary:** Returns a dict with counts and lists (hidden_missing_replaced, columns_converted, text_standardized, duplicates_removed, rows_before, rows_after).

## Tests

- **Test 1:** Run on `survey_results.csv` (from survey_cleaner.py). Summary shows replaced hidden missing, converted columns, standardized text, and duplicate count.
- **Test 2:** Run on `messy_data.csv`. If the file does not exist (e.g. “from class”), the script creates a small `messy_data.csv` and runs the cleaner on it.

Run: `python auto_clean_dataframe.py`

## Critical evaluation (~200 words)

**Edge cases:** All-NaN columns are left as-is; the function does not drop them. Mixed date formats are handled only via `pd.to_datetime(..., errors='coerce')`, so some formats may become NaT. No explicit handling of mixed numeric formats (e.g. "1.5" vs "1,500") beyond comma removal. So edge cases are partially covered.

**Fill strategy:** The function does not fill missing values; it only replaces hidden markers with NaN and converts types. So there is no “fill strategy per column”—that would need to be a separate step (as in survey_cleaner.py). For a generic auto-cleaner, “no fill” is a safe default; the user can then decide.

**Documentation of changes:** The summary dict documents what was done (counts and column lists). It does not record cell-level before/after values, which would be heavy for 1M rows.

**Improvements:** (1) Option to drop all-NaN columns. (2) Configurable list of hidden-missing tokens. (3) Optional fill strategies (e.g. median for numeric) with a parameter. (4) For dates, try multiple formats or use `format='mixed'` (pandas 2+) where available.

**Performance on 1M rows:** The current implementation is vectorized (no row-wise Python loops), so it should scale. The main cost is type conversion and string operations; for 1M rows and a few dozen columns, runtimes of tens of seconds are typical. Chunked processing would be needed only for much larger DataFrames.
