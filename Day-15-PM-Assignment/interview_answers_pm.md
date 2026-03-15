# Day 15 PM Part C — Interview Ready

## Q1 — Update anomalies in a denormalised database (e-commerce example)

**Insertion anomaly:** We cannot record a new product category until we have at least one product in that category if the table is (product_id, product_name, category_name, ...) and category is embedded. So “Electronics” as a category cannot exist without a product.

**Update anomaly:** If we store (order_id, customer_name, customer_phone) and the customer changes their phone number, we must update every order row for that customer. If we miss one, the same customer has different phone numbers in different rows — inconsistency.

**Deletion anomaly:** If we delete the last order that referenced a product, we might lose the product’s name/price if the table is (order_id, product_id, product_name, quantity). So deleting an order can accidentally delete product information.

**Concrete e-commerce:** One table OrderFacts(order_id, customer_name, product_name, category, quantity). Updating a product’s category requires updating every row that contains that product; deleting the last order for a product removes the product from the database.

---

## Q2 — Schema: current price + price history, 3NF

- **Product(product_id, name, current_price, updated_at)** — current price and last-updated time.
- **PriceHistory(product_id, effective_from, effective_to, price)** — key (product_id, effective_from). Each row is a period during which the product had that price. For the current price we can have effective_to = NULL or a sentinel.

**3NF:** product_id → name (in Product); (product_id, effective_from) → price, effective_to (in PriceHistory). No transitive dependency: price depends on the full key. Product and PriceHistory are in 3NF.

**Alternative:** Product(product_id, name), Price(product_id, effective_from, effective_to, price) with the same key. Current price = row where effective_to IS NULL.

---

## Q3 — ACID and double-booking (last hotel room)

**Property at risk:** **Isolation.** Two transactions both read “1 room left,” both decide to book, both write “room booked.” Without isolation we get double-booking.

**How the database prevents it:** Use **locking** or **serialisable isolation**. For example:
- **Row-level lock:** When transaction A reads the row for that room (or the “rooms left” counter), it takes a lock. Transaction B blocks until A commits or aborts. So only one transaction can book the last room.
- **Optimistic concurrency:** Both read the same “version”; on update, the second writer detects a conflict (e.g. row version changed) and aborts/retries.
- **Serialisable isolation:** The scheduler ensures the two transactions behave as if one ran completely before the other, so only one booking succeeds.

So the database enforces isolation (and consistency) so that the “last room” is not booked twice.
