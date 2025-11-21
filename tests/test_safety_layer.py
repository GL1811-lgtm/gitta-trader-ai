"""
Tests for Safety Layer
"""
import pytest
from backend.core.safety_layer import SafetyLimits

class TestSafetyLayer:
    def test_initialization(self):
        safety = SafetyLimits(current_capital=100000)
        assert safety.current_capital == 100000
        assert safety.daily_pnl == 0
        assert safety.is_circuit_breaker_active == False

    def test_risk_per_trade_limit(self):
        safety = SafetyLimits(current_capital=100000)
        # Max risk is 0.5% = 500
        
        # Case 1: Safe trade (Risk 400)
        # Entry 100, Stop 96, Qty 100 -> Risk 4 * 100 = 400
        result = safety.validate_trade(entry_price=100, stop_loss=96, quantity=100)
        assert result['allowed'] == True
        
        # Case 2: Unsafe trade (Risk 600)
        # Entry 100, Stop 94, Qty 100 -> Risk 6 * 100 = 600
        result = safety.validate_trade(entry_price=100, stop_loss=94, quantity=100)
        assert result['allowed'] == False
        assert "Risk" in result['reason']

    def test_position_size_limit(self):
        safety = SafetyLimits(current_capital=100000)
        # Max position is 20% = 20,000
        
        # Case 1: Safe position (15,000)
        result = safety.validate_trade(entry_price=150, stop_loss=149, quantity=100)
        assert result['allowed'] == True
        
        # Case 2: Unsafe position (25,000)
        result = safety.validate_trade(entry_price=250, stop_loss=249, quantity=100)
        assert result['allowed'] == False
        assert "Position size" in result['reason']

    def test_daily_loss_limit(self):
        safety = SafetyLimits(current_capital=100000)
        # Max daily loss is 2% = 2000
        
        # Simulate loss of 1500
        safety.update_capital(98500) 
        assert safety.daily_pnl == -1500
        assert safety.circuit_breaker_check() == False
        
        # Simulate loss of 2100
        safety.update_capital(97900)
        assert safety.daily_pnl == -2100
        
        # Check circuit breaker
        assert safety.circuit_breaker_check() == True
        
        # Validate trade should fail
        result = safety.validate_trade(entry_price=100, stop_loss=99, quantity=10)
        assert result['allowed'] == False
        assert "Daily loss limit hit" in result['reason']

    def test_consecutive_loss_limit(self):
        safety = SafetyLimits(current_capital=100000)
        
        # 4 losses
        for _ in range(4):
            safety.record_trade_result(-100)
            assert safety.circuit_breaker_check() == False
            
        # 5th loss
        safety.record_trade_result(-100)
        assert safety.consecutive_losses == 5
        assert safety.circuit_breaker_check() == True
        
        # Validate trade should fail
        result = safety.validate_trade(entry_price=100, stop_loss=99, quantity=10)
        assert result['allowed'] == False
        assert "Max consecutive losses" in result['reason']

    def test_max_trades_per_day(self):
        safety = SafetyLimits(current_capital=100000)
        
        # 19 trades
        for _ in range(19):
            safety.record_trade_result(10)
            
        result = safety.validate_trade(entry_price=100, stop_loss=99, quantity=10)
        assert result['allowed'] == True
        
        # 20th trade
        safety.record_trade_result(10)
        
        # 21st trade attempt
        result = safety.validate_trade(entry_price=100, stop_loss=99, quantity=10)
        assert result['allowed'] == False
        assert "Max trades per day" in result['reason']
