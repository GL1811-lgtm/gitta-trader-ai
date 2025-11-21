import { Alert, MarketIndex, LearningLogEntry, ChartDataPoint, AgentDetail, AgentType } from '../types';

export const MOCK_ALERTS: Alert[] = [
  { id: '1', instrument: 'NIFTY 23500 CE', type: 'BUY', confidence: 85, reason: 'Strong bullish momentum, RSI above 70.', timestamp: '10:45 AM', strikePrice: 120.50, targetPrice: 150.00, stopLoss: 105.00 },
  { id: '2', instrument: 'BANKNIFTY 51200 PE', type: 'BUY', confidence: 78, reason: 'Breaking key support level, high volume.', timestamp: '11:15 AM', strikePrice: 210.00, targetPrice: 280.00, stopLoss: 180.00 },
  { id: '3', instrument: 'RELIANCE 2900 CE', type: 'SELL', confidence: 65, reason: 'Reached resistance, bearish divergence forming.', timestamp: '01:20 PM', strikePrice: 85.30, targetPrice: 60.00, stopLoss: 95.00 },
  { id: '4', instrument: 'NIFTY 23300 PE', type: 'BUY', confidence: 92, reason: 'Market sentiment shift, VIX spike expected.', timestamp: '02:05 PM', strikePrice: 95.75, targetPrice: 140.00, stopLoss: 80.00 },
];



export const MOCK_LEARNING_LOGS: LearningLogEntry[] = [
  { id: '1', timestamp: '2024-07-20', title: 'Volatility Model Update', summary: 'Improved prediction accuracy in high VIX environments by integrating GARCH model outputs. Model now better anticipates sharp reversals.', accuracyChange: 1.2 },
  { id: '2', timestamp: '2024-07-19', title: 'Pattern Recognition Enhancement', summary: 'Added recognition for "cup and handle" pattern. Backtesting shows a 72% success rate on signals generated from this pattern.', accuracyChange: 0.8 },
  { id: '3', timestamp: '2024-07-18', title: 'Sentiment Analysis Integration', summary: 'AI now processes real-time news sentiment. Confidence scores are adjusted based on positive/negative news flow for underlying stocks.', accuracyChange: 1.5 },
];

export const MOCK_CHART_DATA: ChartDataPoint[] = Array.from({ length: 50 }, (_, i) => ({
  time: `10:${i < 10 ? '0' : ''}${i}`,
  open: 23400 + Math.random() * 20 - 10,
  high: 23410 + Math.random() * 25,
  low: 23390 - Math.random() * 25,
  close: 23405 + Math.random() * 30 - 15,
}));


const createAgents = (type: AgentType, count: number, namePrefix: string, idPrefix: string): AgentDetail[] => {
  return Array.from({ length: count }, (_, i) => ({
    id: `${idPrefix}_${i + 1}`,
    name: `${namePrefix}-${String(i + 1).padStart(2, '0')}`,
    type,
    status: 'Online',
    activity: 'Initializing...',
    cpu: Math.random() * 20,
    memory: Math.random() * 30,
  }));
};

export const INITIAL_AGENT_DETAILS: AgentDetail[] = [
  ...createAgents('Collector', 10, 'Collector', 'agent'),
  ...createAgents('Tester', 10, 'Tester', 'tester'),
  ...createAgents('Supervisor', 1, 'Supervisor', 'supervisor'),
  ...createAgents('Expert', 1, 'Expert', 'expert'),
];


export const MOCK_AGENT_ACTIVITIES: Record<AgentType, string[]> = {
  Collector: [
    'Scanning news feeds for NIFTY 50...',
    'Ingesting 1-min tick data from NSE...',
    'Analyzing social media sentiment for BANKNIFTY...',
    'Parsing options chain data for RELIANCE.NS...',
    'Archiving historical volume data...',
    'Monitoring FII/DII flow...',
    'Scraping YouTube for new strategies...',
    'Checking for unusual options activity...',
    'Fetching global market indices...',
    'Processing corporate announcements...'
  ],
  Tester: [
    'Backtesting Strategy #A4B on INFY.NS...',
    'Simulating trades on NIFTY 15m chart...',
    'Running risk analysis model for high VIX...',
    'Evaluating performance metrics of v2.3 model...',
    'Comparing LSTM vs. Transformer model output...',
    'Paper trading BANKNIFTY options...',
    'Stress testing portfolio allocation...',
    'Validating collector data integrity...',
    'Analyzing slippage on simulated trades...',
    'Generating P&L report for strategy #C12...'
  ],
  Supervisor: [
    'All systems nominal. Agent health at 99.8%.',
    'Monitoring agent swarm health...',
    'Verifying data integrity across all collectors...',
    'Optimizing resource allocation for testers...',
    'Restarting idle agent Collector-07...',
    'Compiling agent performance metrics...',
    'Checking for API rate limits...',
    'Running diagnostics on Expert agent...',
    'Data pipeline throughput normal.',
    'No errors detected in the last cycle.'
  ],
  Expert: [
    'Awaiting end-of-day data for report generation.',
    'Compiling daily performance report.',
    'Identifying new market patterns from aggregated data.',
    'Initiating model retraining cycle v2.4...',
    'Generating learning summary for the day.',
    'Analyzing tester agent results for strategy #B8F.',
    'Reviewing collector sentiment data against price action.',
    'Preparing insights for tomorrow morning.',
    'Correlating global events with local market impact.',
    'Model convergence achieved.'
  ]
};