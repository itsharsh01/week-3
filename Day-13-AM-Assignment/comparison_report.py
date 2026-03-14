"""
Multi-DataFrame Comparison Report (Day 13 AM Part B).
Creates 3 months of sales data, computes metrics, summary DataFrame, uses .query(), nlargest/nsmallest.
"""

import pandas as pd


def build_month_sales(month: str, rows: list[dict]) -> pd.DataFrame:
    """Build a sales DataFrame for one month (product, quantity, unit_price, order_id)."""
    df = pd.DataFrame(rows)
    df["month"] = month
    return df


def main() -> None:
    # Three separate DataFrames for 3 months
    jan = build_month_sales(
        "January",
        [
            {"product": "Laptop", "quantity": 12, "unit_price": 45000, "order_id": "J1"},
            {"product": "Mouse", "quantity": 45, "unit_price": 899, "order_id": "J2"},
            {"product": "Keyboard", "quantity": 20, "unit_price": 5500, "order_id": "J3"},
            {"product": "Laptop", "quantity": 8, "unit_price": 45000, "order_id": "J4"},
            {"product": "Monitor", "quantity": 15, "unit_price": 18500, "order_id": "J5"},
        ],
    )
    feb = build_month_sales(
        "February",
        [
            {"product": "Laptop", "quantity": 10, "unit_price": 45000, "order_id": "F1"},
            {"product": "Headphones", "quantity": 35, "unit_price": 3999, "order_id": "F2"},
            {"product": "Monitor", "quantity": 18, "unit_price": 18500, "order_id": "F3"},
            {"product": "Mouse", "quantity": 60, "unit_price": 899, "order_id": "F4"},
            {"product": "Laptop", "quantity": 5, "unit_price": 45000, "order_id": "F5"},
        ],
    )
    mar = build_month_sales(
        "March",
        [
            {"product": "Smart Watch", "quantity": 25, "unit_price": 12500, "order_id": "M1"},
            {"product": "Laptop", "quantity": 14, "unit_price": 45000, "order_id": "M2"},
            {"product": "Keyboard", "quantity": 30, "unit_price": 5500, "order_id": "M3"},
            {"product": "Monitor", "quantity": 12, "unit_price": 18500, "order_id": "M4"},
            {"product": "Mouse", "quantity": 80, "unit_price": 899, "order_id": "M5"},
        ],
    )

    all_months = [jan, feb, mar]
    month_names = ["January", "February", "March"]

    # Add revenue column for each
    for frame in all_months:
        frame["revenue"] = frame["quantity"] * frame["unit_price"]

    # For each month: total revenue, average order value, top-selling product
    results = []
    for name, df in zip(month_names, all_months):
        total_revenue = df["revenue"].sum()
        num_orders = df["order_id"].nunique()
        avg_order_value = total_revenue / num_orders if num_orders else 0
        # Top-selling product by quantity
        by_product = df.groupby("product", as_index=False)["quantity"].sum()
        top_product = by_product.nlargest(1, "quantity").iloc[0]
        top_name = top_product["product"]
        top_qty = int(top_product["quantity"])
        results.append(
            {
                "month": name,
                "total_revenue": total_revenue,
                "avg_order_value": round(avg_order_value, 2),
                "top_selling_product": top_name,
                "top_selling_quantity": top_qty,
            }
        )

    # Summary comparison DataFrame: months as index, metrics as columns
    summary = pd.DataFrame(results).set_index("month")
    print("=== Summary comparison (months × metrics) ===\n")
    print(summary)

    # Use .query() for filtering (e.g. orders with quantity > 20)
    print("\n=== .query() example: quantity > 20 ===")
    combined = pd.concat([jan, feb, mar], ignore_index=True)
    high_qty = combined.query("quantity > 20")
    print(high_qty)

    # .nlargest() and .nsmallest() for outliers
    print("\n=== .nlargest(2) revenue per row ===")
    print(combined.nlargest(2, "revenue")[["product", "quantity", "unit_price", "revenue"]])

    print("\n=== .nsmallest(2) revenue per row ===")
    print(combined.nsmallest(2, "revenue")[["product", "quantity", "unit_price", "revenue"]])


if __name__ == "__main__":
    main()
