import datetime
from typing import List, Dict
from backend.data_providers.manager import DataProviderManager
from backend.database.db import DatabaseManager
from backend.notifications.telegram_bot import TelegramBot

class EveningValidator:
    """
    Validates predictions at 5:00 PM.
    """

    def __init__(self):
        self.data_manager = DataProviderManager()
        self.db = DatabaseManager()
        self.bot = TelegramBot()

    def validate_predictions(self) -> str:
        """
        Checks how the morning picks performed.
        """
        print("--- Starting Evening Validation ---")
        
        # 1. Get Morning Report (to see what we predicted)
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        morning_report = self.db.get_latest_report() # Ideally fetch by date/type
        
        if not morning_report:
            return "No morning report found to validate."

        # Parse symbols from report (Simple parsing for now)
        # In a real app, we'd query the 'predictions' table
        predicted_symbols = self._extract_symbols_from_report(morning_report)
        
        results = []
        for symbol in predicted_symbols:
            try:
                # Get today's close
                price = self.data_manager.get_live_price(symbol)
                if price:
                    # Mock logic: Assume entry was at 'Last Price' from morning (approx)
                    # Real logic would need stored entry price
                    results.append({
                        "symbol": symbol,
                        "close_price": price,
                        "status": "Tracked"
                    })
            except Exception as e:
                print(f"Error validating {symbol}: {e}")

        # Generate Report
        report = self._generate_report(results)
        return report

    def _extract_symbols_from_report(self, report_content: str) -> List[str]:
        # Quick hack to extract symbols from markdown table
        symbols = []
        lines = report_content.split('\n')
        for line in lines:
            if "|" in line and "**" in line:
                try:
                    # Extract text between ** **
                    parts = line.split("**")
                    if len(parts) >= 2:
                        symbols.append(parts[1])
                except:
                    pass
        return symbols

    def _generate_report(self, results: List[Dict]) -> str:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        report = f"# 🌇 Evening Performance Review - {date_str}\n\n"
        report += "Here is how our morning predictions performed:\n\n"
        
        if not results:
            report += "No data available for validation.\n"
        else:
            report += "| Symbol | Closing Price | Status |\n"
            report += "|---|---|---|\n"
            for res in results:
                report += f"| **{res['symbol']}** | {res['close_price']:.2f} | {res['status']} |\n"
        
        # Save to DB (Appending or new report)
        # For now, we just print it or save as a new entry
        self.db.save_report(f"{date_str}_EVENING", report)
        
        # Send Telegram Alert
        self.bot.send_alert(report)
        return report

if __name__ == "__main__":
    validator = EveningValidator()
    print(validator.validate_predictions())
