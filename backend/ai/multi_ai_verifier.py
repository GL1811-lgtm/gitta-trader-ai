"""
Multi-AI Verifier
Coordinates multiple AI models to verify trading strategies
"""

import os
import asyncio
import aiohttp
from typing import List, Dict, Optional
from datetime import datetime
from dotenv import load_dotenv

from backend.ai.config.models_config import (
    get_active_models,
    get_trading_models,
    get_model_by_id
)

load_dotenv()

class MultiAIVerifier:
    """Verifies trading strategies using multiple AI models"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1"
        
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
    
    async def _call_single_model(
        self,
        session: aiohttp.ClientSession,
        model_config: Dict,
        messages: List[Dict],
        timeout: int = 30
    ) -> Dict:
        """
        Call a single AI model asynchronously
        
        Args:
            session: aiohttp session
            model_config: Model configuration dict
            messages: Chat messages
            timeout: Request timeout in seconds
            
        Returns:
            Response dict with model analysis
        """
        url = f"{self.base_url}/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://gitta-trader-ai.com",
            "X-Title": "Gitta Trader AI",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model_config["id"],
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        start_time = datetime.now()
        
        try:
            async with session.post(
                url,
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=timeout)
            ) as response:
                response.raise_for_status()
                data = await response.json()
                
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                return {
                    "model_id": model_config["id"],
                    "model_name": model_config["name"],
                    "role": model_config["role"].value,
                    "specialty": model_config["specialty"],
                    "weight": model_config["weight"],
                    "content": data["choices"][0]["message"]["content"],
                    "success": True,
                    "duration": duration,
                    "timestamp": datetime.now().isoformat(),
                    "usage": data.get("usage", {})
                }
                
        except asyncio.TimeoutError:
            return {
                "model_id": model_config["id"],
                "model_name": model_config["name"],
                "role": model_config["role"].value,
                "content": None,
                "success": False,
                "error": "Request timeout",
                "duration": timeout,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "model_id": model_config["id"],
                "model_name": model_config["name"],
                "role": model_config["role"].value,
                "content": None,
                "success": False,
                "error": str(e),
                "duration": (datetime.now() - start_time).total_seconds(),
                "timestamp": datetime.now().isoformat()
            }
    
    async def verify_strategy_async(
        self,
        strategy_text: str,
        use_trading_models_only: bool = True
    ) -> Dict:
        """
        Verify a trading strategy using multiple AI models (async)
        
        Args:
            strategy_text: Description of the trading strategy
            use_trading_models_only: If True, use only active trading models
            
        Returns:
            Dict with all model responses and consensus
        """
        # Get models to use
        if use_trading_models_only:
            models = get_trading_models()
        else:
            models = get_active_models()
        
        if not models:
            raise ValueError("No active models configured")
        
        # Prepare messages
        system_message = {
            "role": "system",
            "content": "You are an expert trading strategy analyst. Analyze the given strategy and provide: 1) Viability score (1-10), 2) Key strengths, 3) Key risks, 4) Recommendation (VIABLE/MODERATE/RISKY). Be concise but thorough."
        }
        
        user_message = {
            "role": "user",
            "content": f"Analyze this trading strategy:\n\n{strategy_text}\n\nProvide a viability score (1-10) and your analysis."
        }
        
        messages = [system_message, user_message]
        
        # Call all models in parallel
        start_time = datetime.now()
        
        async with aiohttp.ClientSession() as session:
            tasks = [
                self._call_single_model(session, model, messages)
                for model in models
            ]
            
            responses = await asyncio.gather(*tasks)
        
        end_time = datetime.now()
        total_duration = (end_time - start_time).total_seconds()
        
        # Count successes
        successful = [r for r in responses if r["success"]]
        failed = [r for r in responses if not r["success"]]
        
        return {
            "strategy": strategy_text,
            "timestamp": datetime.now().isoformat(),
            "total_models": len(models),
            "successful_responses": len(successful),
            "failed_responses": len(failed),
            "total_duration": total_duration,
            "responses": responses,
            "status": "completed"
        }
    
    def verify_strategy(
        self,
        strategy_text: str,
        use_trading_models_only: bool = True
    ) -> Dict:
        """
        Verify a trading strategy using multiple AI models (sync wrapper)
        
        Args:
            strategy_text: Description of the trading strategy
            use_trading_models_only: If True, use only active trading models
            
        Returns:
            Dict with all model responses and consensus
        """
        return asyncio.run(
            self.verify_strategy_async(strategy_text, use_trading_models_only)
        )
    
    def analyze_with_model(
        self,
        model_id: str,
        prompt: str
    ) -> Dict:
        """
        Analyze with a specific model
        
        Args:
            model_id: Model ID to use
            prompt: Analysis prompt
            
        Returns:
            Analysis result
        """
        model_config = get_model_by_id(model_id)
        if not model_config:
            return {"error": f"Model {model_id} not found"}
        
        messages = [{"role": "user", "content": prompt}]
        
        async def call():
            async with aiohttp.ClientSession() as session:
                return await self._call_single_model(session, model_config, messages)
        
        return asyncio.run(call())


# Convenience function
def verify_trading_strategy(strategy_text: str) -> Dict:
    """Quick verification of a trading strategy"""
    verifier = MultiAIVerifier()
    return verifier.verify_strategy(strategy_text)


if __name__ == "__main__":
    # Test the verifier
    print("=" * 60)
    print("Multi-AI Verifier Test")
    print("=" * 60)
    
    verifier = MultiAIVerifier()
    
    # Test strategy
    strategy = """
    Buy when RSI crosses below 30 (oversold)
    Sell when RSI crosses above 70 (overbought)
    Timeframe: 15 minutes
    Stop loss: 2%
    """
    
    print(f"\nTesting strategy verification...")
    print(f"Strategy: {strategy.strip()}")
    print(f"\nCalling {len(get_trading_models())} AI models in parallel...")
    print("This may take 6-10 seconds...\n")
    
    result = verifier.verify_strategy(strategy)
    
    print("=" * 60)
    print("Results:")
    print("=" * 60)
    print(f"Total Duration:  {result['total_duration']:.2f} seconds")
    print(f"Models Called: {result['total_models']}")
    print(f"Successful: {result['successful_responses']}")
    print(f"Failed: {result['failed_responses']}")
    print()
    
    print("=" * 60)
    print("Model Responses:")
    print("=" * 60)
    for response in result['responses']:
        if response['success']:
            print(f"\n✓ {response['model_name']} ({response['duration']:.2f}s)")
            print(f"  Role: {response['role']}")
            print(f"  Response: {response['content'][:200]}...")
        else:
            print(f"\n✗ {response['model_name']}")
            print(f"  Error: {response.get('error', 'Unknown error')}")
