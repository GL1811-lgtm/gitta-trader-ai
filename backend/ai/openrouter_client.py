"""
OpenRouter AI Integration
Provides access to multiple AI models through OpenRouter API
"""

import os
import requests
from typing import Dict, List, Optional
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class OpenRouterClient:
    """Client for OpenRouter AI API"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1"
        self.default_model = "google/gemma-3-27b-it:free"  # Free model
        
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
    
    def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Dict:
        """
        Send a chat completion request to OpenRouter
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model to use (default: google/gemma-3-27b-it:free)
            temperature: Randomness (0-1)
            max_tokens: Maximum response length
            
        Returns:
            Response dict with 'content' and 'model'
        """
        url = f"{self.base_url}/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://gitta-trader-ai.com",
            "X-Title": "Gitta Trader AI",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model or self.default_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "content": data["choices"][0]["message"]["content"],
                "model": data["model"],
                "usage": data.get("usage", {}),
                "success": True
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "content": None,
                "error": str(e),
                "success": False
            }
    
    def analyze_strategy(self, strategy_text: str) -> str:
        """
        Analyze a trading strategy using AI
        
        Args:
            strategy_text: Description of the trading strategy
            
        Returns:
            AI analysis of the strategy
        """
        messages = [
            {
                "role": "system",
                "content": "You are an expert trading strategy analyst. Analyze trading strategies for viability, risk, and potential returns."
            },
            {
                "role": "user",
                "content": f"Analyze this trading strategy:\n\n{strategy_text}\n\nProvide: 1) Viability score (1-10), 2) Key risks, 3) Potential returns, 4) Recommendation"
            }
        ]
        
        result = self.chat_completion(messages, max_tokens=500)
        
        if result["success"]:
            return result["content"]
        else:
            return f"Error analyzing strategy: {result.get('error', 'Unknown error')}"
    
    def research_market_topic(self, topic: str) -> str:
        """
        Research a market-related topic
        
        Args:
            topic: Topic to research
            
        Returns:
            Research summary
        """
        messages = [
            {
                "role": "system",
                "content": "You are a financial market research analyst. Provide concise, accurate market insights."
            },
            {
                "role": "user",
                "content": f"Research and summarize: {topic}"
            }
        ]
        
        result = self.chat_completion(messages, max_tokens=800)
        
        if result["success"]:
            return result["content"]
        else:
            return f"Error researching topic: {result.get('error', 'Unknown error')}"
    
    def generate_report_summary(self, data: str) -> str:
        """
        Generate a summary report from data
        
        Args:
            data: Raw data to summarize
            
        Returns:
            Formatted summary
        """
        messages = [
            {
                "role": "system",
                "content": "You are a financial report writer. Create clear, actionable summaries."
            },
            {
                "role": "user",
                "content": f"Create a concise trading report summary from this data:\n\n{data}"
            }
        ]
        
        result = self.chat_completion(messages, max_tokens=600)
        
        if result["success"]:
            return result["content"]
        else:
            return f"Error generating summary: {result.get('error', 'Unknown error')}"


# Convenience function for quick access
def get_openrouter_client() -> OpenRouterClient:
    """Get an OpenRouter client instance"""
    return OpenRouterClient()


if __name__ == "__main__":
    # Test the client
    client = OpenRouterClient()
    
    # Test chat
    response = client.chat_completion([
        {"role": "user", "content": "What are the key indicators for a bullish market?"}
    ])
    
    print("Test Response:")
    print(response)
