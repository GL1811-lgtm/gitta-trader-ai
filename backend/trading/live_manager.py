from datetime import datetime
from typing import Dict, Optional
from backend.core.safety_layer import SafetyLimits
from backend.trading.approval_system import TradeApprovalSystem
from backend.utils.logger import logger

class LiveTradingManager:
    """
    Manages live trading with real capital, enforcing strict safety controls.
    """
    
    def __init__(self, initial_capital=25000):
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.enabled = False  # Live trading disabled by default
        self.emergency_stop = False
        
        # Safety systems
        self.safety_limits = SafetyLimits(current_capital=initial_capital)
        self.approval_system = TradeApprovalSystem(approval_threshold=10)
        
        # Daily tracking
        self.daily_pnl = 0.0
        self.daily_trades = 0
        self.trade_history = []
        
    def enable_live_trading(self, authorized_by: str) -> Dict:
        """Enable live trading (requires explicit authorization)."""
        if self.enabled:
            return {'success': False, 'message': 'Live trading already enabled'}
        
        logger.critical(f"LIVE TRADING ENABLED by {authorized_by}")
        logger.critical(f"Starting capital: ₹{self.initial_capital}")
        logger.critical(f"Max daily loss: ₹{self.safety_limits.max_daily_loss}")
        
        self.enabled = True
        self.emergency_stop = False
        
        return {
            'success': True,
            'message': 'Live trading enabled',
            'capital': self.current_capital,
            'safety_limits': {
                'max_daily_loss': self.safety_limits.max_daily_loss,
                'max_risk_per_trade': self.safety_limits.max_risk_per_trade,
                'max_position_size': self.safety_limits.max_position_size,
                'max_daily_trades': self.safety_limits.max_daily_trades
            }
        }
    
    def disable_live_trading(self, reason: str = 'Manual stop') -> Dict:
        """Disable live trading."""
        logger.critical(f"LIVE TRADING DISABLED: {reason}")
        self.enabled = False
        
        return {
            'success': True,
            'message': f'Live trading disabled: {reason}',
            'final_capital': self.current_capital,
            'total_pnl': self.current_capital - self.initial_capital
        }
    
    def emergency_stop_all(self, reason: str = 'Emergency stop activated') -> Dict:
        """Immediately halt all trading activity."""
        logger.critical(f"🚨 EMERGENCY STOP: {reason}")
        
        self.emergency_stop = True
        self.enabled = False
        
        # In production, this would also:
        # - Close all open positions
        # - Cancel all pending orders
        # - Notify user immediately
        
        return {
            'success': True,
            'message': 'Emergency stop activated - all trading halted',
            'reason': reason,
            'timestamp': datetime.now().isoformat()
        }
    
    def validate_trade(self, trade_details: Dict) -> Dict:
        """Validate a trade against safety limits."""
        if not self.enabled:
            return {'valid': False, 'reason': 'Live trading not enabled'}
        
        if self.emergency_stop:
            return {'valid': False, 'reason': 'Emergency stop active'}
        
        # Check safety limits
        is_valid, reason = self.safety_limits.validate_trade(
            position_size=trade_details.get('cost', 0),
            risk_amount=trade_details.get('risk', 0),
            current_daily_loss=abs(self.daily_pnl) if self.daily_pnl < 0 else 0,
            current_daily_trades=self.daily_trades
        )
        
        if not is_valid:
            logger.warning(f"Trade REJECTED by safety limits: {reason}")
            return {'valid': False, 'reason': reason}
        
        return {'valid': True}
    
    def submit_trade(self, trade_details: Dict) -> Dict:
        """Submit a trade (may require approval)."""
        # Validate first
        validation = self.validate_trade(trade_details)
        if not validation['valid']:
            return {'status': 'rejected', 'reason': validation['reason']}
        
        # Check if approval required
        if self.approval_system.requires_approval():
            trade_id = self.approval_system.submit_for_approval(trade_details)
            return {
                'status': 'pending_approval',
                'trade_id': trade_id,
                'message': 'Trade requires manual approval',
                'approvals_remaining': self.approval_system.approval_threshold - self.approval_system.approved_count
            }
        else:
            # Auto-approved, execute immediately
            return self._execute_trade(trade_details)
    
    def _execute_trade(self, trade_details: Dict) -> Dict:
        """Execute a trade (internal method)."""
        # In production, this would call broker API
        # For now, simulate execution
        
        logger.info(f"EXECUTING TRADE: {trade_details['side']} {trade_details['quantity']} {trade_details['symbol']}")
        
        self.daily_trades += 1
        self.trade_history.append({
            **trade_details,
            'executed_at': datetime.now().isoformat(),
            'status': 'executed'
        })
        
        return {
            'status': 'executed',
            'trade_id': f"exec_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'message': 'Trade executed successfully (simulated)'
        }
    
    def get_status(self) -> Dict:
        """Get current live trading status."""
        return {
            'enabled': self.enabled,
            'emergency_stop': self.emergency_stop,
            'current_capital': self.current_capital,
            'daily_pnl': self.daily_pnl,
            'daily_trades': self.daily_trades,
            'requires_approval': self.approval_system.requires_approval(),
            'approval_stats': self.approval_system.get_approval_stats(),
            'safety_status': {
                'daily_loss_used': abs(self.daily_pnl) if self.daily_pnl < 0 else 0,
                'daily_loss_limit': self.safety_limits.max_daily_loss,
                'trades_used': self.daily_trades,
                'trades_limit': self.safety_limits.max_daily_trades
            }
        }
