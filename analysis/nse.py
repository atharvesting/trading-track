from nsetools import Nse
import yfinance as yf
import pandas as pd
import numpy as np
from screens import StockAnalysis

ns = Nse()

stock_codes = ns.get_stock_codes()
stock_codes = stock_codes[:100]

def get_stock(stock_code: str):
    stock_id = stock_code + '.NS'
    st = yf.Ticker(stock_id)
    data = pd.DataFrame(st.history(period="20d"))
    ans = StockAnalysis(data)
    sma = ans.get_sma(7)
    result = np.where(data.Close > sma, 1, -1)
    if sum(result[-5:]) == 5:
        print(result)
        return stock_id
    return
        
for stock in stock_codes:
    good_list = []
    result = get_stock(stock)
    if result:
        print(stock)
        # good_list.append(result)