import datetime
import pandas as pd
from typing import List, Dict
from backend.data.tickers import ALL_TICKERS
from backend.data_providers.manager import DataProviderManager
from backend.database.db import DatabaseManager
from backend.notifications.telegram_bot import TelegramBot

class MorningScanner:
    """
    Scans the market at 8:00 AM to identify potential opportunities.
    """

    def __init__(self):
        self.data_manager = DataProviderManager()
        self.db = DatabaseManager()
        self.bot = TelegramBot()

    def scan_market(self) -> str:
        """
        Main function to scan the market and generate a report.
        Returns the generated report content.
        """
        print("--- Starting Morning Scan ---")
        opportunities = []
        
        # Use ALL_TICKERS from updated tickers.py
        total_tickers = len(ALL_TICKERS)
        print(f"Scanning {total_tickers} symbols...")

        import time
        
        for i, symbol in enumerate(ALL_TICKERS):
            try:
                # Rate Limiting: Sleep every 10 requests to be safe with Yahoo
                if i % 10 == 0 and i > 0:
                    time.sleep(1)

                # 1. Get Historical Data (Last 5 days)
                df = self.data_manager.get_historical_data(symbol, period="5d")
                if df is None or df.empty:
                    continue

                # 2. Analyze (Simple Momentum Strategy)
                # Condition: Close > Open (Green Candle) AND Volume > Average Volume
                last_candle = df.iloc[-1]
                avg_volume = df['Volume'].mean()
                
                is_bullish = last_candle['Close'] > last_candle['Open']
                high_volume = last_candle['Volume'] > (avg_volume * 1.2) # 20% above average
                
                # Additional check: Price above 50-day MA (if we had enough data, for now simple check)
                # price_change = (last_candle['Close'] - df.iloc[0]['Close']) / df.iloc[0]['Close']
                
                if is_bullish and high_volume:
                    opportunities.append({
                        "symbol": symbol,
                        "last_price": last_candle['Close'],
                        "volume": last_candle['Volume'],
                        "reason": "Bullish Momentum + High Volume (>20% avg)"
                    })
            except Exception as e:
                print(f"Error scanning {symbol}: {e}")

        # 3. Select Top 50 (Sort by Volume for now as a proxy for liquidity/interest)
        # In a real app, we'd sort by 'Momentum Score'
        opportunities.sort(key=lambda x: x['volume'], reverse=True)
        top_picks = opportunities[:50]
        
        # 4. Save Predictions to DB (Mock table for now, or use existing strategies table)
        self._save_predictions(top_picks)

        # 5. Generate Report
        report = self._generate_report(top_picks)
        return report

    def _save_predictions(self, picks: List[Dict]):
        # In a real app, we'd have a 'predictions' table.
        # For now, we'll log it or store it as a 'strategy' in the existing DB
        pass

    def _generate_report(self, picks: List[Dict]) -> str:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        report = f"# 🌅 Morning Opportunity Report - {date_str}\n\n"
        report += "Based on overnight analysis and momentum signals, here are the top stocks to watch today:\n\n"
        
        if not picks:
            report += "No strong signals found today. Market might be choppy.\n"
        else:
            report += "| Symbol | Last Price | Reason |\n"
            report += "|---|---|---|\n"
            for pick in picks:
                report += f"| **{pick['symbol']}** | {pick['last_price']:.2f} | {pick['reason']} |\n"
        
        report += "\n**Strategy:** Look for entries if price breaks above yesterday's high.\n"
        
        # Save report to DB as a daily report
        self.db.save_report(date_str, report)
        
        # Send Telegram Alert
        self.bot.send_alert(report)
        return report

if __name__ == "__main__":
    scanner = MorningScanner()
    print(scanner.scan_market())
