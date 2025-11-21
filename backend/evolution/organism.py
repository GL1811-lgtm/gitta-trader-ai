import random
import copy
from typing import Dict, Any, List
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)

@dataclass
class TradingOrganism:
    """
    Represents a single trading strategy with its own DNA (parameters).
    """
    generation: int
    id: str
    dna: Dict[str, Any]
    fitness: float = 0.0
    parents: List[str] = field(default_factory=list)
    
    @classmethod
    def create_random(cls, generation: int, organism_id: str) -> 'TradingOrganism':
        """Create a new organism with random DNA."""
        dna = {
            # Entry Rules
            "rsi_period": random.randint(5, 30),
            "rsi_overbought": random.randint(65, 85),
            "rsi_oversold": random.randint(15, 35),
            "ma_fast": random.randint(5, 50),
            "ma_slow": random.randint(50, 200),
            
            # Risk Management
            "stop_loss_pct": round(random.uniform(0.5, 5.0), 2),
            "take_profit_pct": round(random.uniform(1.0, 10.0), 2),
            "max_position_size_pct": round(random.uniform(1.0, 20.0), 2),
            "trailing_stop_activation": round(random.uniform(0.5, 3.0), 2),
            
            # Strategy Type (Gene expression)
            "strategy_type": random.choice(["trend_following", "mean_reversion", "breakout"])
        }
        
        # Ensure logical constraints
        if dna["ma_fast"] >= dna["ma_slow"]:
            dna["ma_fast"], dna["ma_slow"] = dna["ma_slow"], dna["ma_fast"]
            
        return cls(generation=generation, id=organism_id, dna=dna)

    def mutate(self, mutation_rate: float = 0.1):
        """
        Randomly alter DNA based on mutation rate.
        """
        if random.random() < mutation_rate:
            # Mutate RSI Period
            self.dna["rsi_period"] = max(2, min(50, self.dna["rsi_period"] + random.randint(-2, 2)))
            
        if random.random() < mutation_rate:
            # Mutate Stop Loss
            self.dna["stop_loss_pct"] = max(0.1, round(self.dna["stop_loss_pct"] * random.uniform(0.8, 1.2), 2))
            
        if random.random() < mutation_rate:
            # Mutate Take Profit
            self.dna["take_profit_pct"] = max(0.2, round(self.dna["take_profit_pct"] * random.uniform(0.8, 1.2), 2))
            
        if random.random() < mutation_rate:
            # Flip Strategy Type
            self.dna["strategy_type"] = random.choice(["trend_following", "mean_reversion", "breakout"])

    def crossover(self, partner: 'TradingOrganism', child_id: str) -> 'TradingOrganism':
        """
        Combine DNA with another organism to create a child.
        """
        child_dna = {}
        for key in self.dna:
            # 50/50 chance to inherit from either parent
            child_dna[key] = self.dna[key] if random.random() > 0.5 else partner.dna[key]
            
        return TradingOrganism(
            generation=self.generation + 1,
            id=child_id,
            dna=child_dna,
            parents=[self.id, partner.id]
        )
