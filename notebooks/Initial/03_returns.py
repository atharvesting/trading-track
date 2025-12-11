import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('analysis/Time Series/Initial/coforge_5d.csv')

price = data.Close
data['Returns'] = price.pct_change() * 100

print(data)

fig, ax = plt.subplots(2)

ax[0].plot(data.index, data.Close)
ax[1].scatter(data.index, data.Returns)

plt.show()