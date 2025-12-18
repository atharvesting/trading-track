import pandas as pd
import yfinance as yf

import numpy as np

nifty = yf.Ticker('COFORGE.NS')

data = nifty.history(period='5d', interval = '15m')

data.to_csv('coforge_5d_15m.csv')