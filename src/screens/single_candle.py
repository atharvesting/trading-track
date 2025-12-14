import pandas as pd
import numpy as np

class Candle:
    def __init__(self, row_data: pd.Series):
        self.date = row_data.Date
        self.o = row_data.Open
        self.c = row_data.Close
        self.h = row_data.High
        self.l = row_data.Low
        self.v = row_data.Volume
        self.body = abs(self.c - self.o)
        self.range = abs(self.h - self.l)
        self.body_weight = self.body / self.range
        self.is_bullish = self.o < self.c
        self.is_bearish = self.o > self.c
        
    def __repr__(self):
        return f"{self.date}, O - {self.o}, C - {self.c}, H - {self.h}, L - {self.l}"


class SingleCandleAnalyser:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        
    def fetch_candle(self, index):
        return self.data[index]
        
    def is_long(self, index, multiplier=2.0, lookback=10) -> bool:
        candle = self.fetch_candle(index)
        avg_body = get_avg_body(data, self, lookback)
        return candle.body > multiplier * avg_body
    
    def is_bozo(self, proportion: float, multiplier, lookback) -> bool:
        # try:
        #     if 0 < proportion < 1:
        #         pass
        # except:
        #     raise ValueError("Proportion must be between 0 and 1")
        return self.is_long(multiplier, lookback) and self.body_weight > proportion

    def get_last_n_candles(data: pd.DataFrame, candle: Candle, range: int):
        index = index_from_date(data, candle.date)  # Fixed: pass data first, then date
        start = max(0, index - range)
        return data.loc[start:index]
        
    def get_avg_body(data: pd.DataFrame, candle: Candle, lookback: int) -> float:
        previous_candles = get_last_n_candles(data, candle, lookback)
        return abs(previous_candles.Close - previous_candles.Open).mean()

    def index_from_date(data: pd.DataFrame, date) -> int:  # Fixed: swapped parameters and return int
        return data[data.Date == date].index[0]