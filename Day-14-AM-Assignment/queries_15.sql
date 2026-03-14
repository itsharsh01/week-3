-- Day 14 AM Part A: 15 queries (exercise section equivalent)
-- Each query has a comment with the Pandas equivalent concept.

-- ---------- Query 1: Select all employees ----------
SELECT emp_id, name, department_id, salary, hire_date
FROM employees;

-- ---------- Query 2: Filter with WHERE (salary > 70000) ----------
SELECT emp_id, name, salary
FROM employees
WHERE salary > 70000;

-- ---------- Query 3: ORDER BY salary DESC ----------
SELECT name, salary
FROM employees
ORDER BY salary DESC;

-- ---------- Query 4: LIMIT 5 ----------
SELECT name, salary
FROM employees
ORDER BY salary DESC
LIMIT 5;

-- ---------- Query 5: Aggregate COUNT ----------
SELECT COUNT(*) AS total_employees
FROM employees;

-- ---------- Query 6: Aggregate AVG ----------
SELECT AVG(salary) AS avg_salary
FROM employees;

-- ---------- Query 7: GROUP BY department, COUNT and AVG ----------
SELECT d.name AS dept_name, COUNT(e.emp_id) AS emp_count, AVG(e.salary) AS avg_sal
FROM departments d
LEFT JOIN employees e ON d.dept_id = e.department_id
GROUP BY d.dept_id, d.name;

-- ---------- Query 8: GROUP BY with HAVING (avg salary > 65000) ----------
SELECT d.name AS dept_name, AVG(e.salary) AS avg_sal
FROM departments d
JOIN employees e ON d.dept_id = e.department_id
GROUP BY d.dept_id, d.name
HAVING AVG(e.salary) > 65000;

-- ---------- Query 9: INNER JOIN employees and departments ----------
SELECT e.name AS emp_name, d.name AS dept_name, e.salary
FROM employees e
INNER JOIN departments d ON e.department_id = d.dept_id;

-- ---------- Query 10: LEFT JOIN (all departments, employee count) ----------
SELECT d.name AS dept_name, COUNT(e.emp_id) AS emp_count
FROM departments d
LEFT JOIN employees e ON d.dept_id = e.department_id
GROUP BY d.dept_id, d.name;

-- ---------- Query 11: JOIN + WHERE (employees in Engineering) ----------
SELECT e.name, e.salary, d.name AS dept_name
FROM employees e
JOIN departments d ON e.department_id = d.dept_id
WHERE d.name = 'Engineering';

-- ---------- Query 12: ORDER BY multiple columns ----------
SELECT name, department_id, salary
FROM employees
ORDER BY department_id ASC, salary DESC;

-- ---------- Query 13: MIN and MAX salary per department ----------
SELECT d.name AS dept_name, MIN(e.salary) AS min_sal, MAX(e.salary) AS max_sal
FROM departments d
JOIN employees e ON d.dept_id = e.department_id
GROUP BY d.dept_id, d.name;

-- ---------- Query 14: SUM salary by department ----------
SELECT d.name AS dept_name, SUM(e.salary) AS total_salary
FROM departments d
JOIN employees e ON d.dept_id = e.department_id
GROUP BY d.dept_id, d.name;

-- ---------- Query 15: Three columns from JOIN (name, dept, salary) with alias ----------
SELECT e.name AS employee_name, d.name AS department_name, e.salary
FROM employees e
INNER JOIN departments d ON e.department_id = d.dept_id
WHERE e.salary >= 60000
ORDER BY e.salary DESC;
