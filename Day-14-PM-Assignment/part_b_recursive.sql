-- Day 14 PM Part B: Recursive CTE and fill missing dates

-- ---------- 1. Number series 1 to 100 using recursive CTE (no hard-coded values) ----------
WITH RECURSIVE nums(n) AS (
    SELECT 1
    UNION ALL
    SELECT n + 1 FROM nums WHERE n < 100
)
SELECT n FROM nums ORDER BY n;

-- ---------- 2. Fill missing dates in sparse time series (dates with no orders get revenue=0) ----------
-- Assume we have a sparse table: order_dates with (order_date, revenue). We generate all dates in range and LEFT JOIN.

-- Create a sparse sample (only some dates have rows)
DROP TABLE IF EXISTS sparse_revenue;
CREATE TABLE sparse_revenue (sale_date TEXT PRIMARY KEY, revenue REAL);
INSERT INTO sparse_revenue VALUES ('2024-01-01', 100), ('2024-01-03', 150), ('2024-01-05', 200);
-- Missing: 2024-01-02, 2024-01-04

-- Recursive CTE to generate all dates from min to max
WITH RECURSIVE date_range(d) AS (
    SELECT (SELECT MIN(sale_date) FROM sparse_revenue)
    UNION ALL
    SELECT date(d, '+1 day') FROM date_range
    WHERE d < (SELECT MAX(sale_date) FROM sparse_revenue)
)
SELECT dr.d AS sale_date, COALESCE(sr.revenue, 0) AS revenue
FROM date_range dr
LEFT JOIN sparse_revenue sr ON sr.sale_date = dr.d
ORDER BY dr.d;
