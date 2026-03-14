"""
Day 14 AM: Run SQL queries and Pandas equivalents; compare results.
Run schema_and_data.sql first to create day14_am.db, or this script creates it.
"""
import sqlite3
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent
DB_PATH = BASE / "day14_am.db"
SCHEMA_PATH = BASE / "schema_and_data.sql"


def setup_db():
    if not SCHEMA_PATH.exists():
        print("Missing schema_and_data.sql")
        return None
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA_PATH.read_text())
    conn.commit()
    return conn


def main():
    conn = setup_db()
    if conn is None:
        return
    employees = pd.read_sql_query("SELECT * FROM employees", conn)
    departments = pd.read_sql_query("SELECT * FROM departments", conn)

    # Run a few representative queries and show SQL vs Pandas match
    q2_sql = pd.read_sql_query("SELECT name, salary FROM employees WHERE salary > 70000", conn)
    q2_pd = employees.loc[employees["salary"] > 70000, ["name", "salary"]].reset_index(drop=True)
    print("Q2 (WHERE): SQL rows =", len(q2_sql), ", Pandas rows =", len(q2_pd), "-> Match:", len(q2_sql) == len(q2_pd))

    q6_sql = pd.read_sql_query("SELECT AVG(salary) AS avg_salary FROM employees", conn)
    q6_pd = employees["salary"].mean()
    print("Q6 (AVG): SQL avg =", q6_sql["avg_salary"].iloc[0], ", Pandas avg =", q6_pd, "-> Match:", abs(q6_sql["avg_salary"].iloc[0] - q6_pd) < 1e-5)

    q9_sql = pd.read_sql_query(
        "SELECT e.name AS emp_name, d.name AS dept_name FROM employees e JOIN departments d ON e.department_id = d.dept_id",
        conn,
    )
    merged = employees.merge(departments, left_on="department_id", right_on="dept_id", suffixes=("_emp", "_dept"))
    q9_pd = merged[["name_emp", "name_dept"]].rename(columns={"name_emp": "emp_name", "name_dept": "dept_name"})
    print("Q9 (JOIN): SQL rows =", len(q9_sql), ", Pandas rows =", len(q9_pd), "-> Match:", len(q9_sql) == len(q9_pd))

    # EXPLAIN for 3 queries (SQLite)
    for label, sql in [
        ("Q5 COUNT", "SELECT COUNT(*) FROM employees"),
        ("Q8 HAVING", "SELECT d.name FROM departments d JOIN employees e ON d.dept_id = e.department_id GROUP BY d.dept_id HAVING AVG(e.salary) > 65000"),
        ("Q15 JOIN+ORDER", "SELECT e.name, e.salary FROM employees e JOIN departments d ON e.department_id = d.dept_id WHERE e.salary >= 60000 ORDER BY e.salary DESC"),
    ]:
        plan = pd.read_sql_query("EXPLAIN QUERY PLAN " + sql, conn)
        print(f"\nEXPLAIN {label}:\n", plan.to_string())

    conn.close()
    print("\nComparison done. See explain_insights.md for interpretation.")


if __name__ == "__main__":
    main()
