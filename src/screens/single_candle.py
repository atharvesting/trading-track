import pandas as pd
import numpy as np
# from sklearn.linear_model import LinearRegression
# from statsmodels.tsa.deterministic import DeterministicProcess

class Candle:
    def __init__(self, row_data: pd.Series):
        self.date = row_data.Date
        self.index = row_data.index
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
    def __init__(self, file_path: str):
        self.data = pd.read_csv(file_path)
        self.default_lookback:int = 10
        self.default_proportion:float = 0.9
        self.default_multiplier:float = 2

    def index_from_date(self, date) -> int:
        return self.data[self.data.Date == date].index[0]

    def date_from_index(self, srn:int) -> str:
        return self.data.loc[srn].Date
        
    def fetch_candle(self, srn) -> Candle:
        return Candle(self.data.loc[srn])

    def get_last_n_candles(self, srn, lookback:int = None) -> list[Candle]:
        lookback = self.default_lookback if lookback is None else lookback
        candles = list(map(
            lambda serial: self.fetch_candle(serial),
            list(range(max(srn - lookback, 0), srn))
        ))
        return candles
        
    def get_avg_body(self, srn, lookback:int = None) -> float:
        lookback = self.default_lookback if lookback is None else lookback
        previous_candles = self.get_last_n_candles(srn, lookback)
        avg = [c.body for c in previous_candles]
        return sum(avg) / len(avg)
    
    def is_long(self, srn:int, multiplier:float = None, lookback:int = None) -> bool:
        lookback = self.default_lookback if lookback is None else lookback
        multiplier = self.default_multiplier if multiplier is None else multiplier
        c = self.fetch_candle(srn)
        avg_body = self.get_avg_body(srn, lookback)
        return c.body > multiplier * avg_body

    def is_bozo(self, srn:int, proportion:float = None, multiplier:float = None, lookback:int = None) -> bool:
        lookback = self.default_lookback if lookback is None else lookback
        multiplier = self.default_multiplier if multiplier is None else multiplier
        proportion = self.default_proportion if proportion is None else proportion
        c = self.fetch_candle(srn)
        return self.is_long(srn, multiplier, lookback) and c.body_weight > proportion

    def get_sma(self, period:int = 15):
        return self.data.Close.rolling(window=period).mean()

    def get_xma(self, period:int = 15):
        return self.data.Close.ewm(span=period, adjust=False).mean()

    def get_trend(self, srn:int, lookback:int = 15, period:int = 15) -> tuple:
        start_idx = max(0, srn - lookback)
        y = self.data['Close'].iloc[start_idx: srn + 1].values  # Converts series to NumPy series
        n = len(y)
        if n < 2:
            return 0.0, y[0] if n == 1 else 0.0
        X = np.arange(n)
        slope, intercept = np.polyfit(X, y, 1)
        return slope, intercept