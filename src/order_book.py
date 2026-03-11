from collections import deque
import sys

# ========================
# Order Data Structure
# ========================

class Order:
    def __init__(self, order_id, side, price, quantity):
        self.id = order_id
        self.side = side
        self.price = price
        self.quantity = quantity


# ========================
# Order Book Engine
# ========================

class OrderBook:

    def __init__(self):
        self.bids = {}
        self.asks = {}
        self.order_lookup = {}

    def add_order(self, order):
        if order.side == "BUY":
            self.match_buy(order)
            if order.quantity > 0:
                if order.price not in self.bids:
                    self.bids[order.price] = deque()
                self.bids[order.price].append(order)
                self.order_lookup[order.id] = ("BUY", order.price, order)
        else:
            self.match_sell(order)
            if order.quantity > 0:
                if order.price not in self.asks:
                    self.asks[order.price] = deque()
                self.asks[order.price].append(order)
                self.order_lookup[order.id] = ("SELL", order.price, order)

    def match_buy(self, buy):
        while buy.quantity > 0 and self.asks:
            best_price = min(self.asks.keys())

            if buy.price != 0 and buy.price < best_price:
                break

            queue = self.asks[best_price]
            sell = queue[0]

            # Self-trade prevention
            if buy.id == sell.id:
                break

            trade_qty = min(buy.quantity, sell.quantity)

            print(f"TRADE {buy.id} {sell.id} {best_price} {trade_qty}")

            buy.quantity -= trade_qty
            sell.quantity -= trade_qty

            if sell.quantity == 0:
                queue.popleft()
                if sell.id in self.order_lookup:
                    del self.order_lookup[sell.id]

            if not queue:
                del self.asks[best_price]


    def match_sell(self, sell):
        while sell.quantity > 0 and self.bids:
            best_price = max(self.bids.keys())

            if sell.price != 0 and sell.price > best_price:
                break

            queue = self.bids[best_price]
            buy = queue[0]

            # Self-trade prevention
            if sell.id == buy.id:
                break

            trade_qty = min(sell.quantity, buy.quantity)

            trade_price = sell.price if sell.price != 0 else best_price
            print(f"TRADE {buy.id} {sell.id} {trade_price} {trade_qty}")

            sell.quantity -= trade_qty
            buy.quantity -= trade_qty

            if buy.quantity == 0:
                queue.popleft()
                if buy.id in self.order_lookup:
                    del self.order_lookup[buy.id]

            if not queue:
                del self.bids[best_price]

    def cancel_order(self, order_id):
        if order_id not in self.order_lookup:
            return

        side, price, order = self.order_lookup[order_id]

        book = self.bids if side == "BUY" else self.asks

        if price in book:
            queue = book[price]

            for i, o in enumerate(queue):
                if o.id == order_id:
                    del queue[i]
                    break

            if not queue:
                del book[price]

        del self.order_lookup[order_id]

    def print_book(self):
        print("--- Book ---")


        ask_prices = sorted(self.asks.keys())[:5]
        if not ask_prices:
            print("ASK: (empty)")
        else:
            for price in ask_prices:
                total_qty = sum(order.quantity for order in self.asks[price])
                if total_qty > 0:
                    print(f"ASK: {price:.2f} x {total_qty}")

        bid_prices = sorted(self.bids.keys(), reverse=True)[:5]
        if not bid_prices:
            print("BID: (empty)")
        else:
            for price in bid_prices:
                total_qty = sum(order.quantity for order in self.bids[price])
                if total_qty > 0:
                    print(f"BID: {price:.2f} x {total_qty}")


# ========================
# Program Entry Point
# ========================

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

    book.print_book()


if __name__ == "__main__":
    main()