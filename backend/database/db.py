import sqlite3
import os
import json
from datetime import datetime

class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
        self.db_path = os.path.join(self.project_root, 'backend/data/gitta.db')
        self.schema_path = os.path.join(self.project_root, 'backend/database/schema.sql')
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        self._init_db()
        self._initialized = True

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path, timeout=20.0)
        conn.execute('PRAGMA journal_mode=WAL;')
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Initialize the database with the schema."""
        if not os.path.exists(self.schema_path):
            print(f"Schema file not found at {self.schema_path}")
            return

        try:
            with self._get_connection() as conn:
                with open(self.schema_path, 'r') as f:
                    schema = f.read()
                conn.executescript(schema)
                print("Database initialized successfully.")
        except Exception as e:
            print(f"Error initializing database: {e}")

    def log_agent_activity(self, agent_id, activity_type, description, metadata=None):
        """Log agent activity to the database."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO agent_activity_logs (agent_id, activity_type, description, metadata)
                    VALUES (?, ?, ?, ?)
                    """,
                    (agent_id, activity_type, description, json.dumps(metadata) if metadata else None)
                )
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error logging agent activity: {e}")
            return None

    def get_agent_activity_logs(self, agent_id, limit=50):
        """Get recent activity logs for an agent."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT * FROM agent_activity_logs
                    WHERE agent_id = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                    """,
                    (agent_id, limit)
                )
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error fetching agent activity logs: {e}")
            return []

    def insert_strategy(self, source, content, title=None, url=None, verification_data=None, verified=True, confidence_score=100.0, collector_id=None):
        """Insert a new collected strategy with verification data."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Convert verification_data to JSON if provided
                verification_json = json.dumps(verification_data) if verification_data else None
                collected_at = datetime.now().isoformat()
                
                cursor.execute(
                    """
                    INSERT INTO strategies 
                    (source, content, title, url, verification_data, verified, confidence_score, collector_id, collected_at) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        source, 
                        json.dumps(content) if isinstance(content, (dict, list)) else content, 
                        title, 
                        url,
                        verification_json,
                        verified,
                        confidence_score,
                        collector_id,
                        collected_at
                    )
                )
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error inserting strategy: {e}")
            return None

    def insert_test_result(self, strategy_id, agent_name, metrics, recommendation):
        """Insert a test result."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO test_results 
                    (strategy_id, agent_name, win_rate, profit_factor, total_trades, net_profit, sharpe_ratio, recommendation) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        strategy_id, 
                        agent_name, 
                        metrics.get('win_rate'), 
                        metrics.get('profit_factor'), 
                        metrics.get('total_trades'), 
                        metrics.get('net_profit'), 
                        metrics.get('sharpe_ratio'),
                        recommendation
                    )
                )
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error inserting test result: {e}")
            return None

    def insert_daily_report(self, report_date, report_type, content, summary_stats):
        """Insert or update a daily report."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO daily_reports (report_date, type, content, summary_stats) 
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(report_date, type) DO UPDATE SET 
                        content=excluded.content, 
                        summary_stats=excluded.summary_stats,
                        timestamp=CURRENT_TIMESTAMP
                    """,
                    (report_date, report_type, content, json.dumps(summary_stats))
                )
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error inserting daily report: {e}")
            return None

    def get_analytics_performance(self):
        """Get aggregated performance data for analytics."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                # Get average win rate per day (mocking date from timestamp for now as we just started)
                cursor.execute("""
                    SELECT 
                        date(timestamp) as date, 
                        AVG(win_rate) as avg_win_rate,
                        AVG(profit_factor) as avg_profit_factor,
                        SUM(net_profit) as total_profit
                    FROM test_results 
                    GROUP BY date(timestamp)
                    ORDER BY date(timestamp) DESC
                    LIMIT 30
                """)
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error fetching analytics: {e}")
            return []

    def get_learning_history(self):
        """Get history of daily reports/learnings."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, report_date, summary_stats 
                    FROM daily_reports 
                    ORDER BY report_date DESC 
                    LIMIT 50
                """)
                rows = cursor.fetchall()
                history = []
                for row in rows:
                    stats = json.loads(row['summary_stats']) if row['summary_stats'] else {}
                    history.append({
                        'id': row['id'],
                        'date': row['report_date'],
                        'summary': f"Pass Rate: {stats.get('pass_rate', 'N/A')}, Profit: ${stats.get('total_profit', '0')}",
                        'accuracyChange': 0 # Placeholder
                    })
                return history
        except Exception as e:
            print(f"Error fetching learning history: {e}")
            return []

    def save_report(self, report_data):
        """
        Save a report dictionary.
        Expected format: {'date': '...', 'type': '...', 'content': '...'}
        """
        return self.insert_daily_report(
            report_data.get('date'), 
            report_data.get('type'), 
            report_data.get('content'), 
            {}
        )

    def get_report(self, report_date):
        """Fetch a report by date."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT content FROM daily_reports WHERE report_date = ?", (report_date,))
                row = cursor.fetchone()
                return row['content'] if row else None
        except Exception as e:
            print(f"Error fetching report: {e}")
            return None

    def get_latest_report(self, report_type=None):
        """Fetch the content of the latest report, optionally filtered by type."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                if report_type:
                    cursor.execute("SELECT content FROM daily_reports WHERE type = ? ORDER BY report_date DESC LIMIT 1", (report_type,))
                else:
                    cursor.execute("SELECT content FROM daily_reports ORDER BY report_date DESC LIMIT 1")
                
                row = cursor.fetchone()
                return row['content'] if row else None
        except Exception as e:
            print(f"Error fetching latest report: {e}")
            return None

    # --- Phase 18: Paper Trading Methods ---

    def get_account_balance(self):
        """Get current virtual account balance."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT balance FROM virtual_account ORDER BY id DESC LIMIT 1")
                row = cursor.fetchone()
                if row:
                    return row['balance']
                else:
                    # Initialize account if not exists
                    cursor.execute("INSERT INTO virtual_account (balance) VALUES (100000.0)")
                    conn.commit()
                    return 100000.0
        except Exception as e:
            print(f"Error getting balance: {e}")
            return 0.0

    def update_balance(self, amount_change):
        """Update account balance (positive for credit, negative for debit)."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                current_balance = self.get_account_balance()
                new_balance = current_balance + amount_change
                cursor.execute("UPDATE virtual_account SET balance = ?, updated_at = CURRENT_TIMESTAMP WHERE id = (SELECT id FROM virtual_account ORDER BY id DESC LIMIT 1)", (new_balance,))
                conn.commit()
                return new_balance
        except Exception as e:
            print(f"Error updating balance: {e}")
            return None

    def get_portfolio(self):
        """Get all open positions."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT symbol, quantity, avg_price FROM portfolio WHERE quantity > 0")
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error fetching portfolio: {e}")
            return []

    def update_portfolio(self, symbol, quantity_change, price):
        """Update portfolio position after a trade."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                # Check existing position
                cursor.execute("SELECT quantity, avg_price FROM portfolio WHERE symbol = ?", (symbol,))
                row = cursor.fetchone()
                
                if row:
                    old_qty = row['quantity']
                    old_avg = row['avg_price']
                    new_qty = old_qty + quantity_change
                    
                    if new_qty == 0:
                        # Position closed
                        cursor.execute("DELETE FROM portfolio WHERE symbol = ?", (symbol,))
                    else:
                        # Calculate new average price (only on BUY)
                        if quantity_change > 0:
                            total_cost = (old_qty * old_avg) + (quantity_change * price)
                            new_avg = total_cost / new_qty
                        else:
                            new_avg = old_avg # Avg price doesn't change on sell
                        
                        cursor.execute("UPDATE portfolio SET quantity = ?, avg_price = ?, last_updated = CURRENT_TIMESTAMP WHERE symbol = ?", (new_qty, new_avg, symbol))
                else:
                    # New position
                    if quantity_change > 0:
                        cursor.execute("INSERT INTO portfolio (symbol, quantity, avg_price) VALUES (?, ?, ?)", (symbol, quantity_change, price))
                    else:
                        raise ValueError("Cannot sell stock not in portfolio")
                
                conn.commit()
                return True
        except Exception as e:
            print(f"Error updating portfolio: {e}")
            return False

    def add_transaction(self, symbol, type, quantity, price):
        """Record a transaction."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                total_value = quantity * price
                cursor.execute(
                    "INSERT INTO transactions (symbol, type, quantity, price, total_value) VALUES (?, ?, ?, ?, ?)",
                    (symbol, type, quantity, price, total_value)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error adding transaction: {e}")
            return False

    # --- Phase 5: Agent Detail View Methods ---

    def get_agent_statistics(self, collector_id):
        """Get performance statistics for a specific collector agent."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Total collected
                cursor.execute(
                    "SELECT COUNT(*) as total FROM strategies WHERE collector_id = ?",
                    (collector_id,)
                )
                total = cursor.fetchone()['total'] or 0
                
                # Success rate (verified strategies)
                cursor.execute(
                    "SELECT COUNT(*) as verified FROM strategies WHERE collector_id = ? AND verified = 1",
                    (collector_id,)
                )
                verified = cursor.fetchone()['verified'] or 0
                success_rate = (verified / total * 100) if total > 0 else 0
                
                # Average quality score
                cursor.execute(
                    "SELECT AVG(confidence_score) as avg_quality FROM strategies WHERE collector_id = ?",
                    (collector_id,)
                )
                avg_quality = cursor.fetchone()['avg_quality'] or 0
                
                return {
                    "total_collected": total,
                    "success_rate": round(success_rate, 1),
                    "avg_quality_score": round(avg_quality, 1),
                    "uptime_percentage": 99.8  # Mock for now
                }
        except Exception as e:
            print(f"Error fetching agent statistics: {e}")
            return {}

    def get_agent_collections(self, collector_id, limit=20):
        """Get recent collections by a specific agent."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT id, title, source, url, confidence_score, verified, collected_at
                    FROM strategies
                    WHERE collector_id = ?
                    ORDER BY collected_at DESC
                    LIMIT ?
                    """,
                    (collector_id, limit)
                )
                rows = cursor.fetchall()
                collections = []
                for row in rows:
                    collections.append({
                        "id": row['id'],
                        "strategy_name": row['title'] or f"Strategy #{row['id']}",
                        "source_url": row['url'],
                        "source": row['source'],
                        "collected_at": row['collected_at'],
                        "quality_score": row['confidence_score'],
                        "verification_status": "approved" if row['verified'] else "rejected",
                        "confidence": row['confidence_score']
                    })
                return collections
        except Exception as e:
            print(f"Error fetching agent collections: {e}")
            return []

    def get_agent_verification_breakdown(self, collector_id):
        """Get multi-AI verification breakdown for an agent's collections."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Count by verification status
                cursor.execute(
                    """
                    SELECT 
                        SUM(CASE WHEN verified = 1 AND confidence_score >= 80 THEN 1 ELSE 0 END) as approved,
                        SUM(CASE WHEN verified = 1 AND confidence_score < 80 THEN 1 ELSE 0 END) as warning,
                        SUM(CASE WHEN verified = 0 THEN 1 ELSE 0 END) as rejected,
                        AVG(confidence_score) as avg_confidence
                    FROM strategies
                    WHERE collector_id = ?
                    """,
                    (collector_id,)
                )
                row = cursor.fetchone()
                return {
                    "approved": row['approved'] or 0,
                    "warning": row['warning'] or 0,
                    "rejected": row['rejected'] or 0,
                    "avg_confidence": round(row['avg_confidence'] or 0, 1)
                }
        except Exception as e:
            print(f"Error fetching verification breakdown: {e}")
            return {}

    def get_agent_graph_data(self, collector_id):
        """Get additional data for agent detail graphs."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # 1. Source Breakdown
                cursor.execute(
                    """
                    SELECT source, COUNT(*) as count
                    FROM strategies
                    WHERE collector_id = ?
                    GROUP BY source
                    """,
                    (collector_id,)
                )
                source_rows = cursor.fetchall()
                total_source = sum(r['count'] for r in source_rows)
                source_breakdown = [
                    {"source": r['source'], "count": r['count'], "percentage": round((r['count'] / total_source * 100), 1) if total_source > 0 else 0}
                    for r in source_rows
                ]
                
                # 2. Quality Distribution
                cursor.execute(
                    """
                    SELECT confidence_score
                    FROM strategies
                    WHERE collector_id = ?
                    """,
                    (collector_id,)
                )
                scores = [r['confidence_score'] for r in cursor.fetchall()]
                quality_dist = [
                    {"range": "90-100%", "count": len([s for s in scores if 90 <= s <= 100])},
                    {"range": "80-89%", "count": len([s for s in scores if 80 <= s < 90])},
                    {"range": "70-79%", "count": len([s for s in scores if 70 <= s < 80])},
                    {"range": "60-69%", "count": len([s for s in scores if 60 <= s < 70])},
                    {"range": "<60%", "count": len([s for s in scores if s < 60])}
                ]
                
                # 3. Performance Metrics (Calculated)
                # Speed: Mocked based on collection count (more is faster)
                # Accuracy: Avg confidence
                # Reliability: Success rate
                # Efficiency: Mocked
                # Coverage: Mocked
                
                cursor.execute("SELECT COUNT(*) as total, AVG(confidence_score) as avg_conf FROM strategies WHERE collector_id = ?", (collector_id,))
                perf_row = cursor.fetchone()
                total = perf_row['total'] or 0
                avg_conf = perf_row['avg_conf'] or 0
                
                performance_metrics = {
                    "speed": min(100, 50 + (total * 2)), # Mock logic
                    "accuracy": round(avg_conf, 1),
                    "reliability": 95, # Mock
                    "efficiency": 85, # Mock
                    "coverage": min(100, total * 5) # Mock
                }
                
                return {
                    "sourceBreakdown": source_breakdown,
                    "qualityDistribution": quality_dist,
                    "performanceMetrics": performance_metrics
                }
        except Exception as e:
            print(f"Error fetching graph data: {e}")
            return {
                "sourceBreakdown": [],
                "qualityDistribution": [],
                "performanceMetrics": {}
            }

    # --- Phase 2: Tester Agent Methods ---

    def get_untested_strategies(self, limit=5):
        """Get strategies that haven't been fully tested yet."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                # For now, just get latest strategies. 
                # In a real system, we'd join with test_results to exclude already tested ones.
                cursor.execute(
                    "SELECT * FROM strategies ORDER BY timestamp DESC LIMIT ?",
                    (limit,)
                )
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error fetching untested strategies: {e}")
            return []

    def save_test_result(self, strategy_id, agent_name, win_rate, profit_factor, total_trades, net_profit, sharpe_ratio, recommendation):
        """Save a simulation result."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO test_results 
                    (strategy_id, agent_name, win_rate, profit_factor, total_trades, net_profit, sharpe_ratio, recommendation)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (strategy_id, agent_name, win_rate, profit_factor, total_trades, net_profit, sharpe_ratio, recommendation)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error saving test result: {e}")
            return False

    def get_agent_timeline(self, collector_id, days=30):
        """Get daily collection counts for timeline chart."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT 
                        DATE(collected_at) as date,
                        COUNT(*) as count
                    FROM strategies
                    WHERE collector_id = ?
                    AND collected_at >= DATE('now', ? || ' days')
                    GROUP BY DATE(collected_at)
                    ORDER BY date DESC
                    """,
                    (collector_id, -days)
                )
                rows = cursor.fetchall()
                return [{"date": row['date'], "count": row['count']} for row in rows]
        except Exception as e:
            print(f"Error fetching agent timeline: {e}")
            return []

    def get_strategies(self):
        """Get all strategies."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM strategies")
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error fetching strategies: {e}")
            return []

    def get_tester_statistics(self, agent_name):
        """Get aggregated statistics for a tester agent."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT 
                        COUNT(*) as total_tests,
                        AVG(win_rate) as avg_win_rate,
                        AVG(profit_factor) as avg_profit_factor,
                        AVG(net_profit) as avg_net_profit,
                        SUM(CASE WHEN recommendation = 'PASS' THEN 1 ELSE 0 END) as passed_tests
                    FROM test_results
                    WHERE agent_name = ?
                    """,
                    (agent_name,)
                )
                row = cursor.fetchone()
                
                total = row['total_tests'] or 0
                passed = row['passed_tests'] or 0
                
                return {
                    "total_tests": total,
                    "avg_win_rate": round(row['avg_win_rate'] or 0, 2),
                    "avg_profit_factor": round(row['avg_profit_factor'] or 0, 2),
                    "avg_net_profit": round(row['avg_net_profit'] or 0, 2),
                    "pass_rate": round((passed / total * 100), 1) if total > 0 else 0
                }
        except Exception as e:
            print(f"Error fetching tester stats: {e}")
            return {}

    def get_tester_results(self, agent_name, limit=20):
        """Get recent test results for a tester."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT tr.*, s.title as strategy_name, s.source
                    FROM test_results tr
                    JOIN strategies s ON tr.strategy_id = s.id
                    WHERE tr.agent_name = ?
                    ORDER BY tr.timestamp DESC
                    LIMIT ?
                    """,
                    (agent_name, limit)
                )
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error fetching tester results: {e}")
            return []

    def get_tester_graph_data(self, agent_name):
        """Get graph data for tester agent."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # 1. Performance Metrics (Radar)
                stats = self.get_tester_statistics(agent_name)
                performance_metrics = {
                    "Win Rate": stats.get('avg_win_rate', 0),
                    "Profit Factor": min(100, stats.get('avg_profit_factor', 0) * 20), # Scale for chart
                    "Pass Rate": stats.get('pass_rate', 0),
                    "Activity": min(100, stats.get('total_tests', 0) * 2), # Mock scale
                    "Profitability": min(100, max(0, stats.get('avg_net_profit', 0) / 10)) # Mock scale
                }
                
                # 2. Profit Distribution (Bar Chart)
                cursor.execute(
                    """
                    SELECT net_profit
                    FROM test_results
                    WHERE agent_name = ?
                    """,
                    (agent_name,)
                )
                profits = [r['net_profit'] for r in cursor.fetchall()]
                profit_dist = [
                    {"range": "> $1000", "count": len([p for p in profits if p > 1000])},
                    {"range": "$500-$1000", "count": len([p for p in profits if 500 < p <= 1000])},
                    {"range": "$0-$500", "count": len([p for p in profits if 0 < p <= 500])},
                    {"range": "Loss", "count": len([p for p in profits if p <= 0])}
                ]
                
                return {
                    "performanceMetrics": performance_metrics,
                    "profitDistribution": profit_dist
                }
        except Exception as e:
            print(f"Error fetching tester graph data: {e}")
            return {}

    # --- Phase 1: Master AI V2.0 Methods ---

    def log_evolution(self, generation, best_fitness, avg_fitness, worst_fitness, population_size):
        """Log evolution generation stats."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO evolution_history 
                    (generation, best_fitness, avg_fitness, worst_fitness, population_size)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (generation, best_fitness, avg_fitness, worst_fitness, population_size)
                )
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error logging evolution: {e}")
            return None

    def log_code_modification(self, file_path, modification_type, description, previous_code_hash, new_code_hash, status='PENDING'):
        """Log AI code modification."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO code_modifications 
                    (file_path, modification_type, description, previous_code_hash, new_code_hash, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (file_path, modification_type, description, previous_code_hash, new_code_hash, status)
                )
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error logging code modification: {e}")
            return None

    def log_system_health(self, metric_name, metric_value, status):
        """Log system health metric."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO system_health (metric_name, metric_value, status)
                    VALUES (?, ?, ?)
                    """,
                    (metric_name, metric_value, status)
                )
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error logging system health: {e}")
            return None

    def save_market_data(self, symbol, timestamp, open_price, high, low, close, volume, timeframe='1m'):
        """Save market data."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO market_data 
                    (symbol, timestamp, open, high, low, close, volume, timeframe)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (symbol, timestamp, open_price, high, low, close, volume, timeframe)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error saving market data: {e}")
            return False

    def get_latest_market_data(self, symbol):
        """Get latest market data for a symbol."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT * FROM market_data 
                    WHERE symbol = ? 
                    ORDER BY timestamp DESC 
                    LIMIT 1
                    """,
                    (symbol,)
                )
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"Error fetching market data: {e}")
            return None
    
    # ===== Validation Session Methods =====
    
    def create_validation_session(self, session_id, start_time, end_time, num_strategies):
        """Create a new paper trading validation session."""
        conn = self._get_connection()
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS validation_sessions (
                    session_id TEXT PRIMARY KEY,
                    start_time TEXT,
                    end_time TEXT,
                    num_strategies INTEGER,
                    status TEXT DEFAULT 'active'
                )
            """)
            conn.execute("""
                INSERT INTO validation_sessions 
                (session_id, start_time, end_time, num_strategies, status)
                VALUES (?, ?, ?, ?, 'active')
            """, (session_id, start_time, end_time, num_strategies))
            conn.commit()
        finally:
            conn.close()

    def log_validation_strategy(self, session_id, strategy_id, dna, initial_fitness):
        """Log a strategy being tested in this session."""
        conn = self._get_connection()
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS validation_strategies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    strategy_id TEXT,
                    dna TEXT,
                    initial_fitness REAL
                )
            """)
            conn.execute("""
                INSERT INTO validation_strategies
                (session_id, strategy_id, dna, initial_fitness)
                VALUES (?, ?, ?, ?)
            """, (session_id, strategy_id, str(dna), initial_fitness))
            conn.commit()
        finally:
            conn.close()

    def get_validation_session(self, session_id):
        """Get details of a validation session."""
        conn = self._get_connection()
        try:
            result = conn.execute("""
                SELECT * FROM validation_sessions WHERE session_id = ?
            """, (session_id,)).fetchone()
            
            if result:
                return {
                    'session_id': result[0],
                    'start_time': result[1],
                    'end_time': result[2],
                    'num_strategies': result[3],
                    'status': result[4]
                }
            return None
        finally:
            conn.close()

    def update_validation_session(self, session_id, status):
        """Update validation session status."""
        conn = self._get_connection()
        try:
            conn.execute("""
                UPDATE validation_sessions SET status = ? WHERE session_id = ?
            """, (status, session_id))
            conn.commit()
        finally:
            conn.close()

    def get_validation_trades(self, session_id):
        """Get all trades for a validation session."""
        # Mock data for now - in production would query validation_trades table
        return []

    def get_equity_curve(self, session_id):
        """Get equity curve data for drawdown calculation."""
        # Mock equity curve for demonstration
        return [100000, 101000, 100500, 102000, 101800, 103000]
    
    # ===== Trade Approval Methods =====
    
    def log_trade_approval(self, trade_id, approval_data):
        """Log a trade approval request."""
        conn = self._get_connection()
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS trade_approvals (
                    trade_id TEXT PRIMARY KEY,
                    symbol TEXT,
                    side TEXT,
                    quantity INTEGER,
                    estimated_price REAL,
                    status TEXT,
                    submitted_at TEXT
                )
            """)
            conn.execute("""
                INSERT INTO trade_approvals
                (trade_id, symbol, side, quantity, estimated_price, status, submitted_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (trade_id, approval_data['symbol'], approval_data['side'],
                  approval_data['quantity'], approval_data.get('estimated_price', 0),
                  approval_data['status'], approval_data['submitted_at']))
            conn.commit()
        finally:
            conn.close()
    
    def update_trade_approval(self, trade_id, status, approved_by=None, reason=None):
        """Update trade approval status."""
        conn = self._get_connection()
        try:
            if status == 'approved':
                conn.execute("""
                    UPDATE trade_approvals 
                    SET status = ?, approved_by = ?, approved_at = ?
                    WHERE trade_id = ?
                """, (status, approved_by, datetime.now().isoformat(), trade_id))
            else:
                conn.execute("""
                    UPDATE trade_approvals 
                    SET status = ?, rejection_reason = ?
                    WHERE trade_id = ?
                """, (status, reason, trade_id))
            conn.commit()
        finally:
            conn.close()

    # ===== Database Optimization Methods =====
    
    def create_indexes(self):
        """Create indexes for frequently queried columns."""
        conn = self._get_connection()
        try:
            # Index on trades table
            conn.execute("CREATE INDEX IF NOT EXISTS idx_trades_timestamp ON trades(timestamp)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_trades_symbol ON trades(symbol)")
            
            # Index on market_data table
            conn.execute("CREATE INDEX IF NOT EXISTS idx_market_data_symbol ON market_data(symbol)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_market_data_timestamp ON market_data(timestamp)")
            
            # Index on strategies table
            conn.execute("CREATE INDEX IF NOT EXISTS idx_strategies_status ON strategies(status)")
            
            # Index on evolution_history table
            conn.execute("CREATE INDEX IF NOT EXISTS idx_evolution_generation ON evolution_history(generation)")
            
            conn.commit()
            logger.info("Database indexes created successfully")
        except Exception as e:
            logger.error(f"Error creating indexes: {e}")
        finally:
            conn.close()
    
    def vacuum_database(self):
        """Optimize database by vacuuming (reclaim space and optimize)."""
        try:
            conn = self._get_connection()
            conn.execute("VACUUM")
            conn.execute("ANALYZE")
            conn.close()
            logger.info("Database vacuumed and analyzed")
        except Exception as e:
            logger.error(f"Error vacuuming database: {e}")
    
    def get_db_stats(self) -> Dict:
        """Get database statistics."""
        conn = self._get_connection()
        try:
            # Get table counts
            tables = ['trades', 'portfolio', 'strategies', 'market_data', 'evolution_history']
            stats = {}
            
            for table in tables:
                try:
                    result = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
                    stats[f"{table}_count"] = result[0] if result else 0
                except:
                    stats[f"{table}_count"] = 0
            
            # Database size
            import os
            if os.path.exists(self.db_path):
                stats['db_size_mb'] = round(os.path.getsize(self.db_path) / (1024 * 1024), 2)
            else:
                stats['db_size_mb'] = 0
            
            return stats
        finally:
            conn.close()

# Global instance

db = DatabaseManager()
