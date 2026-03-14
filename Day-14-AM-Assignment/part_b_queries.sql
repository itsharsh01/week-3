-- Day 14 AM Part B: projects table already in schema_and_data.sql
-- (1) 3-table JOIN: employee name, department budget, project budget
SELECT e.name AS employee_name, d.budget AS department_budget, p.budget AS project_budget, p.project_name
FROM employees e
JOIN departments d ON e.department_id = d.dept_id
JOIN projects p ON p.lead_emp_id = e.emp_id
ORDER BY e.name, p.project_name;

-- (2) Departments where total project budget exceeds department budget
SELECT d.name AS dept_name, d.budget AS dept_budget, SUM(p.budget) AS total_project_budget
FROM departments d
JOIN employees e ON e.department_id = d.dept_id
JOIN projects p ON p.lead_emp_id = e.emp_id
GROUP BY d.dept_id, d.name, d.budget
HAVING SUM(p.budget) > d.budget;
