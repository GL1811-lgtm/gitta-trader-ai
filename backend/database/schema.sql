-- Schema for Gitta Trader AI SQLite Database

CREATE TABLE IF NOT EXISTS strategies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL, -- e.g., 'YouTube', 'Reddit', 'News'
    title TEXT,
    content TEXT NOT NULL, -- JSON or text content of the strategy
    url TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'new', -- 'new', 'tested', 'archived'
    verification_data TEXT,  -- JSON field for multi-AI verification results
    verified BOOLEAN DEFAULT 1,  -- Whether strategy passed verification
    confidence_score REAL DEFAULT 100.0,  -- Verification confidence score
    collector_id TEXT,  -- ID of the collector agent
    collected_at DATETIME  -- When the strategy was collected
);

CREATE TABLE IF NOT EXISTS test_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    strategy_id INTEGER,
    agent_name TEXT NOT NULL,
    win_rate REAL,
    profit_factor REAL,
    total_trades INTEGER,
    net_profit REAL,
    sharpe_ratio REAL,
    recommendation TEXT, -- 'PASS', 'FAIL'
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (strategy_id) REFERENCES strategies (id)
);

CREATE TABLE IF NOT EXISTS daily_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_date DATE NOT NULL,
    type TEXT NOT NULL, -- 'MORNING' or 'EVENING'
    content TEXT NOT NULL, -- Markdown content
    summary_stats TEXT, -- JSON string of aggregated stats
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(report_date, type)
);

CREATE TABLE IF NOT EXISTS system_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    level TEXT NOT NULL, -- 'INFO', 'ERROR', 'WARNING'
    agent_id TEXT,
    message TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS agent_activity_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id TEXT NOT NULL,
    activity_type TEXT NOT NULL, -- 'INFO', 'ERROR', 'COLLECTION', 'VERIFICATION'
    description TEXT,
    metadata TEXT, -- JSON for extra details
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Phase 18: Paper Trading Tables

CREATE TABLE IF NOT EXISTS virtual_account (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    balance REAL DEFAULT 100000.0, -- Initial capital ₹1,00,000
    currency TEXT DEFAULT 'INR',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS portfolio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL UNIQUE,
    quantity INTEGER DEFAULT 0,
    avg_price REAL DEFAULT 0.0,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    type TEXT NOT NULL, -- 'BUY' or 'SELL'
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    total_value REAL NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Phase 1: Master AI V2.0 Tables

CREATE TABLE IF NOT EXISTS evolution_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    generation INTEGER NOT NULL,
    best_fitness REAL,
    avg_fitness REAL,
    worst_fitness REAL,
    population_size INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS code_modifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_path TEXT NOT NULL,
    modification_type TEXT, -- 'FIX', 'OPTIMIZATION', 'FEATURE'
    description TEXT,
    previous_code_hash TEXT,
    new_code_hash TEXT,
    status TEXT DEFAULT 'PENDING', -- 'PENDING', 'APPROVED', 'REJECTED', 'ROLLED_BACK'
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS system_health (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metric_name TEXT NOT NULL,
    metric_value REAL,
    status TEXT, -- 'OK', 'WARNING', 'CRITICAL'
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS order_book_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    bid_depth TEXT, -- JSON
    ask_depth TEXT, -- JSON
    imbalance REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS performance_analytics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    period_type TEXT, -- 'DAILY', 'WEEKLY', 'MONTHLY'
    period_start DATETIME,
    period_end DATETIME,
    total_return REAL,
    win_rate REAL,
    sharpe_ratio REAL,
    max_drawdown REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS market_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    timestamp DATETIME NOT NULL,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume INTEGER,
    timeframe TEXT DEFAULT '1m',
    UNIQUE(symbol, timestamp, timeframe)
);
