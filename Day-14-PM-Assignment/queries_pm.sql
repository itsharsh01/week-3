-- Day 14 PM Part A: 5 queries (window functions, CTEs, correlated subquery)

-- ---------- 1. Running total: cumulative revenue per product category ordered by date ----------
SELECT category, sale_date, revenue,
       SUM(revenue) OVER (PARTITION BY category ORDER BY sale_date
                          ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM revenue_by_category
ORDER BY category, sale_date;

-- ---------- 2. Top-N: top-3 customers by revenue per city (ROW_NUMBER) ----------
SELECT city, name, total_revenue, rn
FROM (
    SELECT c.city, c.name,
           SUM(o.amount) AS total_revenue,
           ROW_NUMBER() OVER (PARTITION BY c.city ORDER BY SUM(o.amount) DESC) AS rn
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.city, c.name
) t
WHERE rn <= 3
ORDER BY city, rn;

-- ---------- 3. MoM growth: month-over-month revenue change % using LAG; flag months with < -5% ----------
WITH monthly AS (
    SELECT strftime('%Y-%m', sale_date) AS month, SUM(revenue) AS rev
    FROM revenue_by_category
    GROUP BY strftime('%Y-%m', sale_date)
),
with_prev AS (
    SELECT month, rev, LAG(rev) OVER (ORDER BY month) AS prev_rev
    FROM monthly
)
SELECT month, rev, prev_rev,
       CASE WHEN prev_rev > 0 THEN ROUND(100.0 * (rev - prev_rev) / prev_rev, 2) END AS pct_change,
       CASE WHEN prev_rev > 0 AND 100.0 * (rev - prev_rev) / prev_rev < -5 THEN 1 ELSE 0 END AS flag_below_5pct
FROM with_prev
ORDER BY month;

-- ---------- 4. Multi-CTE: departments where ALL employees earn above the company average ----------
WITH company_avg AS (SELECT AVG(salary) AS avg_sal FROM employees),
     dept_mins AS (
         SELECT department_id, MIN(salary) AS min_sal
         FROM employees GROUP BY department_id
     )
SELECT d.name AS dept_name
FROM departments d
JOIN dept_mins dm ON d.dept_id = dm.department_id
CROSS JOIN company_avg ca
WHERE dm.min_sal > ca.avg_sal;

-- ---------- 5. Correlated subquery: 2nd highest salary per department (WITHOUT window functions) ----------
SELECT e.department_id, e.name, e.salary
FROM employees e
WHERE (
    SELECT COUNT(DISTINCT e2.salary)
    FROM employees e2
    WHERE e2.department_id = e.department_id AND e2.salary >= e.salary
) = 2
ORDER BY e.department_id, e.salary DESC;
