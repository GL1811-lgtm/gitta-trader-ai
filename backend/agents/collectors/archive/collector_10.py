from datetime import datetime, UTC
from .base_collector import BaseCollectorAgent
from backend.ai.openrouter_client import OpenRouterClient

class CollectorAgent10(BaseCollectorAgent):
    """Market Sentiment Collector using OpenRouter."""
    def __init__(self, agent_id, source_name):
        super().__init__(agent_id, source_name)
        self.ai_client = OpenRouterClient()

    def collect(self) -> list[dict]:
        try:
            prompt = "Analyze the general sentiment of the stock market (Fear vs Greed) and suggest a trading approach (Risk-On vs Risk-Off)."
            response = self.ai_client.get_chat_completion(
                model="mistralai/mistral-small-3.1-24b-instruct:free",
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.get('choices', [{}])[0].get('message', {}).get('content', 'No sentiment analysis available.')
            
            return [{
                "title": "AI Market Sentiment Analysis",
                "source": "Market Sentiment (AI)",
                "content": content,
                "tags": ["sentiment", "psychology", "risk"]
            }]
        except Exception:
            return []