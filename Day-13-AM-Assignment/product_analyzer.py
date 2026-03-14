"""
E-Commerce Product Analyzer (Day 13 AM Part A).
Uses Pandas DataFrame with .loc[], .iloc[], filtering, and CSV export.
"""

from pathlib import Path

import pandas as pd


def build_products_df() -> pd.DataFrame:
    """Build a DataFrame with 20+ products: name, category, price, stock, rating, num_reviews."""
    products = [
        {"name": "Laptop Pro", "category": "Electronics", "price": 45000, "stock": 25, "rating": 4.5, "num_reviews": 320},
        {"name": "Wireless Mouse", "category": "Electronics", "price": 899, "stock": 150, "rating": 4.2, "num_reviews": 210},
        {"name": "USB-C Hub", "category": "Electronics", "price": 2499, "stock": 80, "rating": 4.7, "num_reviews": 180},
        {"name": "Mechanical Keyboard", "category": "Electronics", "price": 5500, "stock": 45, "rating": 4.8, "num_reviews": 420},
        {"name": "Monitor 27\"", "category": "Electronics", "price": 18500, "stock": 30, "rating": 4.4, "num_reviews": 95},
        {"name": "Cotton T-Shirt", "category": "Clothing", "price": 599, "stock": 200, "rating": 4.1, "num_reviews": 150},
        {"name": "Denim Jeans", "category": "Clothing", "price": 1899, "stock": 120, "rating": 4.3, "num_reviews": 88},
        {"name": "Winter Jacket", "category": "Clothing", "price": 4500, "stock": 55, "rating": 4.6, "num_reviews": 65},
        {"name": "Running Shoes", "category": "Clothing", "price": 3499, "stock": 70, "rating": 4.5, "num_reviews": 210},
        {"name": "Socks Pack", "category": "Clothing", "price": 349, "stock": 300, "rating": 4.0, "num_reviews": 45},
        {"name": "Python Cookbook", "category": "Books", "price": 699, "stock": 90, "rating": 4.7, "num_reviews": 320},
        {"name": "Data Science Guide", "category": "Books", "price": 899, "stock": 60, "rating": 4.4, "num_reviews": 110},
        {"name": "Clean Code", "category": "Books", "price": 599, "stock": 75, "rating": 4.9, "num_reviews": 550},
        {"name": "Design Patterns", "category": "Books", "price": 749, "stock": 40, "rating": 4.2, "num_reviews": 85},
        {"name": "Algorithms", "category": "Books", "price": 1299, "stock": 35, "rating": 4.6, "num_reviews": 200},
        {"name": "Desk Lamp", "category": "Home", "price": 1299, "stock": 100, "rating": 4.3, "num_reviews": 75},
        {"name": "Coffee Maker", "category": "Home", "price": 3500, "stock": 45, "rating": 4.5, "num_reviews": 130},
        {"name": "Bluetooth Speaker", "category": "Electronics", "price": 2999, "stock": 65, "rating": 4.4, "num_reviews": 95},
        {"name": "Throw Pillow", "category": "Home", "price": 499, "stock": 180, "rating": 4.1, "num_reviews": 42},
        {"name": "Storage Box Set", "category": "Home", "price": 899, "stock": 90, "rating": 4.0, "num_reviews": 38},
        {"name": "Smart Watch", "category": "Electronics", "price": 12500, "stock": 40, "rating": 4.6, "num_reviews": 280},
        {"name": "Headphones", "category": "Electronics", "price": 3999, "stock": 85, "rating": 4.7, "num_reviews": 410},
    ]
    return pd.DataFrame(products)


def run_first_five_minutes_checklist(df: pd.DataFrame) -> None:
    """Run the 'First 5 Minutes' checklist: shape, info(), describe()."""
    print("=== First 5 Minutes Checklist ===\n")
    print("1. Shape:", df.shape)
    print("\n2. df.info():")
    df.info()
    print("\n3. df.describe():")
    print(df.describe())


def main() -> None:
    out_dir = Path(__file__).resolve().parent
    df = build_products_df()

    # --- First 5 Minutes checklist ---
    run_first_five_minutes_checklist(df)

    # --- .loc[] operations ---
    print("\n=== .loc[] (a) All Electronics ===")
    electronics = df.loc[df["category"] == "Electronics"]
    print(electronics)

    print("\n=== .loc[] (b) Rating > 4.0 and price < 5000 ===")
    top_affordable = df.loc[(df["rating"] > 4.0) & (df["price"] < 5000)]
    print(top_affordable)

    # (c) Update stock for a specific product (e.g. first product by name)
    product_name = "Wireless Mouse"
    df.loc[df["name"] == product_name, "stock"] = 200
    print(f"\n=== .loc[] (c) Updated stock for '{product_name}' to 200 ===")
    print(df.loc[df["name"] == product_name, ["name", "stock"]])

    # --- .iloc[] operations ---
    print("\n=== .iloc[] (a) First 5 products ===")
    print(df.iloc[:5])
    print("\n=== .iloc[] (a) Last 5 products ===")
    print(df.iloc[-5:])

    print("\n=== .iloc[] (b) Every other row ===")
    print(df.iloc[::2])

    print("\n=== .iloc[] (c) Rows 10-15, columns 0-3 ===")
    print(df.iloc[10:16, 0:4])

    # --- Filtered DataFrames ---
    budget_products = df.loc[df["price"] < 1000].copy()
    premium_products = df.loc[df["price"] > 10000].copy()
    popular_products = df.loc[(df["num_reviews"] > 100) & (df["rating"] > 4.0)].copy()

    filtered_dfs = {
        "budget_products": budget_products,
        "premium_products": premium_products,
        "popular_products": popular_products,
    }

    # Export each to CSV using a loop
    for name, frame in filtered_dfs.items():
        path = out_dir / f"{name}.csv"
        frame.to_csv(path, index=False)
        print(f"Exported {name}.csv ({len(frame)} rows)")


if __name__ == "__main__":
    main()
