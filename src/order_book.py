from collections import deque
import sys


class Order:
    def __init__(self, order_id, side, price, quantity):
        self.id = order_id
        self.side = side
        self.price = price
        self.quantity = quantity


class OrderBook:

    def __init__(self):
        # price -> queue of orders
        self.bids = {}
        self.asks = {}

    def add_order(self, order):
        if order.side == "BUY":
            if order.price not in self.bids:
                self.bids[order.price] = deque()
            self.bids[order.price].append(order)
        else:
            if order.price not in self.asks:
                self.asks[order.price] = deque()
            self.asks[order.price].append(order)

    def cancel_order(self, order_id):
        print(f"CANCEL request for {order_id}")


def main():

    book = OrderBook()

    for line in sys.stdin:

        parts = line.strip().split()

        if not parts:
            continue

        if parts[0] == "CANCEL":
            if len(parts) >= 2:
                book.cancel_order(parts[1])
            continue

        # ensure a valid order format: ORDER_ID SIDE PRICE QUANTITY
        if len(parts) != 4:
            # ignore malformed input lines
            continue

        order_id, side, price, qty = parts

        price = float(price)
        qty = int(qty)

        order = Order(order_id, side, price, qty)

        book.add_order(order)


if __name__ == "__main__":
    main()