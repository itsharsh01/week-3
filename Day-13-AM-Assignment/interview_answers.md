# Day 13 AM Part C — Interview Ready Answers

## Q1 (Conceptual): .loc[] vs .iloc[]

- **`.loc[]`** is **label-based**: you use index labels and column names. Slices are **inclusive** on both ends.
- **`.iloc[]`** is **position-based**: you use integer positions (0-based). Slices follow Python slicing: **start inclusive, stop exclusive**.

### Example: `df.loc[0:3]` vs `df.iloc[0:3]`

**When the index is 0, 1, 2, 3, 4:**
- `df.loc[0:3]` → rows with **labels** 0, 1, 2, 3 (4 rows). Label 3 is included.
- `df.iloc[0:3]` → rows at **positions** 0, 1, 2 (3 rows). Position 3 is excluded.

**When the index is 'a', 'b', 'c', 'd', 'e':**
- `df.loc[0:3]` → would raise an error or return nothing if there are no integer labels 0–3. With **string** index, you’d use something like `df.loc['a':'c']` to get rows 'a', 'b', 'c' (inclusive).
- `df.iloc[0:3]` → still the first 3 **positions** (rows 0, 1, 2), i.e. 'a', 'b', 'c'. Position is independent of index labels.

So: **loc** = “by label,” **iloc** = “by position”; **loc** slices are inclusive on the end, **iloc** slices are exclusive on the end (like Python).
