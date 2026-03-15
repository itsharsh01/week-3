"""
Day 16 PM Part B: Recreate 3 charts as interactive Plotly Express; save as HTML.
Run: pip install plotly pandas; python visualization_plotly.py
"""
from pathlib import Path

import pandas as pd
import plotly.express as px

OUT_DIR = Path(__file__).resolve().parent
CSV_PATH = OUT_DIR / "eda_assignment_data.csv"


def main() -> None:
    df = pd.read_csv(CSV_PATH)

    # 1. Histogram with density (distribution) — sales
    fig1 = px.histogram(df, x="sales", nbins=40, title="Sales distribution (interactive)")
    fig1.update_layout(xaxis_title="Sales", yaxis_title="Count")
    fig1.write_html(OUT_DIR / "plotly_histogram.html")
    print("Saved plotly_histogram.html")

    # 2. Scatter with regression line — price vs sales
    fig2 = px.scatter(df, x="price", y="sales", trendline="ols", title="Price vs Sales with trend (interactive)")
    fig2.update_layout(xaxis_title="Price", yaxis_title="Sales")
    fig2.write_html(OUT_DIR / "plotly_scatter_regression.html")
    print("Saved plotly_scatter_regression.html")

    # 3. Box plot — key metric across categories
    fig3 = px.box(df, x="category", y="sales", title="Sales by category (interactive)")
    fig3.update_layout(xaxis_title="Category", yaxis_title="Sales")
    fig3.write_html(OUT_DIR / "plotly_box.html")
    print("Saved plotly_box.html")


if __name__ == "__main__":
    main()
