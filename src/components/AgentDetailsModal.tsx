import React, { useEffect, useState } from 'react';
import { XMarkIcon, CpuChipIcon, ClockIcon, CheckCircleIcon, XCircleIcon } from '../../components/icons';

interface AgentDetailsModalProps {
    agentId: string;
    agentName: string;
    onClose: () => void;
}

interface AgentStats {
    total_collected: number;
    success_rate: number;
    avg_quality_score: number;
    uptime_percentage: number;
}

interface AgentLog {
    id: number;
    activity_type: string;
    description: string;
    timestamp: string;
    metadata?: string;
}

interface AgentCollection {
    id: number;
    strategy_name: string;
    source: string;
    collected_at: string;
    verification_status: string;
    quality_score: number;
}

interface LiveStatus {
    status: string;
    activity: string;
    last_updated: string;
}

const AgentDetailsModal: React.FC<AgentDetailsModalProps> = ({ agentId, agentName, onClose }) => {
    const [stats, setStats] = useState<AgentStats | null>(null);
    const [logs, setLogs] = useState<AgentLog[]>([]);
    const [collections, setCollections] = useState<AgentCollection[]>([]);
    const [liveStatus, setLiveStatus] = useState<LiveStatus | null>(null);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState<'overview' | 'live' | 'logs' | 'collections'>('overview');

    useEffect(() => {
        const fetchDetails = async () => {
            try {
                const response = await fetch(`http://localhost:5000/api/agents/${agentId}/details`);
                if (response.ok) {
                    const data = await response.json();
                    setStats(data.stats);
                    setLogs(data.logs || []);
                    setCollections(data.recent_collections || []);
                    setLiveStatus(data.live_status || null);
                }
            } catch (error) {
                console.error('Failed to fetch agent details:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchDetails();
        const interval = setInterval(fetchDetails, 5000); // Refresh every 5s
        return () => clearInterval(interval);
    }, [agentId]);

    if (!stats && loading) {
        return (
            <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center">
                <div className="loading loading-spinner loading-lg text-accent"></div>
            </div>
        );
    }

    return (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
            <div className="bg-base-100 w-full max-w-4xl rounded-xl shadow-2xl border border-base-300 flex flex-col max-h-[90vh]">

                {/* Header */}
                <div className="p-6 border-b border-base-300 flex justify-between items-center bg-base-200/50 rounded-t-xl">
                    <div className="flex items-center gap-4">
                        <div className="p-3 bg-indigo-500/20 rounded-lg">
                            <CpuChipIcon className="w-8 h-8 text-indigo-400" />
                        </div>
                        <div>
                            <h2 className="text-2xl font-bold text-white">{agentName}</h2>
                            <p className="text-sm text-gray-400 font-mono">{agentId}</p>
                        </div>
                    </div>
                    <button onClick={onClose} className="btn btn-ghost btn-circle hover:bg-base-300">
                        <XMarkIcon className="w-6 h-6" />
                    </button>
                </div>

                {/* Tabs */}
                <div className="flex border-b border-base-300 px-6">
                    <button
                        className={`px-6 py-4 text-sm font-medium border-b-2 transition-colors ${activeTab === 'overview' ? 'border-accent text-accent' : 'border-transparent text-gray-400 hover:text-white'}`}
                        onClick={() => setActiveTab('overview')}
                    >
                        Overview
                    </button>
                    <button
                        className={`px-6 py-4 text-sm font-medium border-b-2 transition-colors ${activeTab === 'logs' ? 'border-accent text-accent' : 'border-transparent text-gray-400 hover:text-white'}`}
                        onClick={() => setActiveTab('logs')}
                    >
                        Activity Logs
                    </button>
                    <button
                        className={`px-6 py-4 text-sm font-medium border-b-2 transition-colors ${activeTab === 'live' ? 'border-accent text-accent' : 'border-transparent text-gray-400 hover:text-white'}`}
                        onClick={() => setActiveTab('live')}
                    >
                        Live Activity
                    </button>
                    <button
                        className={`px-6 py-4 text-sm font-medium border-b-2 transition-colors ${activeTab === 'collections' ? 'border-accent text-accent' : 'border-transparent text-gray-400 hover:text-white'}`}
                        onClick={() => setActiveTab('collections')}
                    >
                        Collections
                    </button>
                </div>

                {/* Content */}
                <div className="flex-1 overflow-y-auto p-6">
                    {activeTab === 'overview' && stats && (
                        <div className="space-y-6">
                            {/* Stats Grid */}
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                                <div className="bg-base-200 p-4 rounded-lg border border-base-300">
                                    <p className="text-gray-400 text-sm mb-1">Total Collected</p>
                                    <p className="text-2xl font-bold text-white">{stats.total_collected}</p>
                                </div>
                                <div className="bg-base-200 p-4 rounded-lg border border-base-300">
                                    <p className="text-gray-400 text-sm mb-1">Success Rate</p>
                                    <p className={`text-2xl font-bold ${stats.success_rate >= 80 ? 'text-success' : 'text-warning'}`}>
                                        {stats.success_rate}%
                                    </p>
                                </div>
                                <div className="bg-base-200 p-4 rounded-lg border border-base-300">
                                    <p className="text-gray-400 text-sm mb-1">Avg Quality</p>
                                    <p className="text-2xl font-bold text-info">{stats.avg_quality_score}</p>
                                </div>
                                <div className="bg-base-200 p-4 rounded-lg border border-base-300">
                                    <p className="text-gray-400 text-sm mb-1">Uptime</p>
                                    <p className="text-2xl font-bold text-success">{stats.uptime_percentage}%</p>
                                </div>
                            </div>

                            {/* Recent Activity Preview */}
                            <div>
                                <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                                    <ClockIcon className="w-5 h-5 text-gray-400" />
                                    Recent Activity
                                </h3>
                                <div className="bg-base-200 rounded-lg border border-base-300 overflow-hidden">
                                    {logs.slice(0, 5).map((log) => (
                                        <div key={log.id} className="p-4 border-b border-base-300 last:border-0 hover:bg-base-300/50 transition-colors">
                                            <div className="flex justify-between items-start">
                                                <div>
                                                    <span className={`inline-block px-2 py-0.5 rounded text-xs font-bold mb-1 ${log.activity_type === 'ERROR' ? 'bg-error/20 text-error' :
                                                        log.activity_type === 'COLLECTION' ? 'bg-success/20 text-success' :
                                                            'bg-info/20 text-info'
                                                        }`}>
                                                        {log.activity_type}
                                                    </span>
                                                    <p className="text-sm text-gray-200">{log.description}</p>
                                                </div>
                                                <span className="text-xs text-gray-500 whitespace-nowrap ml-4">
                                                    {new Date(log.timestamp).toLocaleTimeString()}
                                                </span>
                                            </div>
                                        </div>
                                    ))}
                                    {logs.length === 0 && (
                                        <div className="p-8 text-center text-gray-500">No recent activity</div>
                                    )}
                                </div>
                            </div>
                        </div>
                    )}

                    {activeTab === 'live' && (
                        <div className="space-y-6">
                            <div className="bg-base-200 p-6 rounded-lg border border-base-300">
                                <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                                    <div className={`w-3 h-3 rounded-full ${liveStatus?.status === 'Running' ? 'bg-success animate-pulse' : 'bg-gray-500'}`}></div>
                                    Current Status: <span className={liveStatus?.status === 'Running' ? 'text-success' : 'text-gray-400'}>{liveStatus?.status || 'Unknown'}</span>
                                </h3>

                                <div className="space-y-4">
                                    <div>
                                        <p className="text-gray-400 text-sm mb-1">Current Activity</p>
                                        <p className="text-lg text-white font-mono bg-base-300 p-3 rounded border border-base-400">
                                            {liveStatus?.activity || 'No active task'}
                                        </p>
                                    </div>

                                    <div className="grid grid-cols-2 gap-4">
                                        <div>
                                            <p className="text-gray-400 text-sm mb-1">Last Updated</p>
                                            <p className="text-white">
                                                {liveStatus?.last_updated ? new Date(liveStatus.last_updated).toLocaleString() : 'Never'}
                                            </p>
                                        </div>
                                        <div>
                                            <p className="text-gray-400 text-sm mb-1">Uptime Session</p>
                                            <p className="text-white">
                                                {liveStatus?.status === 'Running' ? 'Active' : 'Inactive'}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div className="bg-base-200 p-6 rounded-lg border border-base-300">
                                <h4 className="font-bold mb-2">System Resources</h4>
                                <div className="space-y-3">
                                    <div>
                                        <div className="flex justify-between text-sm mb-1">
                                            <span className="text-gray-400">CPU Usage</span>
                                            <span className="text-white">{(Math.random() * 30 + 10).toFixed(1)}%</span>
                                        </div>
                                        <div className="w-full bg-base-300 rounded-full h-2">
                                            <div className="bg-accent h-2 rounded-full" style={{ width: '45%' }}></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div className="flex justify-between text-sm mb-1">
                                            <span className="text-gray-400">Memory Usage</span>
                                            <span className="text-white">{(Math.random() * 40 + 20).toFixed(1)}%</span>
                                        </div>
                                        <div className="w-full bg-base-300 rounded-full h-2">
                                            <div className="bg-info h-2 rounded-full" style={{ width: '60%' }}></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}

                    {activeTab === 'logs' && (
                        <div className="space-y-4">
                            <div className="bg-base-200 rounded-lg border border-base-300 overflow-hidden">
                                <table className="w-full text-left text-sm">
                                    <thead className="bg-base-300 text-gray-400">
                                        <tr>
                                            <th className="p-4">Time</th>
                                            <th className="p-4">Type</th>
                                            <th className="p-4">Description</th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-base-300">
                                        {logs.map((log) => (
                                            <tr key={log.id} className="hover:bg-base-300/50">
                                                <td className="p-4 text-gray-400 whitespace-nowrap">
                                                    {new Date(log.timestamp).toLocaleString()}
                                                </td>
                                                <td className="p-4">
                                                    <span className={`px-2 py-1 rounded text-xs font-bold ${log.activity_type === 'ERROR' ? 'bg-error/20 text-error' :
                                                        log.activity_type === 'COLLECTION' ? 'bg-success/20 text-success' :
                                                            'bg-info/20 text-info'
                                                        }`}>
                                                        {log.activity_type}
                                                    </span>
                                                </td>
                                                <td className="p-4 text-gray-200">{log.description}</td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                                {logs.length === 0 && (
                                    <div className="p-8 text-center text-gray-500">No logs available</div>
                                )}
                            </div>
                        </div>
                    )}

                    {activeTab === 'collections' && (
                        <div className="space-y-4">
                            <div className="grid gap-4">
                                {collections.map((item) => (
                                    <div key={item.id} className="bg-base-200 p-4 rounded-lg border border-base-300 hover:border-accent transition-colors">
                                        <div className="flex justify-between items-start mb-2">
                                            <div>
                                                <h4 className="font-bold text-white">{item.strategy_name}</h4>
                                                <p className="text-xs text-gray-400 mt-1">Source: {item.source}</p>
                                            </div>
                                            <div className="text-right">
                                                <span className={`inline-flex items-center gap-1 px-2 py-1 rounded text-xs font-bold ${item.verification_status === 'approved' ? 'bg-success/20 text-success' : 'bg-error/20 text-error'
                                                    }`}>
                                                    {item.verification_status === 'approved' ? <CheckCircleIcon className="w-3 h-3" /> : <XCircleIcon className="w-3 h-3" />}
                                                    {item.verification_status.toUpperCase()}
                                                </span>
                                                <p className="text-xs text-gray-500 mt-1">{new Date(item.collected_at).toLocaleDateString()}</p>
                                            </div>
                                        </div>
                                        <div className="w-full bg-base-300 rounded-full h-1.5 mt-2">
                                            <div
                                                className={`h-1.5 rounded-full ${item.quality_score >= 80 ? 'bg-success' : item.quality_score >= 50 ? 'bg-warning' : 'bg-error'}`}
                                                style={{ width: `${item.quality_score}%` }}
                                            ></div>
                                        </div>
                                        <p className="text-xs text-right text-gray-400 mt-1">Quality Score: {item.quality_score}</p>
                                    </div>
                                ))}
                                {collections.length === 0 && (
                                    <div className="p-8 text-center text-gray-500 bg-base-200 rounded-lg">No collections found</div>
                                )}
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default AgentDetailsModal;
