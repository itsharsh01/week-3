"""Generate eda_assignment_data.csv — 1200 rows, 10 mixed-type columns (LMS has real file)."""
import csv
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent / "eda_assignment_data.csv"
random.seed(42)

categories = ["Electronics", "Clothing", "Food", "Home", "Sports"]
regions = ["North", "South", "East", "West"]
rows = []
for i in range(1200):
    cat = random.choice(categories)
    rows.append({
        "id": i + 1,
        "sales": round(random.gammavariate(2, 50), 2),
        "quantity": random.randint(1, 20),
        "price": round(random.uniform(10, 500), 2),
        "rating": round(random.uniform(1, 5), 1),
        "category": cat,
        "region": random.choice(regions),
        "customer_age": random.randint(18, 70),
        "discount_pct": round(random.uniform(0, 30), 1),
        "year": random.choice([2022, 2023, 2024]),
    })

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
print("Wrote", OUT)
