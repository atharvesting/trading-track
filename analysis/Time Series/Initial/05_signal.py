import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(project_root)

from src.utils.basic import StockAnalysis

df = pd.read_csv('data/raw/reliance_data.csv', parse_dates=["Date"], index_col="Date")

test = StockAnalysis(df)

df['MA20'] = test.get_sma(20)

    
df['Signal'] = np.where(df.Close > df.MA20, 1, -1)



'''print(df[["Close", "MA20", "Signal"]].head(25))

df[["Close", "MA20", "Signal"]].plot(figsize=(12, 6))
plt.show()'''

plt.figure(figsize=(12, 4))
df["Signal"].plot()
plt.title("Trading Signal (+1 / -1)")
plt.show()
