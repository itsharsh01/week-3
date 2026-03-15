# Day 15 PM Part A — Relational Algebra (5 queries)

Using schema: Customer(C_id, name, phone), Restaurant(R_id, name), Order(O_id, C_id, R_id, order_date), OrderItem(O_id, item_id, qty), Item(item_id, R_id, name, unit_price).

**Notation:** σ = selection, π = projection, ⋈ = natural join (or join on specified attrs), ∪ = union, − = set difference.

---

1. **All orders placed by customer with name 'Alice'**
   - π_O_id, C_id, R_id, order_date ( σ_name='Alice'(Customer) ⋈ Order )
   - Or: π_Order.* ( Order ⋈ σ_name='Alice'(Customer) )

2. **Restaurant names that have at least one order**
   - π_restaurant_name ( Restaurant ⋈ π_R_id(Order) )
   - Or: π_name ( Restaurant ⋈ Order )  (after restricting Order to R_id)

3. **Order IDs and total quantity per order**
   - Need aggregation: in RA we use group-by style. G_sum(qty)_by_O_id(OrderItem) then π_O_id, total_qty. (Standard RA extension: group by O_id, sum(qty).)
   - Without agg: we can express “order and its total” as a relation built from OrderItem: e.g. T := OrderItem; then group-by O_id, sum(qty). Notation: τ_O_id sum(qty)→total (OrderItem) then π_O_id, total.

4. **Customers who have never placed an order**
   - π_C_id(Customer) − π_C_id(Order)
   - All customer IDs minus those that appear in Order.

5. **Orders that contain item named 'Plain Dosa'**
   - π_O_id ( OrderItem ⋈ σ_item_name='Plain Dosa'(Item) )
   - Join OrderItem with Item on item_id, select item name, project order ID.

---

## Pandas-to-relational-algebra mapping (3 operations)

| Pandas | Relational algebra |
|--------|--------------------|
| `df.merge(df2, on='key')` | ⋈ (natural join on key) or ⋈_condition (theta-join) |
| `df.groupby('A').agg({'B':'sum'})` | Group-by A, aggregate sum(B); then π_A, sum_B |
| `df[df['x'] > 5]` | σ_x>5 (R) |

- **merge:** Join. `pd.merge(orders, customers, on='customer_id')` ≈ π(Orders ⋈ Customers) (with projection on chosen columns).
- **groupby + agg:** Group and aggregate. `df.groupby('order_id')['quantity'].sum()` ≈ G_order_id sum(quantity)(OrderItem).
- **filter:** Selection. `df[df['status'] == 'delivered']` ≈ σ_status='delivered'(Order).
