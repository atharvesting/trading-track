import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('analysis/Time Series/Initial/coforge_5d.csv')

plt.plot(df.index, df.Close)
plt.scatter(df.index, df.Close)

plt.show()