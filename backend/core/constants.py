"""
Global Constants for Gitta Trader AI V2.0
"""

# System Modes
MODE_PAPER = "paper"
MODE_LIVE = "live"
MODE_BACKTEST = "backtest"

# Timeframes
TIMEFRAME_1M = "1m"
TIMEFRAME_5M = "5m"
TIMEFRAME_15M = "15m"
TIMEFRAME_1H = "1h"
TIMEFRAME_1D = "1d"

# Order Types
ORDER_MARKET = "MARKET"
ORDER_LIMIT = "LIMIT"
ORDER_STOP_LOSS = "STOP_LOSS"

# Market Regimes
REGIME_BULL_TREND = "bull_trend"
REGIME_BEAR_TREND = "bear_trend"
REGIME_SIDEWAYS = "sideways"
REGIME_VOLATILE = "volatile"

# Safety Limits (Defaults - overridden by SafetyLayer)
DEFAULT_MAX_RISK_PER_TRADE = 0.005  # 0.5%
DEFAULT_MAX_DAILY_LOSS = 0.02       # 2%
DEFAULT_MAX_POSITIONS = 5
