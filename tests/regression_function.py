from src.screens.single_candle import Candle, SingleCandleAnalyser

sca = SingleCandleAnalyser(r"C:\Users\Atharv Rawat\Desktop\Main\IT\Projects\Trading Track\data\raw\reliance_data.csv")

print(sca.get_trend(50, 15))