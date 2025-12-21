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
        self.upper_shadow = self.h - max(self.c, self.o)
        self.lower_shadow = min(self.c, self.o) - self.l
        self.shadow = self.upper_shadow + self.lower_shadow
        self.body_weight = self.body / self.range if self.range != 0 else 0
        self.is_bullish = self.o < self.c
        self.is_bearish = self.o > self.c
        
    def __repr__(self):
        return f"{self.date}, O - {self.o}, C - {self.c}, H - {self.h}, L - {self.l}"

    def shadow_to_body_ratio(self):
        if self.body == 0:
            return float('inf') # Handle Doji candles
        return self.shadow / self.body

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

    def fetch_data_subset(self, srn:int, lookback:int = 15, columns:list[str] = ['Close']):
        start_idx = max(0, srn - lookback)
        return self.data[columns].iloc[start_idx: srn].values

    @staticmethod
    def convert_to_log_data(data_subset:np.ndarray):
        return np.log(data_subset.squeeze())

    @staticmethod
    def get_trend(data_subset) -> tuple:
        y = np.asarray(data_subset).squeeze()
        n = len(y)
        if n < 2:
            return 0.0, y[0] if n == 1 else 0.0
        X = np.arange(n)
        X_mean = X.mean()
        y_mean = y.mean()
        slope = np.sum((X - X_mean) * (y - y_mean)) / np.sum((X - X_mean)**2)
        intercept = y_mean - slope * X_mean
        r = np.corrcoef(X, y)[0, 1]

        log_returns = np.diff(y)
        sigma = np.std(log_returns, ddof=0)
        trend_strength = slope / sigma if sigma != 0 else 0.0

        return slope, intercept, r, trend_strength

    def get_normal_trend(self, srn:int, lookback:int = 15, columns:list[str] = ['Close']):
        y = self.fetch_data_subset(srn, lookback, columns)
        return self.get_trend(y)

    def get_log_trend(self, srn: int, lookback: int = 15, columns: list[str] = ['Close']):
        y = self.fetch_data_subset(srn, lookback, columns)
        log_y = self.convert_to_log_data(y)
        return self.get_trend(log_y)

    def is_shooting_star(self, srn:int, lookback:int = 15, trend_thresh:float = 0.3):
        m, b, r, trend_strength = self.get_log_trend(srn, lookback)
        optimal_prior_trend = trend_strength > trend_thresh

        c = self.fetch_candle(srn)
        body_size = c.body if c.body > 0 else 0.001
        has_long_upper_shadow = c.upper_shadow >= (2 * body_size)
        has_small_lower_shadow = c.lower_shadow <= body_size
        optimal_shape = c.is_bearish and has_long_upper_shadow and has_small_lower_shadow

        return optimal_prior_trend and optimal_shape