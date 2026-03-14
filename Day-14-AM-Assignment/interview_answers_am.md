# Day 14 AM Part C — Interview Ready

## Q1 — Logical execution order of a SQL SELECT; why it matters for aliases

**Logical order:** FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT/OFFSET.

So the database first builds the table (FROM, JOINs), then filters rows (WHERE), then groups (GROUP BY), then filters groups (HAVING), then computes expressions and aliases (SELECT), then sorts (ORDER BY), then applies LIMIT.

**Why it matters for aliases:** In the SELECT phase you can define column aliases (e.g. `SELECT salary * 1.1 AS new_sal`). Those aliases are **not** visible in WHERE or GROUP BY, because those are evaluated **before** SELECT. So you cannot write `WHERE new_sal > 70000` if `new_sal` is defined only in SELECT. You can use aliases in ORDER BY and in LIMIT, because those are evaluated **after** SELECT. In some databases you can also use SELECT aliases in HAVING. So knowing the order avoids "column/alias not found" errors and clarifies where you can reuse an alias.

---

## Q2 — Employee name, salary, and department average salary (for employees above company-wide average), without subqueries or CTEs

Use window functions: compute company-wide average and department average with window functions, then filter in WHERE.

```sql
SELECT name, salary, dept_avg
FROM (
    SELECT name, salary,
           AVG(salary) OVER (PARTITION BY department_id) AS dept_avg,
           AVG(salary) OVER () AS company_avg
    FROM employees
) t
WHERE salary > company_avg;
```

(If the engine does not allow referencing window results in WHERE of the same level, use a derived table as above: compute in inner SELECT, filter in outer WHERE.)

---

## Q3 (Debug) — Bug in the query

**Bug:** `WHERE AVG(salary) > 70000` is invalid. Aggregates like `AVG(salary)` are computed per group and are not allowed in `WHERE`, because `WHERE` runs before grouping.

**Fix:** Use `HAVING` to filter after aggregation:

```sql
SELECT department, AVG(salary) AS avg_sal
FROM employees
GROUP BY department
HAVING AVG(salary) > 70000;
```
