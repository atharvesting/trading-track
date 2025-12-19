from src.screens.single_candle import SingleCandleAnalyser, Candle
import pandas as pd
sca = SingleCandleAnalyser(r"C:\Users\Atharv Rawat\Desktop\Main\IT\Projects\Trading Track\data\raw\reliance_data.csv")
from time import sleep

class Order:
    def __init__(
            self,
            price: float,
            quantity: int,
            position: str,
            date: str,
            current_cash: float,
            candle_index: int,
            is_concluded: bool = False,
            is_profit: bool = None,
            net_change: float = None,
            net_percent: float = None,
            exit_price: float = None,
            series: pd.Series = None,
    ):
        self.price = price
        self.quantity = quantity
        self.position = position
        self.date = date
        self.current_cash = current_cash
        self.candle_index = candle_index
        self.is_concluded = is_concluded
        self.is_profit = is_profit
        self.net_change = net_change
        self.net_percent = net_percent
        self.exit_price = exit_price
        self.series = series

    def return_order_dict(self):
        return {
            'price': self.price,
            'quantity': self.quantity,
            'position': self.position,
            'date': self.date,
            'current_cash': self.current_cash,
            'candle_index': self.candle_index,
            'is_concluded': self.is_concluded,
            'is_profit': self.is_profit,
            'net_change': self.net_change,
            'net_percent': self.net_percent,
            'exit_price': self.exit_price
        }

    def __repr__(self):
        return (
            f"Order(price={self.price}, quantity={self.quantity}, "
            f"position='{self.position}', date='{self.date}', "
            f"current_cash={self.current_cash}, candle_index={self.candle_index}, "
            f"is_concluded={self.is_concluded}, is_profit={self.is_profit}, "
            f"net_change={self.net_change}, net_percent={self.net_percent}, "
            f"exit_price={self.exit_price})"
        )

def buy(srn:int, price:float, quantity:int):
    global order

    if not order:
        global cash, orders
        s = sca.data.loc[srn]
        total = price * quantity
        cash -= total
        o = Order(
                candle_index=srn, price = price, quantity = quantity,
                position = "buy", date=s.Date, series=s,
                current_cash=cash, is_concluded=False, is_profit=None,
                net_change=None, net_percent=None
            )
        order.append(o)
        return o
    return 0


def sell(srn):
    global order
    if order:
        global cash, orders
        buy_order = order[0]
        s = sca.data.loc[srn]
        cash += s.Close
        change = buy_order.quantity * (s.Close - buy_order.price)
        o = Order(
            candle_index=srn, price=s.Close, quantity=buy_order.quantity,
            position="sell", date=s.Date, series=s,
            current_cash=cash, is_concluded=True, is_profit=change > 0,
            net_change=change, net_percent=change * 100 / buy_order.price * buy_order.quantity
        )
        orders.append((buy_order, o))
        order.clear()
        return o
    return 0


# Setup globals
cash = 10000
orders: list[tuple[Order, Order]] = []
order: list[Order] = []

# Test with multiple candles
test_indices = range(1, 1000)
for i in test_indices:
    print(f"\n--- Candle {i} --- Cash: {cash}, Open orders: {len(order)}")

    # Test buy condition
    if sca.is_bozo(i):
        result = buy(i, price=sca.data.loc[i].Close, quantity=1)
        print(f"Buy result: {result}")
        if result != 0:
            print(f"Created: {result}")

    # Test sell condition (only if we have open position)
    elif sca.is_long(i) and order:
        result = sell(i)
        print(f"Sell result: {result}")
        if result != 0:
            print(f"Closed: {result}, Total trades: {len(orders)}")

    # Show current state
    if order:
        print(f"Open position: {order[0]}")

"""
- A list of dictionaries that contains the details for every order.
- Multiple active orders at once.c
"""