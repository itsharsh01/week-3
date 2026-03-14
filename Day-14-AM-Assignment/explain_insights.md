# Day 14 AM Part A: EXPLAIN insights (3 queries)

## Query 5: `SELECT COUNT(*) FROM employees`
- **EXPLAIN (SQLite):** Shows a single **Full table scan** on `employees`. No index is used because the entire table is aggregated.
- **Insight:** For a simple COUNT on one table, the planner does one sequential scan. On very large tables, COUNT(*) can be expensive; approximate counts or indexed filters help.

## Query 8: `GROUP BY ... HAVING AVG(salary) > 65000`
- **EXPLAIN (SQLite):** Typically **Scan** on employees, then **Seek** or **Lookup** on departments for the JOIN, then a **Sort** or **Aggregate** for GROUP BY, then filter by HAVING.
- **Insight:** HAVING is applied after aggregation. The planner first computes groups, then discards groups that fail the HAVING condition. Indexes on JOIN/GROUP BY columns can reduce sort cost.

## Query 15: `INNER JOIN ... WHERE ... ORDER BY`
- **EXPLAIN (SQLite):** Usually **Nested loop** join (scan one table, lookup the other), then **Filter** for WHERE, then **Sort** for ORDER BY.
- **Insight:** Join order and indexes on `department_id` / `dept_id` affect whether the plan uses a lookup vs a full scan. The final sort can be expensive; an index on the ORDER BY columns could allow a scan in order and avoid a separate sort.
