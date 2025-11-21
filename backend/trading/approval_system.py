import time
from datetime import datetime
from typing import Dict, List
from backend.database.db import db
from backend.utils.logger import logger

class TradeApprovalSystem:
    """
    Manages manual approval for trades during cautious live trading phase.
    First 10 trades require explicit approval, then auto-approves.
    """
    
    def __init__(self, approval_threshold=10):
        self.approval_threshold = approval_threshold
        self.pending_trades = []
        self.approved_count = 0
        
    def requires_approval(self) -> bool:
        """Check if trades still require manual approval."""
        return self.approved_count < self.approval_threshold
    
    def submit_for_approval(self, trade_details: Dict) -> str:
        """Submit a trade for manual approval."""
        trade_id = f"trade_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        approval_request = {
            'trade_id': trade_id,
            'symbol': trade_details['symbol'],
            'side': trade_details['side'],
            'quantity': trade_details['quantity'],
            'estimated_price': trade_details.get('price', 0),
            'estimated_cost': trade_details.get('cost', 0),
            'strategy': trade_details.get('strategy', 'unknown'),
            'status': 'pending',
            'submitted_at': datetime.now().isoformat()
        }
        
        self.pending_trades.append(approval_request)
        
        # Log to database
        db.log_trade_approval(trade_id, approval_request)
        
        logger.info(f"Trade {trade_id} submitted for approval: {trade_details['side']} {trade_details['quantity']} {trade_details['symbol']}")
        
        return trade_id
    
    def approve_trade(self, trade_id: str, approved_by: str = 'user') -> Dict:
        """Approve a pending trade."""
        trade = next((t for t in self.pending_trades if t['trade_id'] == trade_id), None)
        
        if not trade:
            return {'success': False, 'message': 'Trade not found'}
        
        if trade['status'] != 'pending':
            return {'success': False, 'message': f"Trade already {trade['status']}"}
        
        trade['status'] = 'approved'
        trade['approved_at'] = datetime.now().isoformat()
        trade['approved_by'] = approved_by
        
        self.approved_count += 1
        
        # Update in database
        db.update_trade_approval(trade_id, 'approved', approved_by)
        
        logger.info(f"Trade {trade_id} APPROVED by {approved_by} (Count: {self.approved_count}/{self.approval_threshold})")
        
        return {
            'success': True,
            'trade': trade,
            'auto_approve_enabled': not self.requires_approval()
        }
    
    def reject_trade(self, trade_id: str, reason: str = '') -> Dict:
        """Reject a pending trade."""
        trade = next((t for t in self.pending_trades if t['trade_id'] == trade_id), None)
        
        if not trade:
            return {'success': False, 'message': 'Trade not found'}
        
        if trade['status'] != 'pending':
            return {'success': False, 'message': f"Trade already {trade['status']}"}
        
        trade['status'] = 'rejected'
        trade['rejected_at'] = datetime.now().isoformat()
        trade['rejection_reason'] = reason
        
        # Update in database
        db.update_trade_approval(trade_id, 'rejected', reason=reason)
        
        logger.warning(f"Trade {trade_id} REJECTED: {reason}")
        
        return {'success': True, 'trade': trade}
    
    def get_pending_trades(self) -> List[Dict]:
        """Get all trades awaiting approval."""
        return [t for t in self.pending_trades if t['status'] == 'pending']
    
    def get_approval_stats(self) -> Dict:
        """Get approval system statistics."""
        return {
            'approved_count': self.approved_count,
            'approval_threshold': self.approval_threshold,
            'requires_approval': self.requires_approval(),
            'pending_count': len(self.get_pending_trades()),
            'auto_approve_in': max(0, self.approval_threshold - self.approved_count)
        }
