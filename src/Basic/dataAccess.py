import yfinance as yf
import matplotlib.pyplot as plt

ticker_symbol = "COFORGE.NS"
coforge = yf.Ticker(ticker_symbol)

data = coforge.history(period="5y")

total = data['Close'].sum(axis=0)

data['MA200'] = data['Close'].rolling(window=200).mean()
data['MA30'] = data['Close'].rolling(window=30).mean()


plt.plot(data.index, data.Close, label='Close Price')
plt.plot(data.index, data['MA200'], label='200DMA')
plt.plot(data.index, data['MA30'], label='30DMA')

plt.legend()
plt.show()