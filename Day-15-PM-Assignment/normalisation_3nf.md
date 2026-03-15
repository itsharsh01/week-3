# Day 15 PM Part A — Normalise OrderFacts to 3NF

## Step 1: 1NF (atomic values, no repeating groups)

- Each cell has a single value; each row is unique. **Repeating groups:** (item_id, item_name, quantity, unit_price) can repeat per order → one row per order-item.
- **1NF:** One row per (order_id, item_id) combination. So we already have one line per order-item. Add a key: (order_id, item_id) or surrogate order_item_id.

**1NF tables:** OrderFacts with columns order_id, customer_id, customer_name, customer_phone, restaurant_id, restaurant_name, item_id, item_name, quantity, unit_price, order_date. Key: (order_id, item_id).

## Step 2: 2NF (no partial dependency; all non-keys depend on full key)

- Full key: (order_id, item_id). 
- **Partial dependencies:** customer_id, customer_name, customer_phone depend only on order_id (partial key). restaurant_id, restaurant_name depend only on order_id. order_date depends only on order_id. item_name, unit_price might depend on item_id only (if same item same price everywhere).
- **Decompose:** 
  - **Orders(order_id, customer_id, restaurant_id, order_date)** — full key order_id.
  - **Customers(customer_id, customer_name, customer_phone)** — key customer_id.
  - **Restaurants(restaurant_id, restaurant_name)** — key restaurant_id.
  - **Items(item_id, item_name, unit_price, restaurant_id)** — key item_id (if item is per restaurant) or (item_id, restaurant_id).
  - **OrderItems(order_id, item_id, quantity)** — key (order_id, item_id).

So 2NF: Orders, Customers, Restaurants, Items, OrderItems.

## Step 3: 3NF (no transitive dependency; non-keys depend only on key)

- **Customers:** customer_id → customer_name, customer_phone. No transitive dependency. ✓
- **Restaurants:** restaurant_id → restaurant_name. ✓
- **Items:** item_id → item_name, unit_price; if we have restaurant_id in Items, item_name/unit_price might depend on (restaurant_id, item_id). So Items( item_id, restaurant_id, item_name, unit_price ) with key (item_id, restaurant_id) or item_id if globally unique.
- **Orders:** order_id → customer_id, restaurant_id, order_date. No transitive dependency. ✓
- **OrderItems:** (order_id, item_id) → quantity. ✓

**3NF schema:**
- Customer(customer_id, customer_name, customer_phone)
- Restaurant(restaurant_id, restaurant_name)
- Item(item_id, restaurant_id, item_name, unit_price)  — key (item_id, restaurant_id)
- Order(order_id, customer_id, restaurant_id, order_date)
- OrderItem(order_id, item_id, quantity)

All steps shown; no partial or transitive dependencies remain.
