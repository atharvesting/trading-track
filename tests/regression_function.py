from src.screens.single_candle import Candle, SingleCandleAnalyser

sca = SingleCandleAnalyser(r"C:\Users\Atharv Rawat\Desktop\Main\IT\Projects\Trading Track\data\raw\reliance_data.csv")


for i in range(200, len(sca.data)):
    if sca.is_shooting_star(i):
        print(i, sca.fetch_candle(i))