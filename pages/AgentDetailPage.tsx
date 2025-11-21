import { useState, useEffect } from 'react';
import { ArrowLeft, Activity, Clock, CheckCircle, XCircle, AlertCircle, ExternalLink, RefreshCw, TrendingUp, Target, Zap, Database, Award, AlertTriangle, Cpu, BarChart3, PieChart } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart as RechartsPie, Pie, Cell, AreaChart, Area, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';

interface AgentDetailPageProps {
    agentId: string;
    onClose: () => void;
}

export default function AgentDetailPage({ agentId, onClose }: AgentDetailPageProps) {
    const [agentData, setAgentData] = useState<any>(null);
    const [activityLog, setActivityLog] = useState<any>(null);
    const [last24Hours, setLast24Hours] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [autoRefresh, setAutoRefresh] = useState(true);

    useEffect(() => {
        fetchAllData();
        const interval = autoRefresh ? setInterval(fetchAllData, 30000) : null;
        return () => { if (interval) clearInterval(interval); };
    }, [agentId, autoRefresh]);

    const generateMockData = (id: string) => {
        const names: Record<string, string> = {
            'agent_1': 'YouTube Trend Hunter', 'agent_2': 'YouTube Scalping Specialist', 'agent_3': 'YouTube Swing Trader',
            'agent_4': 'Reddit WSB Monitor', 'agent_5': 'Reddit Algo Researcher', 'agent_6': 'Web News Aggregator',
            'agent_7': 'Technical Indicator Analyst', 'agent_8': 'Crypto Strategy Hunter', 'agent_9': 'Angel One Data Miner', 'agent_10': 'Market Sentiment Analyzer',
            'tester_1': 'Conservative Tester', 'tester_2': 'Aggressive Tester', 'tester_3': 'Balanced Tester',
            'tester_4': 'Scalping Tester', 'tester_5': 'Swing Tester', 'tester_6': 'Day Trader',
            'tester_7': 'Position Trader', 'tester_8': 'Volatility Tester', 'tester_9': 'Trend Follower', 'tester_10': 'Mean Reversion Tester'
        };

        if (id.startsWith('tester_')) {
            return {
                agent_id: id, name: names[id] || `Tester ${id}`, type: 'Tester', specialty: 'Strategy Simulation', status: 'idle',
                stats: { total_tests: 120, avg_win_rate: 65, avg_profit_factor: 1.5, avg_net_profit: 1250, pass_rate: 70 },
                test_results: [],
                performanceMetrics: { "Win Rate": 65, "Profit Factor": 75, "Pass Rate": 70, "Activity": 80, "Profitability": 60 },
                profitDistribution: [
                    { range: '> $1000', count: 15 }, { range: '$500-$1000', count: 30 },
                    { range: '$0-$500', count: 45 }, { range: 'Loss', count: 30 }
                ]
            };
        }

        return {
            agent_id: id, name: names[id] || `Agent ${id}`, type: 'Collector', specialty: 'Trading Strategy Collection', status: 'idle',
            stats: { total_collected: 85, success_rate: 82, avg_quality_score: 88, uptime_percentage: 97, collections_today: 12, avg_collection_time: 2.4, errors_24h: 2 },
            verification: { approved: 65, warning: 12, rejected: 8, avg_confidence: 85 },
            timeline: Array.from({ length: 30 }, (_, i) => ({
                date: new Date(Date.now() - (29 - i) * 24 * 60 * 60 * 1000).toISOString().split('T')[0], count: Math.floor(Math.random() * 10) + 2
            })),
            sourceBreakdown: [
                { source: 'YouTube', count: 45, percentage: 53 },
                { source: 'Reddit', count: 25, percentage: 29 },
                { source: 'Web', count: 15, percentage: 18 }
            ],
            qualityDistribution: [
                { range: '90-100%', count: 35 },
                { range: '80-89%', count: 30 },
                { range: '70-79%', count: 15 },
                { range: '60-69%', count: 5 }
            ],
            performanceMetrics: {
                speed: 92,
                accuracy: 88,
                reliability: 95,
                efficiency: 85,
                coverage: 78
            }
        };
    };

    const generateMockActivities = (id: string) => {
        const strategies = ['NIFTY Breakout', 'Bank NIFTY Scalping', 'Options Gamma', 'Momentum RSI', 'Support Resistance',
            'MA Crossover', 'Volume Profile', 'Fibonacci', 'Bollinger Squeeze', 'MACD Divergence', 'Ichimoku Cloud', 'Stochastic Oscillator'];
        return Array.from({ length: 20 }, (_, i) => ({
            id: i + 1, timestamp: new Date(Date.now() - i * 2 * 60 * 60 * 1000).toISOString(), type: 'collection',
            action: 'Collected strategy', strategy_name: strategies[i % strategies.length],
            source: i % 3 === 0 ? 'YouTube' : i % 3 === 1 ? 'Reddit' : 'Web', source_url: `https://example.com/s-${i}`,
            status: i % 5 === 0 ? 'rejected' : i % 3 === 0 ? 'warning' : 'approved', quality_score: Math.floor(Math.random() * 30) + 65,
            details: { ai_models: 12, consensus: 85, processing_time: 1.8 }
        }));
    };

    const fetchAllData = async () => {
        try {
            const detailsRes = await fetch(`/api/agents/${agentId}/details`);
            if (!detailsRes.ok) {
                setAgentData(generateMockData(agentId));
                const mockActs = generateMockActivities(agentId);
                setActivityLog({ activities: mockActs, total_activities: 20 });
                setLast24Hours(mockActs.slice(0, 10));
                setLoading(false);
                return;
            }
            const details = await detailsRes.json();
            setAgentData(details);
            const activityRes = await fetch(`/api/agents/${agentId}/activity?limit=100`);
            const activity = activityRes.ok ? await activityRes.json() : { activities: [], total_activities: 0 };
            setActivityLog(activity);
            const now = new Date();
            const last24h = activity.activities.filter((a: any) => {
                const activityTime = new Date(a.timestamp);
                return (now.getTime() - activityTime.getTime()) / (1000 * 60 * 60) <= 24;
            });
            setLast24Hours(last24h);
            setLoading(false);
        } catch (error) {
            setAgentData(generateMockData(agentId));
            const mockActs = generateMockActivities(agentId);
            setActivityLog({ activities: mockActs, total_activities: 20 });
            setLast24Hours(mockActs.slice(0, 10));
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-slate-950 via-blue-950 to-slate-950 flex items-center justify-center">
                <div className="text-center">
                    <div className="relative">
                        <div className="animate-spin rounded-full h-20 w-20 border-t-4 border-b-4 border-blue-500 mx-auto"></div>
                        <div className="animate-ping absolute inset-0 rounded-full h-20 w-20 border-4 border-blue-400 opacity-20 mx-auto"></div>
                    </div>
                    <p className="text-blue-300 mt-6 font-semibold text-lg">Loading agent details...</p>
                </div>
            </div>
        );
    }

    if (!agentData) return (
        <div className="min-h-screen bg-gradient-to-br from-slate-950 via-blue-950 to-slate-950 flex items-center justify-center">
            <div className="text-center">
                <XCircle className="w-20 h-20 text-red-400 mx-auto mb-4" />
                <p className="text-red-400 text-2xl font-bold mb-4">Agent not found</p>
                <button onClick={onClose} className="px-8 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl hover:from-blue-600 hover:to-purple-700 font-semibold shadow-lg">Back to Agents</button>
            </div>
        </div>
    );

    const getStatusColor = (status: string) => status === 'approved' ? 'text-emerald-400' : status === 'rejected' ? 'text-red-400' : 'text-amber-400';
    const getStatusIcon = (status: string) => status === 'approved' ? <CheckCircle className="w-5 h-5" /> : status === 'rejected' ? <XCircle className="w-5 h-5" /> : <AlertCircle className="w-5 h-5" />;
    const getStatusBadge = (status: string) => status === 'approved' ? 'bg-emerald-500/20 border-emerald-500/40' : status === 'rejected' ? 'bg-red-500/20 border-red-500/40' : 'bg-amber-500/20 border-amber-500/40';

    const hourlyActivity = Array.from({ length: 24 }, (_, i) => {
        const hour = new Date().getHours() - (23 - i);
        const activities = last24Hours.filter(a => new Date(a.timestamp).getHours() === (hour < 0 ? hour + 24 : hour) % 24);
        return { hour: `${(hour < 0 ? hour + 24 : hour) % 24}:00`, count: activities.length };
    });

    const COLORS = ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b'];
    const radarData = Object.entries(agentData.performanceMetrics || {}).map(([key, value]) => ({
        metric: key.charAt(0).toUpperCase() + key.slice(1),
        value: value,
        fullMark: 100
    }));

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-950 via-blue-950 to-slate-950 overflow-y-auto">
            {/* Ultra-Modern Header with Glassmorphism */}
            <div className="sticky top-0 z-50 backdrop-blur-xl bg-slate-900/60 border-b border-blue-500/20 shadow-2xl">
                <div className="max-w-[1600px] mx-auto px-8 py-5">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-5">
                            <button onClick={onClose} className="p-3 hover:bg-blue-500/20 rounded-xl transition-all hover:scale-110 group">
                                <ArrowLeft className="w-6 h-6 text-blue-300 group-hover:text-blue-400" />
                            </button>
                            <div>
                                <h1 className="text-4xl font-black bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">{agentData.name}</h1>
                                <p className="text-blue-300/80 mt-1 font-medium flex items-center gap-2">
                                    <Database className="w-4 h-4" />
                                    {agentData.type} • {agentData.specialty}
                                </p>
                            </div>
                        </div>
                        <div className="flex items-center gap-4">
                            <div className={`flex items-center gap-3 px-6 py-3 rounded-xl backdrop-blur-sm ${agentData.status === 'fetching' ? 'bg-blue-500/20 border border-blue-500/40 shadow-lg shadow-blue-500/20' :
                                agentData.status === 'processing' ? 'bg-purple-500/20 border border-purple-500/40 shadow-lg shadow-purple-500/20' :
                                    'bg-slate-500/20 border border-slate-500/40'
                                }`}>
                                <Activity className={`w-6 h-6 ${agentData.status !== 'idle' ? 'animate-pulse' : ''}`} />
                                <span className="font-bold text-lg">{agentData.status?.toUpperCase() || 'IDLE'}</span>
                            </div>
                            <button
                                onClick={() => setAutoRefresh(!autoRefresh)}
                                className={`p-3 rounded-xl transition-all ${autoRefresh ? 'bg-emerald-500/20 border border-emerald-500/40 shadow-lg shadow-emerald-500/20' : 'bg-slate-700/40 border border-slate-600/40'}`}
                                title={autoRefresh ? 'Auto-refresh ON' : 'Auto-refresh OFF'}>
                                <RefreshCw className={`w-6 h-6 ${autoRefresh ? 'animate-spin text-emerald-400' : 'text-slate-400'}`} />
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <div className="max-w-[1600px] mx-auto px-8 py-10 space-y-8">
                {/* Hero Stats Grid - Glassmorphism Cards */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    {agentData.type === 'Tester' ? (
                        <>
                            <div className="relative group">
                                <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-2xl blur-lg opacity-30 group-hover:opacity-50 transition-opacity"></div>
                                <div className="relative backdrop-blur-xl bg-slate-900/60 border border-blue-500/30 rounded-2xl p-6 hover:border-blue-400/50 transition-all">
                                    <div className="flex items-center justify-between mb-3">
                                        <Database className="w-8 h-8 text-blue-400" />
                                        <TrendingUp className="w-5 h-5 text-emerald-400" />
                                    </div>
                                    <div className="text-slate-400 text-sm font-semibold mb-2">TOTAL TESTS</div>
                                    <div className="text-5xl font-black text-white mb-2">{agentData.stats.total_tests}</div>
                                    <div className="text-emerald-400 text-sm font-bold flex items-center gap-1">
                                        <span className="text-2xl">↑</span> {last24Hours.length} in last 24h
                                    </div>
                                </div>
                            </div>

                            <div className="relative group">
                                <div className="absolute inset-0 bg-gradient-to-r from-emerald-500 to-green-500 rounded-2xl blur-lg opacity-30 group-hover:opacity-50 transition-opacity"></div>
                                <div className="relative backdrop-blur-xl bg-slate-900/60 border border-emerald-500/30 rounded-2xl p-6 hover:border-emerald-400/50 transition-all">
                                    <div className="flex items-center justify-between mb-3">
                                        <Target className="w-8 h-8 text-emerald-400" />
                                        <Award className="w-5 h-5 text-amber-400" />
                                    </div>
                                    <div className="text-slate-400 text-sm font-semibold mb-2">WIN RATE</div>
                                    <div className="text-5xl font-black bg-gradient-to-r from-emerald-400 to-green-400 bg-clip-text text-transparent mb-2">
                                        {agentData.stats.avg_win_rate}%
                                    </div>
                                    <div className="text-emerald-400/80 text-sm font-semibold">Average Win Rate</div>
                                </div>
                            </div>

                            <div className="relative group">
                                <div className="absolute inset-0 bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl blur-lg opacity-30 group-hover:opacity-50 transition-opacity"></div>
                                <div className="relative backdrop-blur-xl bg-slate-900/60 border border-purple-500/30 rounded-2xl p-6 hover:border-purple-400/50 transition-all">
                                    <div className="flex items-center justify-between mb-3">
                                        <BarChart3 className="w-8 h-8 text-purple-400" />
                                        <Zap className="w-5 h-5 text-yellow-400" />
                                    </div>
                                    <div className="text-slate-400 text-sm font-semibold mb-2">PROFIT FACTOR</div>
                                    <div className="text-5xl font-black bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent mb-2">
                                        {agentData.stats.avg_profit_factor}
                                    </div>
                                    <div className="text-purple-400/80 text-sm font-semibold">Risk/Reward Ratio</div>
                                </div>
                            </div>

                            <div className="relative group">
                                <div className="absolute inset-0 bg-gradient-to-r from-amber-500 to-orange-500 rounded-2xl blur-lg opacity-30 group-hover:opacity-50 transition-opacity"></div>
                                <div className="relative backdrop-blur-xl bg-slate-900/60 border border-amber-500/30 rounded-2xl p-6 hover:border-amber-400/50 transition-all">
                                    <div className="flex items-center justify-between mb-3">
                                        <Cpu className="w-8 h-8 text-amber-400" />
                                        <Activity className="w-5 h-5 text-emerald-400 animate-pulse" />
                                    </div>
                                    <div className="text-slate-400 text-sm font-semibold mb-2">NET PROFIT</div>
                                    <div className="text-5xl font-black bg-gradient-to-r from-amber-400 to-orange-400 bg-clip-text text-transparent mb-2">
                                        ${agentData.stats.avg_net_profit}
                                    </div>
                                    <div className="text-amber-400/80 text-sm font-semibold">Avg per Strategy</div>
                                </div>
                            </div>
                        </>
                    ) : (
                        <>
                            <div className="relative group">
                                <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-2xl blur-lg opacity-30 group-hover:opacity-50 transition-opacity"></div>
                                <div className="relative backdrop-blur-xl bg-slate-900/60 border border-blue-500/30 rounded-2xl p-6 hover:border-blue-400/50 transition-all">
                                    <div className="flex items-center justify-between mb-3">
                                        <Database className="w-8 h-8 text-blue-400" />
                                        <TrendingUp className="w-5 h-5 text-emerald-400" />
                                    </div>
                                    <div className="text-slate-400 text-sm font-semibold mb-2">TOTAL COLLECTED</div>
                                    <div className="text-5xl font-black text-white mb-2">{agentData.stats.total_collected}</div>
                                    <div className="text-emerald-400 text-sm font-bold flex items-center gap-1">
                                        <span className="text-2xl">↑</span> {last24Hours.length} in last 24h
                                    </div>
                                </div>
                            </div>

                            <div className="relative group">
                                <div className="absolute inset-0 bg-gradient-to-r from-emerald-500 to-green-500 rounded-2xl blur-lg opacity-30 group-hover:opacity-50 transition-opacity"></div>
                                <div className="relative backdrop-blur-xl bg-slate-900/60 border border-emerald-500/30 rounded-2xl p-6 hover:border-emerald-400/50 transition-all">
                                    <div className="flex items-center justify-between mb-3">
                                        <Target className="w-8 h-8 text-emerald-400" />
                                        <Award className="w-5 h-5 text-amber-400" />
                                    </div>
                                    <div className="text-slate-400 text-sm font-semibold mb-2">SUCCESS RATE</div>
                                    <div className="text-5xl font-black bg-gradient-to-r from-emerald-400 to-green-400 bg-clip-text text-transparent mb-2">
                                        {agentData.stats.success_rate}%
                                    </div>
                                    <div className="text-emerald-400/80 text-sm font-semibold">Multi-AI Verified</div>
                                </div>
                            </div>

                            <div className="relative group">
                                <div className="absolute inset-0 bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl blur-lg opacity-30 group-hover:opacity-50 transition-opacity"></div>
                                <div className="relative backdrop-blur-xl bg-slate-900/60 border border-purple-500/30 rounded-2xl p-6 hover:border-purple-400/50 transition-all">
                                    <div className="flex items-center justify-between mb-3">
                                        <BarChart3 className="w-8 h-8 text-purple-400" />
                                        <Zap className="w-5 h-5 text-yellow-400" />
                                    </div>
                                    <div className="text-slate-400 text-sm font-semibold mb-2">AVG QUALITY</div>
                                    <div className="text-5xl font-black bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent mb-2">
                                        {agentData.stats.avg_quality_score}%
                                    </div>
                                    <div className="text-purple-400/80 text-sm font-semibold">Quality Score</div>
                                </div>
                            </div>

                            <div className="relative group">
                                <div className="absolute inset-0 bg-gradient-to-r from-amber-500 to-orange-500 rounded-2xl blur-lg opacity-30 group-hover:opacity-50 transition-opacity"></div>
                                <div className="relative backdrop-blur-xl bg-slate-900/60 border border-amber-500/30 rounded-2xl p-6 hover:border-amber-400/50 transition-all">
                                    <div className="flex items-center justify-between mb-3">
                                        <Cpu className="w-8 h-8 text-amber-400" />
                                        <Activity className="w-5 h-5 text-emerald-400 animate-pulse" />
                                    </div>
                                    <div className="text-slate-400 text-sm font-semibold mb-2">UPTIME</div>
                                    <div className="text-5xl font-black bg-gradient-to-r from-amber-400 to-orange-400 bg-clip-text text-transparent mb-2">
                                        {agentData.stats.uptime_percentage}%
                                    </div>
                                    <div className="text-amber-400/80 text-sm font-semibold">24/7 Operation</div>
                                </div>
                            </div>
                        </>
                    )}
                </div>

                {/* Performance Radar & Quality Distribution */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <div className="relative group">
                        <div className="absolute inset-0 bg-gradient-to-br from-blue-500/20 to-purple-500/20 rounded-2xl blur-xl"></div>
                        <div className="relative backdrop-blur-xl bg-slate-900/60 border border-blue-500/30 rounded-2xl p-6">
                            <h2 className="text-2xl font-black text-white mb-6 flex items-center gap-3">
                                <PieChart className="w-7 h-7 text-blue-400" />
                                <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">Performance Metrics</span>
                            </h2>
                            <div className="h-80">
                                <ResponsiveContainer width="100%" height="100%">
                                    <RadarChart data={radarData}>
                                        <PolarGrid stroke="#334155" />
                                        <PolarAngleAxis dataKey="metric" tick={{ fill: '#94a3b8', fontSize: 13, fontWeight: 'bold' }} />
                                        <PolarRadiusAxis angle={90} domain={[0, 100]} tick={{ fill: '#64748b' }} />
                                        <Radar name="Performance" dataKey="value" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.6} />
                                        <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569', borderRadius: '12px', fontWeight: 'bold' }} />
                                    </RadarChart>
                                </ResponsiveContainer>
                            </div>
                        </div>
                    </div>

                    <div className="relative group">
                        <div className="absolute inset-0 bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-2xl blur-xl"></div>
                        <div className="relative backdrop-blur-xl bg-slate-900/60 border border-purple-500/30 rounded-2xl p-6">
                            <h2 className="text-2xl font-black text-white mb-6 flex items-center gap-3">
                                <BarChart3 className="w-7 h-7 text-purple-400" />
                                <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                                    {agentData.type === 'Tester' ? 'Profit Distribution' : 'Quality Distribution'}
                                </span>
                            </h2>
                            <div className="h-80">
                                <ResponsiveContainer width="100%" height="100%">
                                    <BarChart data={agentData.type === 'Tester' ? agentData.profitDistribution : agentData.qualityDistribution} layout="vertical">
                                        <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                                        <XAxis type="number" stroke="#94a3b8" tick={{ fill: '#94a3b8', fontWeight: 'bold' }} />
                                        <YAxis dataKey="range" type="category" stroke="#94a3b8" tick={{ fill: '#cbd5e1', fontWeight: 'bold', fontSize: 13 }} width={80} />
                                        <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569', borderRadius: '12px', fontWeight: 'bold' }} />
                                        <Bar dataKey="count" fill="url(#colorGradient)" radius={[0, 8, 8, 0]} />
                                        <defs>
                                            <linearGradient id="colorGradient" x1="0" y1="0" x2="1" y2="0">
                                                <stop offset="0%" stopColor="#8b5cf6" />
                                                <stop offset="100%" stopColor="#ec4899" />
                                            </linearGradient>
                                        </defs>
                                    </BarChart>
                                </ResponsiveContainer>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Current Activity & 24h Chart */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <div className="relative group">
                        <div className="absolute inset-0 bg-gradient-to-br from-emerald-500/20 to-cyan-500/20 rounded-2xl blur-xl"></div>
                        <div className="relative backdrop-blur-xl bg-slate-900/60 border border-emerald-500/30 rounded-2xl p-6">
                            <h2 className="text-2xl font-black text-white mb-6 flex items-center gap-3">
                                <Activity className="w-7 h-7 text-emerald-400 animate-pulse" />
                                <span className="bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">Live Activity</span>
                            </h2>
                            {last24Hours.length > 0 ? (
                                <div className="space-y-4">
                                    <div className="relative group/card">
                                        <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-xl blur"></div>
                                        <div className="relative bg-slate-800/50 border border-blue-500/20 rounded-xl p-5 hover:border-blue-400/40 transition-all">
                                            <div className="flex items-center justify-between mb-3">
                                                <span className="text-white font-black text-lg">Latest Collection</span>
                                                <span className="text-blue-400 text-sm font-bold bg-blue-500/20 px-3 py-1 rounded-lg">
                                                    {new Date(last24Hours[0].timestamp).toLocaleTimeString()}
                                                </span>
                                            </div>
                                            <p className="text-white text-xl font-bold mb-3">{last24Hours[0].strategy_name}</p>
                                            <div className="flex items-center gap-3">
                                                <span className={`${getStatusColor(last24Hours[0].status)} flex items-center gap-2 font-bold`}>
                                                    {getStatusIcon(last24Hours[0].status)}
                                                    <span className="capitalize">{last24Hours[0].status}</span>
                                                </span>
                                                <span className="text-slate-400">•</span>
                                                <span className="text-blue-300 font-semibold">{last24Hours[0].source}</span>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="backdrop-blur-sm bg-emerald-500/10 border border-emerald-500/30 rounded-xl p-4 hover:bg-emerald-500/20 transition-all">
                                            <div className="text-emerald-400 text-sm font-bold mb-1">Approved (24h)</div>
                                            <div className="text-4xl font-black text-white">{last24Hours.filter(a => a.status === 'approved').length}</div>
                                        </div>
                                        <div className="backdrop-blur-sm bg-red-500/10 border border-red-500/30 rounded-xl p-4 hover:bg-red-500/20 transition-all">
                                            <div className="text-red-400 text-sm font-bold mb-1">Rejected (24h)</div>
                                            <div className="text-4xl font-black text-white">{last24Hours.filter(a => a.status === 'rejected').length}</div>
                                        </div>
                                    </div>
                                </div>
                            ) : <div className="text-center py-16 text-slate-500 font-semibold">No activity in last 24h</div>}
                        </div>
                    </div>

                    <div className="relative group">
                        <div className="absolute inset-0 bg-gradient-to-br from-blue-500/20 to-indigo-500/20 rounded-2xl blur-xl"></div>
                        <div className="relative backdrop-blur-xl bg-slate-900/60 border border-blue-500/30 rounded-2xl p-6">
                            <h2 className="text-2xl font-black text-white mb-6 flex items-center gap-3">
                                <Clock className="w-7 h-7 text-blue-400" />
                                <span className="bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">24-Hour Activity</span>
                            </h2>
                            <div className="h-64">
                                <ResponsiveContainer width="100%" height="100%">
                                    <AreaChart data={hourlyActivity}>
                                        <defs>
                                            <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                                                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8} />
                                                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.1} />
                                            </linearGradient>
                                        </defs>
                                        <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                                        <XAxis dataKey="hour" stroke="#94a3b8" tick={{ fill: '#94a3b8', fontSize: 11, fontWeight: 'bold' }} />
                                        <YAxis stroke="#94a3b8" tick={{ fill: '#94a3b8', fontSize: 12, fontWeight: 'bold' }} />
                                        <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569', borderRadius: '12px', fontWeight: 'bold' }} />
                                        <Area type="monotone" dataKey="count" stroke="#3b82f6" strokeWidth={3} fillOpacity={1} fill="url(#colorCount)" />
                                    </AreaChart>
                                </ResponsiveContainer>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Activity Log - Ultra Modern */}
                <div className="relative group">
                    <div className="absolute inset-0 bg-gradient-to-br from-violet-500/20 to-fuchsia-500/20 rounded-2xl blur-xl"></div>
                    <div className="relative backdrop-blur-xl bg-slate-900/60 border border-violet-500/30 rounded-2xl p-6">
                        <h2 className="text-2xl font-black text-white mb-6 flex items-center gap-3">
                            <Database className="w-7 h-7 text-violet-400" />
                            <span className="bg-gradient-to-r from-violet-400 to-fuchsia-400 bg-clip-text text-transparent">Complete Activity Log</span>
                            <span className="ml-auto text-lg font-bold text-violet-400 bg-violet-500/20 px-4 py-2 rounded-xl">{last24Hours.length} activities</span>
                        </h2>
                        <div className="space-y-3 max-h-[600px] overflow-y-auto pr-2 custom-scrollbar">
                            {last24Hours.map((activity, idx) => (
                                <div key={activity.id} className="relative group/item">
                                    <div className="absolute inset-0 bg-gradient-to-r from-blue-500/5 to-purple-500/5 rounded-xl blur opacity-0 group-hover/item:opacity-100 transition-opacity"></div>
                                    <div className={`relative backdrop-blur-sm bg-slate-800/40 border ${getStatusBadge(activity.status)} rounded-xl p-5 hover:bg-slate-800/60 transition-all`}>
                                        <div className="flex items-start justify-between gap-4">
                                            <div className="flex-1">
                                                <div className="flex items-center gap-3 mb-3">
                                                    <span className={`${getStatusColor(activity.status)} flex items-center gap-2 font-bold text-lg`}>
                                                        {getStatusIcon(activity.status)}
                                                    </span>
                                                    <span className="font-black text-white text-lg">{activity.strategy_name}</span>
                                                    <span className="text-slate-500 text-sm">#{idx + 1}</span>
                                                </div>
                                                <div className="flex items-center gap-3 text-sm mb-2">
                                                    <Clock className="w-4 h-4 text-blue-400" />
                                                    <span className="text-blue-300 font-semibold">{new Date(activity.timestamp).toLocaleString()}</span>
                                                    <span className="text-slate-500">•</span>
                                                    <span className="text-purple-300 font-semibold">{activity.source}</span>
                                                </div>
                                                {activity.details && (
                                                    <div className="flex items-center gap-4 text-xs mt-2">
                                                        <span className="text-slate-400 bg-slate-700/50 px-2 py-1 rounded-lg"><strong>AI Models:</strong> {activity.details.ai_models}</span>
                                                        <span className="text-slate-400 bg-slate-700/50 px-2 py-1 rounded-lg"><strong>Consensus:</strong> {activity.details.consensus}%</span>
                                                        <span className="text-slate-400 bg-slate-700/50 px-2 py-1 rounded-lg"><strong>Time:</strong> {activity.details.processing_time}s</span>
                                                    </div>
                                                )}
                                            </div>
                                            <div className="flex items-center gap-4">
                                                <div className="text-right bg-slate-700/30 px-4 py-3 rounded-xl border border-slate-600/30">
                                                    <div className="text-xs text-slate-400 font-bold mb-1">QUALITY</div>
                                                    <div className={`text-3xl font-black ${activity.quality_score >= 80 ? 'text-emerald-400' :
                                                        activity.quality_score >= 60 ? 'text-amber-400' : 'text-red-400'
                                                        }`}>
                                                        {activity.quality_score}%
                                                    </div>
                                                </div>
                                                {activity.source_url && (
                                                    <a href={activity.source_url} target="_blank" rel="noopener noreferrer"
                                                        className="p-3 hover:bg-blue-500/20 rounded-xl transition-all border border-blue-500/30 hover:border-blue-400/50">
                                                        <ExternalLink className="w-6 h-6 text-blue-400" />
                                                    </a>
                                                )}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* 30-Day Timeline */}
                {agentData.timeline && agentData.timeline.length > 0 && (
                    <div className="relative group">
                        <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/20 to-blue-500/20 rounded-2xl blur-xl"></div>
                        <div className="relative backdrop-blur-xl bg-slate-900/60 border border-cyan-500/30 rounded-2xl p-6">
                            <h2 className="text-2xl font-black text-white mb-6 flex items-center gap-3">
                                <TrendingUp className="w-7 h-7 text-cyan-400" />
                                <span className="bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">30-Day Performance Timeline</span>
                            </h2>
                            <div className="h-96">
                                <ResponsiveContainer width="100%" height="100%">
                                    <AreaChart data={[...agentData.timeline].reverse()}>
                                        <defs>
                                            <linearGradient id="timeline" x1="0" y1="0" x2="0" y2="1">
                                                <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.8} />
                                                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.2} />
                                            </linearGradient>
                                        </defs>
                                        <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                                        <XAxis dataKey="date" stroke="#94a3b8" tick={{ fill: '#94a3b8', fontSize: 11, fontWeight: 'bold' }}
                                            tickFormatter={(v) => new Date(v).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })} />
                                        <YAxis stroke="#94a3b8" tick={{ fill: '#94a3b8', fontSize: 13, fontWeight: 'bold' }} />
                                        <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569', borderRadius: '12px', fontWeight: 'bold' }} />
                                        <Area type="monotone" dataKey="count" stroke="#06b6d4" strokeWidth={4} fill="url(#timeline)" />
                                    </AreaChart>
                                </ResponsiveContainer>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            <style>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 8px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: rgba(15, 23, 42, 0.4);
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: linear-gradient(180deg, #3b82f6, #8b5cf6);
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: linear-gradient(180deg, #60a5fa, #a78bfa);
        }
      `}</style>
        </div>
    );
}
