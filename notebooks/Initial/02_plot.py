import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('coforge_5d_15m.csv', index_col=0, parse_dates=['Datetime'])

plt.plot(df.index, df.Close)
plt.scatter(df.index, df.Close)
plt.show()

