import yfinance as yf
from datetime import datetime

print("=" * 60)
print("YAHOO FINANCE DATA VERIFICATION")
print("=" * 60)

# Fetch NIFTY 50
print("\n### NIFTY 50 (^NSEI) ###")
nifty = yf.Ticker("^NSEI")
nifty_hist = nifty.history(period="5d")
print(f"Last 5 days history:")
print(nifty_hist[['Close']])
if not nifty_hist.empty:
    latest_close = nifty_hist['Close'].iloc[-1]
    print(f"\nLatest Close: {latest_close:.2f}")

# Fetch BANKNIFTY  
print("\n### BANKNIFTY (^NSEBANK) ###")
bn = yf.Ticker("^NSEBANK")
bn_hist = bn.history(period="5d")
print(f"Last 5 days history:")
print(bn_hist[['Close']])
if not bn_hist.empty:
    latest_close = bn_hist['Close'].iloc[-1]
    print(f"\nLatest Close: {latest_close:.2f}")

print("\n" + "=" * 60)
print("EXPECTED VALUES (from web search):")
print("NIFTY 50: 23,518.50 (Nov 19, 2024)")
print("=" * 60)
