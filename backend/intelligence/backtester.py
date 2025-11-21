import pandas as pd
import numpy as np
from backend.data_providers.manager import DataProviderManager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BacktestEngine:
    def __init__(self):
        self.data_provider = DataProviderManager()

    def run_backtest(self, symbol, strategy="SMA_CROSSOVER", period="1y", initial_capital=100000, strategy_params=None):
        """
        Runs a backtest for a given symbol and strategy.
        """
        logger.info(f"Starting backtest for {symbol} with strategy {strategy} over {period}")
        
        # 1. Fetch Data
        df = self.data_provider.get_historical_data(symbol, period=period, interval="1d")
        if df is None or df.empty:
            return {"error": "No historical data found"}

        # Ensure we have Close price
        if 'Close' not in df.columns:
             return {"error": "Data missing 'Close' column"}

        # 2. Apply Strategy Logic
        df = self._apply_strategy(df, strategy, strategy_params)
        
        # 3. Simulate Trades
        results = self._simulate_trades(df, initial_capital)
        
        return results

    def _apply_strategy(self, df, strategy, params=None):
        """
        Calculates indicators and generates signals (1=Buy, -1=Sell, 0=Hold).
        """
        df = df.copy()
        df['Signal'] = 0
        
        # Default parameters if none provided
        if params is None:
            params = {}

        if strategy == "SMA_CROSSOVER":
            # Simple Moving Average Crossover (Golden Cross)
            fast = params.get('ma_fast', 50)
            slow = params.get('ma_slow', 200)
            
            df['SMA_Fast'] = df['Close'].rolling(window=fast).mean()
            df['SMA_Slow'] = df['Close'].rolling(window=slow).mean()
            
            # Buy when Fast crosses above Slow
            df.loc[df['SMA_Fast'] > df['SMA_Slow'], 'Signal'] = 1
            # Sell when Fast crosses below Slow
            df.loc[df['SMA_Fast'] < df['SMA_Slow'], 'Signal'] = -1
            
        elif strategy == "RSI_STRATEGY":
            # Simple RSI Strategy
            period = params.get('rsi_period', 14)
            overbought = params.get('rsi_overbought', 70)
            oversold = params.get('rsi_oversold', 30)
            
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
            
            df.loc[df['RSI'] < oversold, 'Signal'] = 1 # Oversold -> Buy
            df.loc[df['RSI'] > overbought, 'Signal'] = -1 # Overbought -> Sell

        elif strategy == "EVOLUTION_DNA":
            # Logic based on Organism DNA
            # We can combine multiple indicators based on DNA
            
            # 1. RSI Component
            rsi_period = params.get('rsi_period', 14)
            rsi_ob = params.get('rsi_overbought', 70)
            rsi_os = params.get('rsi_oversold', 30)
            
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
            
            # 2. MA Component
            ma_fast_period = params.get('ma_fast', 20)
            ma_slow_period = params.get('ma_slow', 50)
            
            df['MA_Fast'] = df['Close'].rolling(window=ma_fast_period).mean()
            df['MA_Slow'] = df['Close'].rolling(window=ma_slow_period).mean()
            
            # Combined Logic (Simple AND condition for now)
            # Buy: RSI < Oversold AND Price > MA_Slow (Trend filter)
            buy_condition = (df['RSI'] < rsi_os) & (df['Close'] > df['MA_Slow'])
            
            # Sell: RSI > Overbought OR Price < MA_Slow (Trend break)
            sell_condition = (df['RSI'] > rsi_ob) | (df['Close'] < df['MA_Slow'])
            
            df.loc[buy_condition, 'Signal'] = 1
            df.loc[sell_condition, 'Signal'] = -1

        return df

    def _simulate_trades(self, df, initial_capital):
        """
        Iterates through signals to execute trades and calculate equity.
        """
        cash = initial_capital
        position = 0 # Quantity
        equity_curve = []
        trades = []
        
        for i in range(len(df)):
            price = df['Close'].iloc[i]
            signal = df['Signal'].iloc[i]
            date = df.index[i]
            
            # Execute Trade
            if signal == 1 and position == 0: # Buy
                position = cash // price
                cost = position * price
                cash -= cost
                trades.append({
                    "type": "BUY",
                    "date": str(date),
                    "price": price,
                    "quantity": position,
                    "value": cost
                })
            elif signal == -1 and position > 0: # Sell
                revenue = position * price
                cash += revenue
                trades.append({
                    "type": "SELL",
                    "date": str(date),
                    "price": price,
                    "quantity": position,
                    "value": revenue,
                    "pnl": revenue - trades[-1]['value']
                })
                position = 0
            
            # Calculate Daily Equity
            current_equity = cash + (position * price)
            equity_curve.append(current_equity)

        # Metrics
        final_equity = equity_curve[-1]
        total_return = ((final_equity - initial_capital) / initial_capital) * 100
        
        # Calculate Max Drawdown
        equity_series = pd.Series(equity_curve)
        rolling_max = equity_series.cummax()
        drawdown = (equity_series - rolling_max) / rolling_max
        max_drawdown = drawdown.min() * 100

        # Calculate Advanced Metrics
        returns = equity_series.pct_change().dropna()
        
        # Sharpe Ratio (Annualized)
        if returns.std() > 0:
            sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252)
        else:
            sharpe_ratio = 0.0
            
        # Sortino Ratio (Annualized)
        downside_returns = returns[returns < 0]
        if len(downside_returns) > 0 and downside_returns.std() > 0:
            sortino_ratio = (returns.mean() / downside_returns.std()) * np.sqrt(252)
        else:
            sortino_ratio = 0.0
            
        # Win Rate
        winning_trades = [t for t in trades if t.get('pnl', 0) > 0]
        win_rate = (len(winning_trades) / len(trades) * 100) if len(trades) > 0 else 0.0

        return {
            "initial_capital": initial_capital,
            "final_equity": round(final_equity, 2),
            "total_return_pct": round(total_return, 2),
            "max_drawdown_pct": round(max_drawdown, 2),
            "sharpe_ratio": round(sharpe_ratio, 2),
            "sortino_ratio": round(sortino_ratio, 2),
            "win_rate": round(win_rate, 2),
            "total_trades": len(trades),
            "trades": trades[-50:] # Return last 50 trades to avoid huge payload
        }
