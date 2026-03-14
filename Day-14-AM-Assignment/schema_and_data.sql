-- Day 14 AM: Schema and sample data for SQL foundations assignment
-- Compatible with SQLite (and PostgreSQL with minor adjustments)

-- ========== DDL ==========
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS departments;

CREATE TABLE departments (
    dept_id   INTEGER PRIMARY KEY,
    name     TEXT NOT NULL,
    budget   REAL NOT NULL
);

CREATE TABLE employees (
    emp_id        INTEGER PRIMARY KEY,
    name          TEXT NOT NULL,
    department_id INTEGER NOT NULL REFERENCES departments(dept_id),
    salary        REAL NOT NULL,
    hire_date     TEXT,
    CONSTRAINT fk_dept FOREIGN KEY (department_id) REFERENCES departments(dept_id)
);

CREATE TABLE projects (
    project_id   INTEGER PRIMARY KEY,
    project_name TEXT NOT NULL,
    lead_emp_id  INTEGER NOT NULL REFERENCES employees(emp_id),
    budget       REAL NOT NULL,
    start_date   TEXT,
    end_date     TEXT,
    CONSTRAINT fk_lead FOREIGN KEY (lead_emp_id) REFERENCES employees(emp_id)
);

-- ========== Sample data ==========
INSERT INTO departments (dept_id, name, budget) VALUES
(1, 'Engineering', 500000),
(2, 'Sales', 300000),
(3, 'HR', 150000),
(4, 'Marketing', 200000);

INSERT INTO employees (emp_id, name, department_id, salary, hire_date) VALUES
(1, 'Alice', 1, 85000, '2020-01-15'),
(2, 'Bob', 1, 72000, '2021-03-01'),
(3, 'Carol', 2, 68000, '2019-06-10'),
(4, 'Dave', 2, 71000, '2022-02-20'),
(5, 'Eve', 3, 55000, '2020-11-05'),
(6, 'Frank', 1, 90000, '2018-04-12'),
(7, 'Grace', 4, 62000, '2021-08-30'),
(8, 'Henry', 2, 65000, '2020-05-18'),
(9, 'Ivy', 3, 58000, '2022-01-10'),
(10, 'Jack', 1, 78000, '2019-09-22');

INSERT INTO projects (project_id, project_name, lead_emp_id, budget, start_date, end_date) VALUES
(1, 'Alpha', 1, 100000, '2023-01-01', '2023-06-30'),
(2, 'Beta', 2, 80000, '2023-02-01', '2023-08-31'),
(3, 'Gamma', 6, 120000, '2023-03-01', '2023-12-31'),
(4, 'Delta', 3, 50000, '2023-04-01', '2023-09-30'),
(5, 'Epsilon', 4, 60000, '2023-05-01', '2023-10-31');
