import pandas as pd
from src.screens.single_candle import SingleCandleAnalyser, Candle

a = SingleCandleAnalyser(r"C:\Users\Atharv Rawat\Desktop\Main\IT\Projects\Trading Track\data\raw\reliance_data.csv")

l = a.get_last_n_candles(20, 10)

for i in range(1, 100):
    print(i, a.is_bozo(i, 0.85, 1.5))



# for i in range(10):
#     c = a.data.loc[i]
#     print(Candle(c))



