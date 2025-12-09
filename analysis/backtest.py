from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import talib

import yfinance as yf
import pandas as pd

# ticker = 'RELIANCE.NS'

# rel = yf.Ticker(ticker)

# data = rel.history(start='2020-01-01', end='2025-12-01')
# data.to_csv('src/Basic/data/reliance_data.csv')  # Save for reuse

data = pd.read_csv('analysis/reliance_data.csv')

class SmaCross(Strategy):
    def init(self):
        self.sma1 = self.I(talib.SMA, self.data.Close, 20)
        self.sma2 = self.I(talib.SMA, self.data.Close, 50)
        self.tracker = 0
        
    def next(self):
        if crossover(self.sma2, self.sma1):
            self.buy(size=10)
            self.tracker = self.data.Close[-1]
            
        elif crossover(self.sma1, self.sma2):
            self.position.close()
            
        if self.position and self.tracker * 0.95 > self.data.Close[-1]:
            self.position.close()

bt = Backtest(data, SmaCross, cash=10000, commission=.002)
stats = bt.run()

print(stats)
bt.plot()
