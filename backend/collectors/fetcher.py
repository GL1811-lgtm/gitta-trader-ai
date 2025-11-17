import datetime

try:
    import yfinance as yf
    import pandas as pd
    YFINANCE_INSTALLED = True
except ImportError:
    import random
    # Create a dummy pandas DataFrame class if pandas is not available
    class DataFrame:
        def __init__(self, data, index=None):
            self._data = data
            self.index = index if index is not None else range(len(next(iter(data.values()))))
            self.columns = list(data.keys())
        
        def __len__(self):
            return len(self.index)

        def __str__(self):
            return self.head().__str__()

        @property
        def empty(self):
            return len(self) == 0

        def head(self, n=5):
            header = "\t".join(self.columns)
            lines = [header]
            
            # Get the index name or a default
            index_name = "index"
            if hasattr(self.index, 'name') and self.index.name:
                index_name = self.index.name

            # Determine the number of rows to display
            num_rows_to_display = min(n, len(self))

            # Collect data for display
            rows_data = []
            for i in range(num_rows_to_display):
                row_values = [f"{self._data[col][i]:.2f}" for col in self.columns]
                rows_data.append(f"{self.index[i]}\t" + "\t".join(row_values))
            
            return f"--- Simulated Data ---\n{index_name}\n" + "\n".join(rows_data)

    class pd:
        DataFrame = DataFrame
        def to_datetime(self, dates):
            return dates

    YFINANCE_INSTALLED = False


def fetch_latest(symbol: str):
    """
    Fetches the latest 1-minute OHLCV data for a given symbol.
    If yfinance or pandas are not installed, it returns a simulated DataFrame.
    """
    print(f"Fetching latest data for {symbol}...")
    if YFINANCE_INSTALLED:
        try:
            ticker = yf.Ticker(symbol)
            # Fetch 1-minute data for the last day
            data = ticker.history(period="1d", interval="1m")
            if data.empty:
                print(f"No data returned for {symbol}. Simulating data.")
                return _simulate_data(symbol)
            return data
        except Exception as e:
            print(f"An error occurred with yfinance: {e}. Simulating data.")
            return _simulate_data(symbol)
    else:
        print("yfinance and/or pandas not found. Simulating data.")
        return _simulate_data(symbol)

def _simulate_data(symbol: str):
    """Generates a simulated OHLCV DataFrame."""
    dates = [datetime.datetime.now() - datetime.timedelta(minutes=x) for x in range(10)]
    data = {
        'Open': [random.uniform(100, 200) for _ in range(10)],
        'High': [random.uniform(200, 300) for _ in range(10)],
        'Low': [random.uniform(50, 100) for _ in range(10)],
        'Close': [random.uniform(100, 200) for _ in range(10)],
        'Volume': [random.randint(10000, 50000) for _ in range(10)],
    }
    df = pd.DataFrame(data, index=dates)
    if hasattr(df.index, 'name'):
      df.index.name = 'Datetime'
    return df

if __name__ == '__main__':
    # For direct testing
    nifty_data = fetch_latest('^NSEI')
    print("\nNIFTY Data:")
    print(nifty_data.head())

    banknifty_data = fetch_latest('^NSEBANK')
    print("\nBANKNIFTY Data:")
    print(banknifty_data.head())
