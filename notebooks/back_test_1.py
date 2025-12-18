# Class structure I observed in the Backtesting.py Library

class Strategy:
    def buy(self, func):
        pass

    def sell(self, func):
        pass

class TestBack:

    def __init__(self, strategy: Strategy):
        self.strategy = strategy

from src.screens.single_candle import SingleCandleAnalyser, Candle
sca = SingleCandleAnalyser(r"C:\Users\Atharv Rawat\Desktop\Main\IT\Projects\Trading Track\data\raw\reliance_data.csv")

test = (i for i in range(len(sca.data)))

class Order:
    def __init__(
            self,
            price: float,
            quantity: int,
            position: str,
            date: str,
            is_concluded: bool = False,
            candle_index: int,
            is_profit: bool = None,
            net_change: float = None,
            net_percent: float = None,
            current_cash: float,
    ):



            "date": str,
            "is_concluded": True or False,
            "candle_index": int,
            "is_profit": True or False,
            "net_change": float,
            "net_percent": float,
            "current_cash": float, ]]]

    ):
        self.price = price
        self.quantity = quantity
        if position in ["buy", "sell"]:
            self.position = position
        else:
            raise ValueError('Position can only take string values "buy" and "sell".')

cash = 100000

orders: list[dict[int, dict]] = []
order = []

def buy(price:float, quantity:int):
    global order
    if not order:
        global cash
        total = price * quantity
        cash -= total
        order.append(Order(price, quantity, position="buy"))
        return 1
    return 0

def sell(srn):
    global order
    if order:
        global cash
        order = order[0]
        current = srn.data.loc[i].Close
        cash += srn.data.loc[i].Close
        order.append(Order(price, quantity, position="buy"))
        return 1
    return 0


for i in test:
    if sca.is_bozo(i):
        buy(price=sca.data.loc[i].Close, quantity=1)
        break
    if sca.is_long(i):
        sell(i)
        break


"""
- A list of dictionaries that contains the details for every order.
- Multiple active orders at once.
- List[dict[SrN:int, dict[
                        "position": "buy" or "sell",
                        "date": str,
                        "is_concluded": True or False,
                        "candle_index": int,
                        "is_profit": True or False,
                        "net_change": float,
                        "net_percent": float,
                        "current_cash": float,]]]
"""