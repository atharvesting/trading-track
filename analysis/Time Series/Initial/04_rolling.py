import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

symbol = 'COFORGE.NS'
coforge = yf.Ticker(symbol)

data = coforge.history(period="3mo")

data['SMA10'] = data['Close'].rolling(window=10).mean()
data['SMA20'] = data['Close'].rolling(window=20).mean()

plt.plot(data.index, data.Close)
plt.plot(data.index, data.SMA10)
plt.plot(data.index, data.SMA20)

plt.show()