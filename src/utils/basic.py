import yfinance as yf
import pandas as pd

class StockAnalysis:
    def __init__(self, data: pd.DataFrame):
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input must be a Pandas Dataframe")
        self.data = data
        
    def get_sma(self, window: int):
        return self.data['Close'].rolling(window=window).mean()
    
    
        
def from_csv(file_path: str) -> StockAnalysis:
    """Creates a StockAnalysis object from a local CSV file."""
    stock_data = pd.read_csv(file_path, parse_dates=["Date"], index_col="Date")
    return StockAnalysis(stock_data)
        