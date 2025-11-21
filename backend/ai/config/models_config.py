"""
Multi-AI Models Configuration
Defines all AI models available for trading strategy verification
"""

from typing import List, Dict, Optional
from enum import Enum

class ModelTier(Enum):
    """Model tier classification"""
    TIER_1_REASONING = "tier_1_reasoning"  # Best reasoning models for trading
    TIER_2_BALANCED = "tier_2_balanced"    # Balanced general-purpose models
    TIER_3_SPECIALIZED = "tier_3_specialized"  # Code/specialized models

class ModelRole(Enum):
    """Model roles in verification"""
    CHIEF_ANALYST = "chief_analyst"
    TECHNICAL_EXPERT = "technical_expert"
    POWERHOUSE = "powerhouse"
    INNOVATION_LEADER = "innovation_leader"
    DEVILS_ADVOCATE = "devils_advocate"
    VALIDATOR = "validator"
    FAST_ANALYST = "fast_analyst"
    ASIAN_MARKET_EXPERT = "asian_market_expert"
    CODE_ANALYST = "code_analyst"
    ML_EXPERT = "ml_expert"
    HYBRID_REASONER = "hybrid_reasoner"

# Complete model configuration
AI_MODELS_CONFIG = {
    # ===== TIER 1: Best Reasoning Models (5 models) =====
    "tier_1_reasoning": [
        {
            "id": "openrouter/sherlock-think-alpha",
            "name": "Sherlock Think Alpha",
            "role": ModelRole.CHIEF_ANALYST,
            "tier": ModelTier.TIER_1_REASONING,
            "specialty": "Deep multi-step reasoning and analysis",
            "context_length": 1_840_000,
            "weight": 1.2,  # Highest weight for best reasoner
            "enabled": True,
            "priority": 1,
            "description": "Best for complex strategy analysis with detailed reasoning steps",
            "best_for": ["complex strategies", "multi-indicator systems", "risk assessment"]
        },
        {
            "id": "openrouter/sherlock-dash-alpha",
            "name": "Sherlock Dash Alpha",
            "role": ModelRole.FAST_ANALYST,
            "tier": ModelTier.TIER_1_REASONING,
            "specialty": "Fast reasoning with good accuracy",
            "context_length": 1_840_000,
            "weight": 1.0,
            "enabled": True,
            "priority": 2,
            "description": "Quick analysis while maintaining reasoning quality",
            "best_for": ["quick validation", "simple strategies", "confirmation"]
        },
        {
            "id": "meta-llama/llama-3.3-70b-instruct:free",
            "name": "Llama 3.3 70B",
            "role": ModelRole.POWERHOUSE,
            "tier": ModelTier.TIER_1_REASONING,
            "specialty": "General intelligence and comprehensive analysis",
            "context_length": 128_000,
            "weight": 1.1,
            "enabled": True,
            "priority": 3,
            "description": "Most powerful free model, excellent for detailed analysis",
            "best_for": ["comprehensive analysis", "long strategy documents", "general intelligence"]
        },
        {
            "id": "deepseek/deepseek-chat-v3-0324:free",
            "name": "DeepSeek V3",
            "role": ModelRole.INNOVATION_LEADER,
            "tier": ModelTier.TIER_1_REASONING,
            "specialty": "Latest technology and modern techniques",
            "context_length": 163_840,
            "weight": 1.0,
            "enabled": True,
            "priority": 4,
            "description": "Cutting-edge model with latest trading insights",
            "best_for": ["modern strategies", "latest techniques", "innovation"]
        },
        {
            "id": "deepseek/deepseek-r1-0528:free",
            "name": "DeepSeek R1",
            "role": ModelRole.TECHNICAL_EXPERT,
            "tier": ModelTier.TIER_1_REASONING,
            "specialty": "Technical analysis and pattern recognition",
            "context_length": 163_840,
            "weight": 1.1,
            "enabled": True,
            "priority": 5,
            "description": "Expert in technical indicators and chart patterns",
            "best_for": ["technical analysis", "indicators", "chart patterns"]
        }
    ],
    
    # ===== TIER 2: Balanced General Models (3 models) =====
    "tier_2_balanced": [
        {
            "id": "mistralai/mistral-small-3.1-24b-instruct:free",
            "name": "Mistral Small 3.1",
            "role": ModelRole.DEVILS_ADVOCATE,
            "tier": ModelTier.TIER_2_BALANCED,
            "specialty": "Risk analysis and contrarian perspective",
            "context_length": 128_000,
            "weight": 1.0,
            "enabled": True,
            "priority": 6,
            "description": "European model with focus on risk and alternative views",
            "best_for": ["risk assessment", "finding flaws", "contrarian analysis"]
        },
        {
            "id": "google/gemma-3-27b-it:free",
            "name": "Gemma 3 27B",
            "role": ModelRole.VALIDATOR,
            "tier": ModelTier.TIER_2_BALANCED,
            "specialty": "Validation and fact-checking",
            "context_length": 131_072,
            "weight": 0.9,
            "enabled": True,
            "priority": 7,
            "description": "Reliable Google model for validation and error detection",
            "best_for": ["validation", "math verification", "fact-checking"]
        },
        {
            "id": "z-ai/glm-4.5-air:free",
            "name": "GLM 4.5 Air",
            "role": ModelRole.ASIAN_MARKET_EXPERT,
            "tier": ModelTier.TIER_2_BALANCED,
            "specialty": "Asian market insights",
            "context_length": 131_072,
            "weight": 0.9,
            "enabled": True,
            "priority": 8,
            "description": "Chinese model with insights into Asian markets",
            "best_for": ["NIFTY strategies", "Asian markets", "regional insights"]
        }
    ],
    
    # ===== TIER 3: Specialized Models (4 models - for future use) =====
    "tier_3_specialized": [
        {
            "id": "qwen/qwen3-coder:free",
            "name": "Qwen3 Coder",
            "role": ModelRole.CODE_ANALYST,
            "tier": ModelTier.TIER_3_SPECIALIZED,
            "specialty": "Code analysis and algorithmic trading",
            "context_length": 262_000,
            "weight": 1.0,
            "enabled": False,  # Enable in Phase 6
            "priority": 9,
            "description": "Expert in analyzing code-based trading strategies",
            "best_for": ["Pine Script", "Python bots", "algorithm analysis"],
            "future_phase": 6
        },
        {
            "id": "kwaipilot/kat-coder-pro:free",
            "name": "KAT-Coder Pro",
            "role": ModelRole.ML_EXPERT,
            "tier": ModelTier.TIER_3_SPECIALIZED,
            "specialty": "Machine learning strategies",
            "context_length": 256_000,
            "weight": 1.0,
            "enabled": False,  # Enable in Phase 6
            "priority": 10,
            "description": "Specialized in ML-based trading systems",
            "best_for": ["ML strategies", "neural networks", "quant analysis"],
            "future_phase": 6
        },
        {
            "id": "tngtech/deepseek-r1t2-chimera:free",
            "name": "DeepSeek R1T2 Chimera",
            "role": ModelRole.HYBRID_REASONER,
            "tier": ModelTier.TIER_3_SPECIALIZED,
            "specialty": "Hybrid reasoning approaches",
            "context_length": 163_840,
            "weight": 0.9,
            "enabled": False,  # Backup/alternative
            "priority": 11,
            "description": "Alternative reasoning model for diversity",
            "best_for": ["alternative perspectives", "backup verification"],
            "future_phase": 6
        },
        {
            "id": "tngtech/deepseek-r1t-chimera:free",
            "name": "DeepSeek R1T Chimera",
            "role": ModelRole.HYBRID_REASONER,
            "tier": ModelTier.TIER_3_SPECIALIZED,
            "specialty": "Alternative hybrid reasoning",
            "context_length": 163_840,
            "weight": 0.8,
            "enabled": False,  # Backup/alternative
            "priority": 12,
            "description": "Older version for fallback scenarios",
            "best_for": ["backup analysis", "alternative reasoning"],
            "future_phase": 6
        }
    ]
}

# Quick access lists
def get_all_models() -> List[Dict]:
    """Get all configured models"""
    all_models = []
    for tier in AI_MODELS_CONFIG.values():
        all_models.extend(tier)
    return all_models

def get_active_models() -> List[Dict]:
    """Get only enabled models"""
    return [model for model in get_all_models() if model["enabled"]]

def get_models_by_tier(tier: ModelTier) -> List[Dict]:
    """Get models by tier"""
    return AI_MODELS_CONFIG.get(tier.value, [])

def get_model_by_id(model_id: str) -> Optional[Dict]:
    """Get specific model by ID"""
    for model in get_all_models():
        if model["id"] == model_id:
            return model
    return None

def get_trading_models() -> List[Dict]:
    """Get models for active trading verification (Tier 1 + Tier 2)"""
    tier1 = get_models_by_tier(ModelTier.TIER_1_REASONING)
    tier2 = get_models_by_tier(ModelTier.TIER_2_BALANCED)
    return [m for m in tier1 + tier2 if m["enabled"]]

def get_specialized_models() -> List[Dict]:
    """Get specialized models (Tier 3)"""
    return get_models_by_tier(ModelTier.TIER_3_SPECIALIZED)

# Model statistics
def get_model_stats() -> Dict:
    """Get statistics about configured models"""
    all_models = get_all_models()
    active = get_active_models()
    
    return {
        "total_models": len(all_models),
        "active_models": len(active),
        "inactive_models": len(all_models) - len(active),
        "tier_1_count": len(get_models_by_tier(ModelTier.TIER_1_REASONING)),
        "tier_2_count": len(get_models_by_tier(ModelTier.TIER_2_BALANCED)),
        "tier_3_count": len(get_models_by_tier(ModelTier.TIER_3_SPECIALIZED)),
        "trading_models": len(get_trading_models()),
        "specialized_models": len(get_specialized_models())
    }

# Configuration validation
def validate_config() -> bool:
    """Validate model configuration"""
    try:
        all_models = get_all_models()
        
        # Check for duplicate IDs
        ids = [m["id"] for m in all_models]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate model IDs found")
        
        # Check required fields
        required_fields = ["id", "name", "role", "tier", "weight", "enabled"]
        for model in all_models:
            for field in required_fields:
                if field not in model:
                    raise ValueError(f"Model {model.get('id', 'unknown')} missing field: {field}")
        
        return True
    except Exception as e:
        print(f"Configuration validation error: {e}")
        return False

if __name__ == "__main__":
    # Test configuration
    print("=" * 60)
    print("Multi-AI Models Configuration")
    print("=" * 60)
    
    # Validate
    if validate_config():
        print("✓ Configuration valid")
    else:
        print("✗ Configuration invalid")
    
    # Stats
    stats = get_model_stats()
    print(f"\nTotal Models: {stats['total_models']}")
    print(f"Active Models: {stats['active_models']}")
    print(f"Trading Models: {stats['trading_models']}")
    print(f"Specialized Models: {stats['specialized_models']}")
    
    print("\n" + "=" * 60)
    print("Active Trading Models (8):")
    print("=" * 60)
    for model in get_trading_models():
        print(f"  {model['priority']}. {model['name']}")
        print(f"     Role: {model['role'].value}")
        print(f"     Specialty: {model['specialty']}")
        print(f"     Weight: {model['weight']}")
        print()
    
    print("=" * 60)
    print("Specialized Models (4 - Future Use):")
    print("=" * 60)
    for model in get_specialized_models():
        status = "✓ Enabled" if model['enabled'] else "○ Disabled"
        print(f"  {model['priority']}. {model['name']} [{status}]")
        print(f"     Future Phase: {model.get('future_phase', 'N/A')}")
        print()
