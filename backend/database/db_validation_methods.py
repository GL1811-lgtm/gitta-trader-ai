# Validation Session Database Methods
# Add these methods to the DatabaseManager class in db.py

def create_validation_session(self, session_id, start_time, end_time, num_strategies):
    """Create a new paper trading validation session."""
    conn = self._get_connection()
    conn.execute("""
        INSERT INTO validation_sessions 
        (session_id, start_time, end_time, num_strategies, status)
        VALUES (?, ?, ?, ?, 'active')
    """, (session_id, start_time, end_time, num_strategies))
    conn.commit()
    conn.close()

def log_validation_strategy(self, session_id, strategy_id, dna, initial_fitness):
    """Log a strategy being tested in this session."""
    conn = self._get_connection()
    conn.execute("""
        INSERT INTO validation_strategies
        (session_id, strategy_id, dna, initial_fitness)
        VALUES (?, ?, ?, ?)
    """, (session_id, strategy_id, str(dna), initial_fitness))
    conn.commit()
    conn.close()

def get_validation_session(self, session_id):
    """Get details of a validation session."""
    conn = self._get_connection()
    result = conn.execute("""
        SELECT * FROM validation_sessions WHERE session_id = ?
    """, (session_id,)).fetchone()
    conn.close()
    
    if result:
        return {
            'session_id': result[0],
            'start_time': result[1],
            'end_time': result[2],
            'num_strategies': result[3],
            'status': result[4]
        }
    return None

def update_validation_session(self, session_id, status):
    """Update validation session status."""
    conn = self._get_connection()
    conn.execute("""
        UPDATE validation_sessions SET status = ? WHERE session_id = ?
    """, (status, session_id))
    conn.commit()
    conn.close()

def get_validation_trades(self, session_id):
    """Get all trades for a validation session."""
    # For now, return mock data since we need to add proper trade logging
    # In production, this would query a validation_trades table
    return []

def get_equity_curve(self, session_id):
    """Get equity curve data for drawdown calculation."""
    # Mock equity curve for now
    # In production, track portfolio value over time
    return [100000, 101000, 100500, 102000, 101800, 103000]
