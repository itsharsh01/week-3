# Day 14 PM Part C — Interview Ready

## Q1 — RANK() vs DENSE_RANK(); when the difference matters

- **RANK():** Ties get the same rank; the next rank skips (e.g. 1, 2, 2, 4).
- **DENSE_RANK():** Ties get the same rank; the next rank does not skip (e.g. 1, 2, 2, 3).

**When it matters in business:** If you need "top N" and want exactly N rows (e.g. "top 3 products"), DENSE_RANK can still return more than 3 if there are ties for 3rd. RANK can skip ranks after ties, so "rank <= 3" might return 3 or more rows. For "give me the 2nd place" with ties, RANK gives one 2nd and then 4th; DENSE_RANK gives 2nd and then 3rd. So for leaderboards or eligibility (e.g. "all 2nd-place finishers"), the choice changes who is included.

---

## Q2 — Users who made a purchase in 3 or more consecutive months (window functions)

Idea: assign a "month group" per user by subtracting ROW_NUMBER() over months from the month value; consecutive months share the same group. Then count months per group and filter >= 3.

```sql
WITH m AS (
    SELECT user_id, strftime('%Y-%m', transaction_date) AS month
    FROM transactions
    GROUP BY user_id, strftime('%Y-%m', transaction_date)
),
with_grp AS (
    SELECT user_id, month,
           date(month || '-01', '-' || (ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY month)) || ' months') AS grp
    FROM m
),
consec AS (
    SELECT user_id, grp, COUNT(*) AS cnt
    FROM with_grp
    GROUP BY user_id, grp
)
SELECT DISTINCT user_id FROM consec WHERE cnt >= 3;
```

Alternative: use LAG to get prev month; count consecutive chains (e.g. where month = prev + 1 month).

---

## Q3 — Rewrite correlated subquery as window function

**Original:**
```sql
SELECT name, salary FROM employees e1
WHERE salary > (SELECT AVG(salary) FROM employees e2 WHERE e2.department = e1.department);
```

**Window version:**
```sql
SELECT name, salary
FROM (
    SELECT name, salary, AVG(salary) OVER (PARTITION BY department_id) AS dept_avg
    FROM employees
) t
WHERE salary > dept_avg;
```

**Why better:** Correlated subquery runs the inner query per row (O(n²) style). The window function scans once, computes AVG per partition, and then filters — one pass (O(n) for the aggregation). So it scales better and is easier for the optimizer to handle.
