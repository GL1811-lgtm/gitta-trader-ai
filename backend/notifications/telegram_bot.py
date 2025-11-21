import os
import requests

class TelegramBot:
    """
    Sends notifications via Telegram.
    """

    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    def send_alert(self, message: str) -> bool:
        """
        Sends a message to the configured Telegram chat.
        """
        if not self.bot_token or not self.chat_id:
            print(f"[MOCK TELEGRAM] {message}")
            return True

        try:
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "Markdown"
            }
            response = requests.post(self.base_url, json=payload)
            if response.status_code == 200:
                print("Telegram alert sent successfully.")
                return True
            else:
                print(f"Failed to send Telegram alert: {response.text}")
                return False
        except Exception as e:
            print(f"Error sending Telegram alert: {e}")
            return False
