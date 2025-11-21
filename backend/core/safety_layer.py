"""
IMMUTABLE SAFETY LAYER - DO NOT MODIFY
This file enforces hard limits on trading risk.
Any attempt to bypass these limits will result in immediate rejection of orders.
"""
import logging
from datetime import datetime
from backend.core.constants import MODE_LIVE

logger = logging.getLogger(__name__)

class SafetyLimits:
    """
    Hardcoded safety limits that cannot be overridden by AI strategies.
    """
    # HARD LIMITS (Fixed values)
    MAX_RISK_PER_TRADE_PERCENT = 0.005  # 0.5% of capital
    MAX_DAILY_LOSS_PERCENT = 0.02       # 2.0% of capital
    MAX_CONSECUTIVE_LOSSES = 5          # Stop after 5 losses
    MAX_POSITION_SIZE_PERCENT = 0.20    # 20% of capital max per trade
    MAX_TRADES_PER_DAY = 20             # Circuit breaker for hyperactivity
    
    def __init__(self, current_capital: float, trading_mode: str = "paper"):
        self.initial_capital = current_capital
        self.current_capital = current_capital
        self.trading_mode = trading_mode
        self.daily_pnl = 0.0
        self.consecutive_losses = 0
        self.trades_today = 0
        self.is_circuit_breaker_active = False
        
    def update_capital(self, new_capital: float):
        """Update current capital and calculate daily P&L."""
        self.current_capital = new_capital
        self.daily_pnl = self.current_capital - self.initial_capital

    def record_trade_result(self, pnl: float):
        """Record the result of a closed trade."""
        self.trades_today += 1
        if pnl < 0:
            self.consecutive_losses += 1
        else:
            self.consecutive_losses = 0
            
    def validate_trade(self, entry_price: float, stop_loss: float, quantity: int) -> dict:
        """
        Validate a proposed trade against all safety limits.
        Returns: {'allowed': bool, 'reason': str}
        """
        if self.is_circuit_breaker_active:
            return {'allowed': False, 'reason': "Circuit breaker is ACTIVE. No trading allowed."}
            
        # 1. Check Daily Loss Limit
        daily_loss_percent = (self.daily_pnl / self.initial_capital) if self.initial_capital > 0 else 0
        if daily_loss_percent <= -self.MAX_DAILY_LOSS_PERCENT:
            self.is_circuit_breaker_active = True
            return {'allowed': False, 'reason': f"Daily loss limit hit ({daily_loss_percent*100:.2f}%). Trading stopped."}
            
        # 2. Check Consecutive Losses
        if self.consecutive_losses >= self.MAX_CONSECUTIVE_LOSSES:
            self.is_circuit_breaker_active = True
            return {'allowed': False, 'reason': f"Max consecutive losses ({self.consecutive_losses}) reached. Trading stopped."}
            
        # 3. Check Max Trades Per Day
        if self.trades_today >= self.MAX_TRADES_PER_DAY:
            return {'allowed': False, 'reason': f"Max trades per day ({self.MAX_TRADES_PER_DAY}) reached."}
            
        # 4. Check Position Size
        trade_value = entry_price * quantity
        max_position_value = self.current_capital * self.MAX_POSITION_SIZE_PERCENT
        if trade_value > max_position_value:
            return {'allowed': False, 'reason': f"Position size ({trade_value}) exceeds limit ({max_position_value})."}
            
        # 5. Check Risk Per Trade
        risk_per_share = abs(entry_price - stop_loss)
        total_risk = risk_per_share * quantity
        max_risk = self.current_capital * self.MAX_RISK_PER_TRADE_PERCENT
        
        if total_risk > max_risk:
            return {'allowed': False, 'reason': f"Risk ({total_risk}) exceeds limit ({max_risk})."}
            
        return {'allowed': True, 'reason': "Trade validated."}

    def circuit_breaker_check(self) -> bool:
        """Returns True if trading should be stopped completely."""
        daily_loss_percent = (self.daily_pnl / self.initial_capital) if self.initial_capital > 0 else 0
        
        if daily_loss_percent <= -self.MAX_DAILY_LOSS_PERCENT:
            self.is_circuit_breaker_active = True
            
        if self.consecutive_losses >= self.MAX_CONSECUTIVE_LOSSES:
            self.is_circuit_breaker_active = True
            
        return self.is_circuit_breaker_active
