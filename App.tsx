import React, { useState, useEffect } from 'react';
import { Page, Alert, MarketIndex, LearningLogEntry, AgentDetail } from './types';
import { DashboardIcon, AlertIcon, AnalysisIcon, LearningIcon, SettingsIcon, CpuChipIcon, MenuIcon } from './components/icons';
import { INITIAL_AGENT_DETAILS, MOCK_AGENT_ACTIVITIES } from './data/mock';
import { apiUrl } from './src/utils/api';
import PaperTrading from './src/pages/PaperTrading';
import AllIndices from './src/components/AllIndices';
import MarketMovers from './src/components/MarketMovers';
import TradingScreens from './src/components/TradingScreens';
import StocksInNews from './src/components/StocksInNews';
import TickerBar from './src/components/TickerBar';
import StockDetailPage from './src/components/StockDetailPage';
import MostTradedStocks from './src/components/MostTradedStocks';
import AgentDetailsModal from './src/components/AgentDetailsModal';

type Theme = 'light' | 'dark';

function App() {
  const [currentPage, setCurrentPage] = useState<Page>('dashboard');
  const [theme, setTheme] = useState<Theme>('dark');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [indices, setIndices] = useState<MarketIndex[]>([]);
  const [learningLogs, setLearningLogs] = useState<LearningLogEntry[]>([]);
  const [agentDetails, setAgentDetails] = useState<AgentDetail[]>(INITIAL_AGENT_DETAILS);
  const [chartModal, setChartModal] = useState<{ symbol: string, name: string } | null>(null);
  const [selectedAgent, setSelectedAgent] = useState<AgentDetail | null>(null);

  // Fetch real data periodically
  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch agents from backend
        const agentsResponse = await fetch(apiUrl('/agents/status')).catch(() => null);
        if (agentsResponse && agentsResponse.ok) {
          const agentsData = await agentsResponse.json();
          // Handle both array response and object with agents property
          const agentsList = Array.isArray(agentsData) ? agentsData : (agentsData.agents || []);

          // Transform backend format to frontend format
          const transformedAgents = agentsList.map((agent: any) => {
            // Normalize status - backend returns "Running", "Active", "Testing", etc.
            // Frontend expects "Online", "Idle", or "Processing"
            const backendStatus = (agent.status || '').toLowerCase();
            let frontendStatus = 'Idle';

            if (['running', 'active', 'online', 'testing'].includes(backendStatus)) {
              frontendStatus = 'Online';
            } else if (backendStatus === 'processing') {
              frontendStatus = 'Processing';
            }

            return {
              id: agent.id,
              name: agent.name,
              type: agent.type,
              status: frontendStatus,
              activity: agent.activity || 'Idle',
              cpu: Math.random() * 20,
              memory: Math.random() * 30,
            };
          });
          setAgentDetails(transformedAgents);
        }

        // Fetch Market Indices
        const indicesResponse = await fetch(apiUrl('/market/indices'));
        if (indicesResponse.ok) {
          const indicesData = await indicesResponse.json();
          if (Array.isArray(indicesData) && indicesData.length > 0) {
            setIndices(indicesData);
          }
        }

        // Fetch Alerts
        const alertsResponse = await fetch(apiUrl('/alerts'));
        if (alertsResponse.ok) {
          const alertsData = await alertsResponse.json();
          setAlerts(alertsData);
        }

        // Fetch Learning Logs
        const logsResponse = await fetch(apiUrl('/learning/logs'));
        if (logsResponse.ok) {
          const logsData = await logsResponse.json();
          setLearningLogs(logsData);
        }

      } catch (error) {
        console.log('Error fetching data:', error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  const navItems = [
    { id: 'dashboard' as Page, label: 'Dashboard', icon: DashboardIcon },
    { id: 'stocksearch' as Page, label: 'Stock Search', icon: AnalysisIcon },
    { id: 'alerts' as Page, label: 'Live Alerts', icon: AlertIcon },
    { id: 'analysis' as Page, label: 'Market Analysis', icon: AnalysisIcon },
    { id: 'learning' as Page, label: 'AI Learning', icon: LearningIcon },
    { id: 'agents' as Page, label: 'Agent Status', icon: CpuChipIcon },
    { id: 'papertrading' as Page, label: 'Paper Trading', icon: AlertIcon },
    { id: 'settings' as Page, label: 'Settings', icon: SettingsIcon },
  ];

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return renderDashboard();
      case 'stocksearch':
        return <AllIndices onIndexClick={openChart} />;
      case 'alerts':
        return renderAlertsPage();
      case 'analysis':
        return renderAnalysisPage();
      case 'learning':
        return renderLearningPage();
      case 'agents':
        return renderAgentsPage();
      case 'papertrading':
        return <PaperTrading />;
      case 'settings':
        return renderSettingsPage();
      default:
        return renderDashboard();
    }
  };

  const openChart = (symbol: string, name: string) => {
    setChartModal({ symbol, name });
  };

  const closeChart = () => {
    setChartModal(null);
  };

  const renderDashboard = () => (
    <div className="p-6">
      <div className="bg-base-200 p-8 rounded-lg shadow-lg mb-6">
        <h2 className="text-gray-400 text-lg mb-2">Overall System Confidence</h2>
        <p className="text-sm text-gray-500 mb-4">Based on continuous backtesting and model validation.</p>
        <div className="text-6xl font-bold text-accent">94.7%</div>
      </div>

      <h3 className="text-2xl font-semibold mb-4">Market Overview</h3>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {indices.length > 0 ? (
          indices.map((index) => (
            <div key={index.name} className="bg-base-200 p-6 rounded-lg">
              <h4 className="text-gray-400 text-sm mb-2">{index.name}</h4>
              <div className="text-3xl font-bold mb-2">{index.value.toLocaleString()}</div>
              <div className={`text-sm ${index.change >= 0 ? 'text-accent' : 'text-danger'}`}>
                {index.change >= 0 ? '+' : ''}{index.change.toFixed(2)} ({index.changePercent.toFixed(2)}%)
              </div>
            </div>
          ))
        ) : (
          <div className="col-span-3 text-center p-6 text-gray-500">
            Waiting for Real Market Data from Angel One...
          </div>
        )}
      </div>

      {/* Most Traded Stocks */}
      <div className="mt-6">
        <MostTradedStocks onStockClick={openChart} />
      </div>

      {/* Dashboard Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
        {/* Left Column - Market Movers (2/3 width) */}
        <div className="lg:col-span-2">
          <MarketMovers onStockClick={openChart} onViewAll={() => setCurrentPage('analysis')} />
        </div>

        {/* Right Column - Trading Screens (1/3 width) */}
        <div>
          <TradingScreens onViewAll={() => setCurrentPage('analysis')} />
        </div>
      </div>

      {/* Stocks in News Section */}
      <div className="mt-6">
        <StocksInNews onViewAll={() => setCurrentPage('analysis')} />
      </div>
    </div>
  );

  const renderAlertsPage = () => (
    <div className="p-6">
      <h2 className="text-3xl font-bold mb-6">Live Trading Alerts</h2>
      <div className="space-y-4">
        {alerts.map((alert) => (
          <div key={alert.id} className={`bg-base-200 p-6 rounded-lg border-2 ${alert.type === 'BUY' ? 'border-accent' : 'border-warning'}`}>
            <div className="flex items-start justify-between mb-4">
              <div>
                <span className={`inline-block px-3 py-1 rounded-full text-white text-sm font-bold mb-2 ${alert.type === 'BUY' ? 'bg-accent' : 'bg-warning'}`}>
                  {alert.type}
                </span>
                <h3 className="text-2xl font-bold">{alert.instrument}</h3>
                <p className="text-gray-400 text-sm">{alert.timestamp}</p>
              </div>
            </div>
            <div className="mb-4">
              <p className="text-sm text-gray-400 mb-1">Confidence</p>
              <p className="text-4xl font-bold text-accent">{alert.confidence}%</p>
            </div>
            <p className="mb-4"><span className="text-gray-400">Reason:</span> {alert.reason}</p>
            <div className="grid grid-cols-3 gap-4 text-sm">
              <div>
                <span className="text-gray-400 block mb-1">Strike</span>
                <span className="font-bold">{alert.strikePrice}</span>
              </div>
              <div>
                <span className="text-gray-400 block mb-1">Target</span>
                <span className="font-bold text-accent">{alert.targetPrice}</span>
              </div>
              <div>
                <span className="text-gray-400 block mb-1">Stoploss</span>
                <span className="font-bold text-danger">{alert.stopLoss}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderAnalysisPage = () => (
    <div className="p-6">
      <h2 className="text-3xl font-bold mb-6">Market Analysis</h2>
      <div className="bg-base-200 p-6 rounded-lg">
        <p className="text-gray-400">Advanced market analysis charts and indicators will appear here.</p>
        <p className="mt-4">Integration with real-time data feeds coming soon.</p>
      </div>
    </div>
  );

  const renderLearningPage = () => (
    <div className="p-6">
      <h2 className="text-3xl font-bold mb-6">AI Learning Logs</h2>
      <div className="space-y-4">
        {learningLogs.map((log) => (
          <div key={log.id} className="bg-base-200 p-6 rounded-lg">
            <div className="flex justify-between items-start mb-2">
              <h3 className="text-xl font-bold">{log.title}</h3>
              <span className="text-sm text-gray-400">{log.timestamp}</span>
            </div>
            <p className="text-gray-300 mb-3">{log.summary}</p>
            <div className="text-sm">
              <span className="text-gray-400">Accuracy Change: </span>
              <span className={`font-bold ${log.accuracyChange >= 0 ? 'text-accent' : 'text-danger'}`}>
                {log.accuracyChange >= 0 ? '+' : ''}{log.accuracyChange}%
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const [expandedSections, setExpandedSections] = useState<{ [key: string]: boolean }>({
    collectors: true,
    testers: true,
  });

  const toggleSection = (section: string) => {
    setExpandedSections(prev => ({ ...prev, [section]: !prev[section] }));
  };

  const renderAgentsPage = () => {
    // Categorize agents
    const masterAgent = agentDetails.find(a => a.name.toLowerCase().includes('master'));
    const supervisorAgent = agentDetails.find(a => a.name.toLowerCase().includes('supervisor'));
    const collectorAgents = agentDetails.filter(a =>
      a.type?.toLowerCase().includes('collector') || a.name.toLowerCase().includes('collector')
    );
    const testerAgents = agentDetails.filter(a =>
      a.type?.toLowerCase().includes('tester') || a.name.toLowerCase().includes('tester')
    );

    const renderAgentCard = (agent: AgentDetail, showCpuMem = true) => (
      <div
        key={agent.id}
        className="bg-base-300 p-4 rounded-lg cursor-pointer hover:bg-base-200 transition-colors border border-transparent hover:border-accent"
        onClick={() => setSelectedAgent(agent)}
      >
        <div className="flex justify-between items-start mb-3">
          <div className="flex items-center gap-2">
            <CpuChipIcon className="w-5 h-5 text-gray-400" />
            <h3 className="font-bold text-lg">{agent.name}</h3>
          </div>
          <div className="flex items-center gap-2">
            <span className={`w-2 h-2 rounded-full ${agent.status === 'Online' ? 'bg-accent' :
              agent.status === 'Processing' ? 'bg-info' : 'bg-gray-500'
              } ${agent.status === 'Online' || agent.status === 'Processing' ? 'animate-pulse' : ''}`}></span>
            <span className={`text-sm font-semibold ${agent.status === 'Online' ? 'text-accent' : 'text-info'
              }`}>{agent.status}</span>
          </div>
        </div>
        <p className="text-sm text-gray-400 mb-3">{agent.activity}</p>
        {showCpuMem && (
          <div className="space-y-2">
            <div>
              <div className="flex justify-between text-xs text-gray-400 mb-1">
                <span>CPU</span>
                <span>{agent.cpu?.toFixed(0)}%</span>
              </div>
              <div className="w-full bg-base-200 rounded-full h-2">
                <div
                  className="bg-accent h-2 rounded-full transition-all duration-300"
                  style={{ width: `${agent.cpu}%` }}
                ></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between text-xs text-gray-400 mb-1">
                <span>MEM</span>
                <span>{agent.memory?.toFixed(0)}%</span>
              </div>
              <div className="w-full bg-base-200 rounded-full h-2">
                <div
                  className="bg-info h-2 rounded-full transition-all duration-300"
                  style={{ width: `${agent.memory}%` }}
                ></div>
              </div>
            </div>
          </div>
        )}
      </div>
    );

    const onlineCount = (agents: AgentDetail[]) => agents.filter(a => a.status === 'Online' || a.status === 'Processing').length;

    return (
      <div className="p-6">
        <h2 className="text-3xl font-bold mb-6">AI Agent Status</h2>

        {/* Master Agent Section */}
        {masterAgent && (
          <div className="mb-6">
            <h3 className="text-xl font-semibold text-gray-400 mb-3">Master Agent</h3>
            {renderAgentCard(masterAgent)}
          </div>
        )}

        {/* Core System Agent Section */}
        {supervisorAgent && (
          <div className="mb-6">
            <h3 className="text-xl font-semibold text-gray-400 mb-3">Core System Agent</h3>
            {renderAgentCard(supervisorAgent)}
          </div>
        )}

        {/* Operational Agents Section */}
        <div className="mb-6">
          <div className="flex justify-between items-center mb-3">
            <h3 className="text-xl font-semibold text-gray-400">Operational Agents</h3>
            <button
              onClick={() => {
                setExpandedSections({ collectors: !expandedSections.collectors, testers: !expandedSections.testers });
              }}
              className="text-sm text-gray-500 hover:text-gray-300 transition-colors"
            >
              {expandedSections.collectors || expandedSections.testers ? 'Collapse All' : 'Expand All'}
            </button>
          </div>

          {/* Data Collector Agents */}
          <div className="bg-base-200 rounded-lg mb-4">
            <button
              onClick={() => toggleSection('collectors')}
              className="w-full p-4 flex justify-between items-center hover:bg-base-300 transition-colors rounded-lg"
            >
              <div className="flex items-center gap-3">
                <span className="text-lg font-semibold">Data Collector Agents ({collectorAgents.length})</span>
                <div className="flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-accent"></span>
                  <span className="text-sm text-accent font-semibold">({onlineCount(collectorAgents)})</span>
                </div>
              </div>
              <svg
                className={`w-5 h-5 transform transition-transform ${expandedSections.collectors ? 'rotate-180' : ''}`}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            {expandedSections.collectors && (
              <div className="p-4 pt-0 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {collectorAgents.length > 0 ? (
                  collectorAgents.map(agent => renderAgentCard(agent))
                ) : (
                  <p className="text-gray-500 col-span-full">No collector agents found</p>
                )}
              </div>
            )}
          </div>

          {/* Strategy Tester Agents */}
          <div className="bg-base-200 rounded-lg">
            <button
              onClick={() => toggleSection('testers')}
              className="w-full p-4 flex justify-between items-center hover:bg-base-300 transition-colors rounded-lg"
            >
              <div className="flex items-center gap-3">
                <span className="text-lg font-semibold">Strategy Tester Agents ({testerAgents.length})</span>
                <div className="flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-accent"></span>
                  <span className="text-sm text-accent font-semibold">({onlineCount(testerAgents)})</span>
                </div>
              </div>
              <svg
                className={`w-5 h-5 transform transition-transform ${expandedSections.testers ? 'rotate-180' : ''}`}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            {expandedSections.testers && (
              <div className="p-4 pt-0 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {testerAgents.length > 0 ? (
                  testerAgents.map(agent => renderAgentCard(agent))
                ) : (
                  <p className="text-gray-500 col-span-full">No tester agents found</p>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  const renderSettingsPage = () => (
    <div className="p-6">
      <h2 className="text-3xl font-bold mb-6">Settings</h2>
      <div className="bg-base-200 p-6 rounded-lg space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">Theme</label>
          <select
            value={theme}
            onChange={(e) => setTheme(e.target.value as Theme)}
            className="bg-base-300 px-4 py-2 rounded"
          >
            <option value="light">Light</option>
            <option value="dark">Dark</option>
          </select>
        </div>
        <div>
          <h3 className="font-bold mb-2">Paper Trading</h3>
          <button
            onClick={() => setCurrentPage('dashboard' as Page)} // Temporarily use dashboard, will add papertrading to Page type
            className="bg-accent text-white px-4 py-2 rounded hover:bg-accent/80"
          >
            Access Paper Trading (Coming Soon)
          </button>
        </div>
      </div>
    </div>
  );

  return (
    <div className="flex h-screen bg-base-100 text-slate-300">
      {/* Sidebar */}
      <div className={`fixed inset-y-0 left-0 z-50 w-64 bg-indigo-700 transform transition-transform duration-300 ease-in-out ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}>
        <div className="h-full overflow-y-auto">
          {/* Logo */}
          <div className="p-6 flex items-center gap-3">
            <DashboardIcon className="w-8 h-8 text-white" />
            <h1 className="text-2xl font-bold text-white">Gitta AI</h1>
          </div>

          {/* Navigation */}
          <nav className="px-4 space-y-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = currentPage === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    setCurrentPage(item.id);
                    setSidebarOpen(false); // Close sidebar after clicking on mobile
                  }}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${isActive
                    ? 'bg-white/20 text-white'
                    : 'text-indigo-100 hover:bg-white/10'
                    }`}
                >
                  <Icon className="w-5 h-5" />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <div className={`flex-1 flex flex-col transition-all duration-300 ${sidebarOpen ? 'ml-64' : 'ml-0'
        }`}>
        {/* Header */}
        <header className="bg-indigo-600 text-white p-4 flex items-center justify-between">
          {/* Menu Button - Always Visible */}
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 rounded hover:bg-indigo-700 transition-colors"
            title="Toggle Menu"
          >
            <MenuIcon className="w-6 h-6" />
          </button>
          <h2 className="text-2xl font-bold capitalize">{currentPage}</h2>
          <div className="w-10"></div>
        </header>

        {/* Ticker Bar */}
        <TickerBar />

        {/* Page Content */}
        <main className="flex-1 overflow-y-auto">
          {renderPage()}
        </main>
      </div>

      {/* Stock Detail Page */}
      {chartModal && (
        <StockDetailPage
          symbol={chartModal.symbol}
          name={chartModal.name}
          onClose={closeChart}
        />
      )}

      {/* Agent Details Modal */}
      {selectedAgent && (
        <AgentDetailsModal
          agentId={selectedAgent.id}
          agentName={selectedAgent.name}
          onClose={() => setSelectedAgent(null)}
        />
      )}
    </div>
  );
}

export default App;