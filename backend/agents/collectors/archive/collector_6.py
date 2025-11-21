from datetime import datetime, UTC
from .base_collector import BaseCollectorAgent
from backend.ai.openrouter_client import OpenRouterClient

class CollectorAgent6(BaseCollectorAgent):
    """Web News Collector using OpenRouter to summarize market news."""
    def __init__(self, agent_id, source_name):
        super().__init__(agent_id, source_name)
        self.ai_client = OpenRouterClient()

    def collect(self) -> list[dict]:
        # Use AI to generate a news summary strategy based on its knowledge
        try:
            prompt = "Summarize a potential trading strategy based on current general market news trends (Inflation, Interest Rates, Geopolitics). Format as a trading strategy."
            response = self.ai_client.get_chat_completion(
                model="mistralai/mistral-small-3.1-24b-instruct:free",
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.get('choices', [{}])[0].get('message', {}).get('content', 'No news analysis available.')
            
            return [{
                "title": "Global Macro News Strategy",
                "source": "Web News (AI Analysis)",
                "content": content,
                "tags": ["news", "macro", "fundamental"]
            }]
        except Exception:
            return []