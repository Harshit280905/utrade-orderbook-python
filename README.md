# utrade-orderbook-python
# In-Memory Order Book Engine

## Overview
This project implements a simplified **in-memory limit order book** that processes buy and sell orders and matches them in real time using **price-time priority**.

The engine reads orders from `stdin`, executes trades when prices cross, supports cancelling orders, and prints the final order book state.

Supported order types:

- **LIMIT orders** – normal buy/sell orders with a price
- **MARKET orders** – represented by `price = 0`
- **CANCEL orders** – remove an existing resting order

---

## Design

### Order Book Structure

The order book maintains two sides:

```
BIDS (buy orders)  → highest price first
ASKS (sell orders) → lowest price first
```

Each price level contains a **FIFO queue** of orders to preserve **time priority**.

### Data Structures Used

| Structure | Purpose |
|---|---|
| `dict price -> deque` | Maintain FIFO queue for orders at each price level |
| `deque` | Efficient push/pop operations for price-time priority |
| `order_lookup` dictionary | O(1) lookup for cancelling orders |

---

## Matching Logic

When a new order arrives:

### BUY order
Matches against the **lowest ASK price**.

### SELL order
Matches against the **highest BID price**.

Trades execute while:

```
BUY price >= SELL price
```

Matching follows **price-time priority**:

1. Best price first
2. Earliest order first

---

## Edge Cases Handled

- Partial fills
- Market orders (`price = 0`)
- Cancel orders
- Self-trade prevention
- Empty order book
- Aggregated quantities per price level

---

## Input Format

```
ORDER_ID SIDE PRICE QUANTITY
```

Example:

```
O1 BUY 100.50 10
O2 SELL 99.00 5
```

Cancel command:

```
CANCEL ORDER_ID
```

Example:

```
CANCEL O2
```

---

## Trade Output Format

```
TRADE BUY_ORDER SELL_ORDER PRICE QUANTITY
```

Example:

```
TRADE O1 O3 100.50 8
```

---

## Final Order Book

After all input is processed the engine prints the top 5 price levels:

```
--- Book ---
ASK: price x quantity
BID: price x quantity
```

Example:

```
--- Book ---
ASK: 99.00 x 13
BID: (empty)
```

---

## How to Run

Run the program with input redirected from a file:

```
python3 src/order_book.py < input.txt
```

Example input file:

```
O1 BUY 100.50 10
O2 BUY 100.50 5
O3 SELL 100.50 8
O4 SELL 99.00 20
```

---

## Complexity

| Operation | Complexity |
|---|---|
| Add order | O(log n) price lookup |
| Match order | O(k) where k = number of matched orders |
| Cancel order | O(1) lookup + O(n) queue scan |

---

## Notes

This implementation focuses on clarity and correctness for a single-instrument order book engine suitable for a coding assignment.