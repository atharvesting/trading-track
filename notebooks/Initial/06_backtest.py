import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("data/raw/reliance_data.csv", parse_dates=["Date"], index_col="Date")

# Recreate indicators
df["MA20"] = df["Close"].rolling(20).mean()
df["Signal"] = np.where(df["Close"] > df["MA20"], 1, -1)

# 1. Compute daily returns (percent)
df["Return"] = df["Close"].pct_change()

# 2. Shift the signal forward 1 day to avoid using future info
df["ShiftedSignal"] = df["Signal"].shift(1)

# 3. Strategy return = today's shifted signal * today's return
df["StrategyReturn"] = df["ShiftedSignal"] * df["Return"]

# 4. Convert daily strategy returns into cumulative growth
df["CumulativeStrategy"] = (1 + df["StrategyReturn"]).cumprod()

# 5. Convert daily asset returns into cumulative buy-and-hold growth (benchmark)
df["CumulativeBuyHold"] = (1 + df["Return"]).cumprod()

# 6. Plot both curves
plt.figure(figsize=(12, 6))
df[["CumulativeStrategy", "CumulativeBuyHold"]].plot()
plt.title("Strategy vs Buy & Hold")
plt.show()


