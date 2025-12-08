import pandas as pd
import yfinance as yf

import numpy as np

nifty = yf.Ticker('COFORGE.NS')

data = nifty.history(period='5d')

data.to_csv('analysis/Time Series/Initial/coforge_5d.csv')