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
        self.bids = {}
        self.asks = {}

    def add_order(self, order):
        if order.side == "BUY":
            self.match_buy(order)
            if order.quantity > 0:
                if order.price not in self.bids:
                    self.bids[order.price] = deque()
                self.bids[order.price].append(order)
        else:
            self.match_sell(order)
            if order.quantity > 0:
                if order.price not in self.asks:
                    self.asks[order.price] = deque()
                self.asks[order.price].append(order)

    def match_buy(self, buy):
        while buy.quantity > 0 and self.asks:
            best_price = min(self.asks.keys())

            if buy.price != 0 and buy.price < best_price:
                break

            queue = self.asks[best_price]
            sell = queue[0]

            trade_qty = min(buy.quantity, sell.quantity)

            print(f"TRADE {buy.id} {sell.id} {best_price} {trade_qty}")

            buy.quantity -= trade_qty
            sell.quantity -= trade_qty

            if sell.quantity == 0:
                queue.popleft()

            if not queue:
                del self.asks[best_price]


    def match_sell(self, sell):
        while sell.quantity > 0 and self.bids:
            best_price = max(self.bids.keys())

            if sell.price != 0 and sell.price > best_price:
                break

            queue = self.bids[best_price]
            buy = queue[0]

            trade_qty = min(sell.quantity, buy.quantity)

            trade_price = sell.price if sell.price != 0 else best_price
            print(f"TRADE {buy.id} {sell.id} {trade_price} {trade_qty}")

            sell.quantity -= trade_qty
            buy.quantity -= trade_qty

            if buy.quantity == 0:
                queue.popleft()

            if not queue:
                del self.bids[best_price]

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

        if len(parts) != 4:
            continue

        order_id, side, price, qty = parts

        price = float(price)
        qty = int(qty)

        order = Order(order_id, side, price, qty)

        book.add_order(order)


if __name__ == "__main__":
    main()