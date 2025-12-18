from backtesting import Backtest
from backtesting import Strategy
import pandas as pd

class StockPlot:
    
    class NoTradeStrategy(Strategy):
        def init(self):
            pass
        def next(self):
            pass
    
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def plot(self):
        bt = Backtest(self.data, self.NoTradeStrategy, cash=10000000)
        stats = bt.run()
        bt.plot()
        
data = pd.read_csv(r"C:\Users\Atharv Rawat\Desktop\Main\IT\Projects\Trading Track\data\raw\reliance_data.csv")
plot = StockPlot(data)

plot.plot()
