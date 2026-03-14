-- Day 14 PM: Schema for Subqueries, Window Functions, CTEs
-- SQLite-compatible (window functions supported in 3.25+)

DROP TABLE IF EXISTS revenue_by_category;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS departments;

-- For running total: revenue per product category by date
CREATE TABLE revenue_by_category (
    id INTEGER PRIMARY KEY,
    category TEXT NOT NULL,
    sale_date TEXT NOT NULL,
    revenue REAL NOT NULL
);

-- Customers and cities for top-N by revenue
CREATE TABLE customers (customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount REAL);

-- Transactions for consecutive months (user_id, transaction_date, amount)
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    transaction_date TEXT NOT NULL,
    amount REAL NOT NULL
);

-- Employees/departments for multi-CTE and 2nd-highest salary
CREATE TABLE departments (dept_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE employees (emp_id INTEGER PRIMARY KEY, name TEXT, department_id INTEGER, salary REAL);

-- Sample data: revenue by category and date
INSERT INTO revenue_by_category (category, sale_date, revenue) VALUES
('Electronics', '2024-01-01', 1000), ('Electronics', '2024-01-02', 1500), ('Electronics', '2024-01-03', 1200),
('Clothing', '2024-01-01', 800), ('Clothing', '2024-01-02', 900), ('Clothing', '2024-01-03', 1100);

-- Customers and orders
INSERT INTO customers VALUES (1, 'Alice', 'NYC'), (2, 'Bob', 'NYC'), (3, 'Carol', 'LA'), (4, 'Dave', 'LA'), (5, 'Eve', 'NYC');
INSERT INTO orders VALUES (1, 1, '2024-01-01', 200), (2, 1, '2024-01-15', 150), (3, 2, '2024-01-10', 300), (4, 3, '2024-01-05', 250), (5, 4, '2024-01-20', 100), (6, 5, '2024-01-25', 400);

-- Transactions for consecutive months
INSERT INTO transactions (user_id, transaction_date, amount) VALUES
(1, '2024-01-01', 50), (1, '2024-02-01', 60), (1, '2024-03-01', 70),
(2, '2024-01-15', 100), (2, '2024-02-15', 80), (2, '2024-03-15', 90),
(3, '2024-02-01', 30), (3, '2024-03-01', 40), (3, '2024-04-01', 50);

-- Departments and employees (for multi-CTE and 2nd salary)
INSERT INTO departments VALUES (1, 'Eng'), (2, 'Sales');
INSERT INTO employees VALUES (1, 'Alice', 1, 100000), (2, 'Bob', 1, 90000), (3, 'Carol', 1, 85000), (4, 'Dave', 2, 70000), (5, 'Eve', 2, 75000);
