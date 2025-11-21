import { X, CheckCircle, AlertCircle, XCircle, ExternalLink, ClockIcon, Activity } from 'lucide-react';
import { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface AgentDetailModalProps {
    agentId: string;
    onClose: () => void;
}

interface AgentData {
    agent_id: string;
    name: string;
    type: string;
    specialty: string;
    status: string;
    stats: {
        total_collected: number;
        success_rate: number;
        avg_quality_score: number;
        uptime_percentage: number;
    };
    verification: {
        approved: number;
        warning: number;
        rejected: number;
        avg_confidence: number;
    };
    recent_collections: Array<{
        id: number;
        strategy_name: string;
        source_url: string;
        source: string;
        collected_at: string;
        quality_score: number;
        verification_status: string;
    }>;
    timeline: Array<{
        date: string;
        count: number;
    }>;
}

interface ActivityLog {
    agent_id: string;
    total_activities: number;
    activities: Array<{
        id: number;
        timestamp: string;
        type: string;
        action: string;
        strategy_name: string;
        source: string;
        source_url: string | null;
        status: string;
        quality_score: number;
        details: any;
    }>;
}

export function AgentDetailModal({ agentId, onClose }: AgentDetailModalProps) {
    const [data, setData] = useState<AgentData | null>(null);
    const [activityLog, setActivityLog] = useState<ActivityLog | null>(null);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState<'overview' | 'activity'>('overview');

    useEffect(() => {
        fetchAgentDetails();
        fetchActivityLog();
    }, [agentId]);

    const fetchAgentDetails = async () => {
        try {
            const response = await fetch(`/api/agents/${agentId}/details`);
            const result = await response.json();
            setData(result);
        } catch (error) {
            console.error('Failed to fetch agent details:', error);
        } finally {
            setLoading(false);
        }
    };

    const fetchActivityLog = async () => {
        try {
            const response = await fetch(`/api/agents/${agentId}/activity?limit=100`);
            const result = await response.json();
            setActivityLog(result);
        } catch (error) {
            console.error('Failed to fetch activity log:', error);
        }
    };

    if (loading) {
        return (
            <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
                <div className="bg-slate-900/95 rounded-lg p-8">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
                </div>
            </div>
        );
    }

    if (!data) {
        return null;
    }

    const getStatusColor = (status: string) => {
        if (status === 'approved') return 'text-green-400';
        if (status === 'rejected') return 'text-red-400';
        return 'text-yellow-400';
    };

    const getStatusIcon = (status: string) => {
        if (status === 'approved') return <CheckCircle className="w-4 h-4" />;
        if (status === 'rejected') return <XCircle className="w-4 h-4" />;
        return <AlertCircle className="w-4 h-4" />;
    };

    return (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
            <div className="bg-slate-900/95 border border-slate-700 rounded-lg w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col">
                {/* Header */}
                <div className="p-6 border-b border-slate-700 flex items-center justify-between">
                    <div>
                        <h2 className="text-2xl font-bold text-white">{data.name}</h2>
                        <p className="text-slate-400 mt-1">{data.type} • {data.specialty}</p>
                    </div>
                    <button
                        onClick={onClose}
                        className="p-2 hover:bg-slate-800 rounded-lg transition-colors"
                    >
                        <X className="w-6 h-6 text-slate-400" />
                    </button>
                </div>

                {/* Tabs */}
                <div className="border-b border-slate-700">
                    <div className="flex">
                        <button
                            onClick={() => setActiveTab('overview')}
                            className={`px-6 py-3 font-semibold transition-colors ${activeTab === 'overview'
                                    ? 'text-blue-400 border-b-2 border-blue-400'
                                    : 'text-slate-400 hover:text-white'
                                }`}
                        >
                            📊 Overview
                        </button>
                        <button
                            onClick={() => setActiveTab('activity')}
                            className={`px-6 py-3 font-semibold transition-colors ${activeTab === 'activity'
                                    ? 'text-blue-400 border-b-2 border-blue-400'
                                    : 'text-slate-400 hover:text-white'
                                }`}
                        >
                            📝 Activity Log ({activityLog?.total_activities || 0})
                        </button>
                    </div>
                </div>

                {/* Content */}
                <div className="flex-1 overflow-y-auto p-6">
                    {activeTab === 'overview' && (
                        <div className="space-y-6">
                            {/* Stats Cards */}
                            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                                <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-4">
                                    <div className="text-slate-400 text-sm mb-1">Total Collected</div>
                                    <div className="text-2xl font-bold text-white">{data.stats.total_collected}</div>
                                </div>
                                <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-4">
                                    <div className="text-slate-400 text-sm mb-1">Success Rate</div>
                                    <div className="text-2xl font-bold text-green-400">{data.stats.success_rate}%</div>
                                </div>
                                <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-4">
                                    <div className="text-slate-400 text-sm mb-1">Avg Quality</div>
                                    <div className="text-2xl font-bold text-blue-400">{data.stats.avg_quality_score}%</div>
                                </div>
                                <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-4">
                                    <div className="text-slate-400 text-sm mb-1">Uptime</div>
                                    <div className="text-2xl font-bold text-purple-400">{data.stats.uptime_percentage}%</div>
                                </div>
                            </div>

                            {/* Verification Breakdown */}
                            <div className="bg-slate-800/30 border border-slate-700 rounded-lg p-4">
                                <h3 className="text-lg font-semibold text-white mb-3">Multi-AI Verification</h3>
                                <div className="grid grid-cols-3 gap-4">
                                    <div className="flex items-center gap-2">
                                        <CheckCircle className="w-5 h-5 text-green-400" />
                                        <div>
                                            <div className="text-slate-400 text-sm">Approved</div>
                                            <div className="text-xl font-bold text-white">{data.verification.approved}</div>
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <AlertCircle className="w-5 h-5 text-yellow-400" />
                                        <div>
                                            <div className="text-slate-400 text-sm">Warning</div>
                                            <div className="text-xl font-bold text-white">{data.verification.warning}</div>
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <XCircle className="w-5 h-5 text-red-400" />
                                        <div>
                                            <div className="text-slate-400 text-sm">Rejected</div>
                                            <div className="text-xl font-bold text-white">{data.verification.rejected}</div>
                                        </div>
                                    </div>
                                </div>
                                <div className="mt-3 text-sm text-slate-400">
                                    Average Confidence: <span className="text-white font-semibold">{data.verification.avg_confidence}%</span>
                                </div>
                            </div>

                            {/* Activity Timeline Chart */}
                            {data.timeline && data.timeline.length > 0 && (
                                <div className="bg-slate-800/30 border border-slate-700 rounded-lg p-4">
                                    <h3 className="text-lg font-semibold text-white mb-3">Activity Timeline (Last 30 Days)</h3>
                                    <div className="h-64">
                                        <ResponsiveContainer width="100%" height="100%">
                                            <LineChart data={[...data.timeline].reverse()}>
                                                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                                                <XAxis
                                                    dataKey="date"
                                                    stroke="#94a3b8"
                                                    tick={{ fill: '#94a3b8', fontSize: 12 }}
                                                    tickFormatter={(value) => new Date(value).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                                                />
                                                <YAxis
                                                    stroke="#94a3b8"
                                                    tick={{ fill: '#94a3b8', fontSize: 12 }}
                                                />
                                                <Tooltip
                                                    contentStyle={{
                                                        backgroundColor: '#1e293b',
                                                        border: '1px solid #475569',
                                                        borderRadius: '8px',
                                                        color: '#fff'
                                                    }}
                                                    labelFormatter={(value) => new Date(value).toLocaleDateString()}
                                                />
                                                <Line
                                                    type="monotone"
                                                    dataKey="count"
                                                    stroke="#3b82f6"
                                                    strokeWidth={2}
                                                    dot={{ fill: '#3b82f6', r: 4 }}
                                                    activeDot={{ r: 6 }}
                                                    name="Collections"
                                                />
                                            </LineChart>
                                        </ResponsiveContainer>
                                    </div>
                                </div>
                            )}
                        </div>
                    )}

                    {activeTab === 'activity' && (
                        <div className="space-y-3">
                            <div className="flex items-center justify-between mb-4">
                                <h3 className="text-lg font-semibold text-white">
                                    Complete Activity Log ({activityLog?.total_activities || 0} activities)
                                </h3>
                            </div>

                            {activityLog && activityLog.activities.length > 0 ? (
                                <div className="space-y-2 max-h-[600px] overflow-y-auto">
                                    {activityLog.activities.map((activity) => (
                                        <div
                                            key={activity.id}
                                            className="bg-slate-800/50 border border-slate-700 rounded-lg p-4 hover:bg-slate-800 transition-colors"
                                        >
                                            <div className="flex items-start justify-between gap-3">
                                                <div className="flex-1">
                                                    <div className="flex items-center gap-2 mb-2">
                                                        <span className={`${getStatusColor(activity.status)}`}>
                                                            {getStatusIcon(activity.status)}
                                                        </span>
                                                        <span className="font-semibold text-white">{activity.strategy_name}</span>
                                                    </div>
                                                    <div className="text-sm text-slate-400 mb-2">
                                                        <ClockIcon className="w-3 h-3 inline mr-1" />
                                                        {new Date(activity.timestamp).toLocaleString()}
                                                    </div>
                                                    <div className="text-sm text-slate-300">
                                                        <span className="font-medium">Source:</span> {activity.source}
                                                    </div>
                                                </div>
                                                <div className="flex items-center gap-3">
                                                    <div className="text-right">
                                                        <div className="text-xs text-slate-400">Quality</div>
                                                        <div className={`text-sm font-semibold ${activity.quality_score >= 80 ? 'text-green-400' :
                                                                activity.quality_score >= 60 ? 'text-yellow-400' : 'text-red-400'
                                                            }`}>
                                                            {activity.quality_score}%
                                                        </div>
                                                    </div>
                                                    {activity.source_url && (
                                                        <a
                                                            href={activity.source_url}
                                                            target="_blank"
                                                            rel="noopener noreferrer"
                                                            className="p-2 hover:bg-slate-700 rounded-lg transition-colors"
                                                            title="View Source"
                                                        >
                                                            <ExternalLink className="w-4 h-4 text-blue-400" />
                                                        </a>
                                                    )}
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            ) : (
                                <div className="text-center text-slate-500 py-12">
                                    No activity recorded yet
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
