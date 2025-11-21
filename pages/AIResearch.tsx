import React, { useState } from 'react';

interface AIResponse {
    model_name: string;
    role: string;
    specialty: string;
    content: string;
    success: boolean;
    duration: number;
    weight: number;
}

interface Consensus {
    average_score: number;
    weighted_average_score: number;
    consensus_recommendation: string;
    agreement_rate: number;
    confidence: number;
    interpretation: string;
    all_scores: number[];
}

interface VerificationResult {
    total_models: number;
    successful_responses: number;
    failed_responses: number;
    total_duration: number;
    responses: AIResponse[];
}

export default function AIResearch() {
    const [strategy, setStrategy] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<any>(null);
    const [error, setError] = useState('');

    const handleVerify = async () => {
        if (!strategy.trim()) {
            setError('Please enter a trading strategy');
            return;
        }

        setLoading(true);
        setError('');
        setResult(null);

        try {
            const response = await fetch('http://localhost:5001/api/ai/verify', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ strategy }),
            });

            if (!response.ok) {
                throw new Error('Verification failed');
            }

            const data = await response.json();
            setResult(data);
        } catch (err: any) {
            setError(err.message || 'Failed to verify strategy');
        } finally {
            setLoading(false);
        }
    };

    const loadDemo = async () => {
        setLoading(true);
        setError('');
        setResult(null);

        try {
            const response = await fetch('http://localhost:5001/api/demo/multi-ai-research');

            if (!response.ok) {
                throw new Error('Demo failed to load');
            }

            const data = await response.json();
            setStrategy(data.strategy);
            setResult(data);
        } catch (err: any) {
            setError(err.message || 'Failed to load demo');
        } finally {
            setLoading(false);
        }
    };

    const getScoreColor = (score: number) => {
        if (score >= 7.5) return 'text-green-400';
        if (score >= 5.5) return 'text-yellow-400';
        return 'text-red-400';
    };

    const getRecommendationColor = (rec: string) => {
        if (rec === 'VIABLE') return 'bg-green-500/20 text-green-400 border-green-500/30';
        if (rec === 'MODERATE') return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
        return 'bg-red-500/20 text-red-400 border-red-500/30';
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 px-6 py-8">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-4xl font-bold text-white mb-2">
                        🤖 Multi-AI Strategy Verification
                    </h1>
                    <p className="text-slate-400">
                        Verify trading strategies using 8 different AI models for consensus analysis
                    </p>
                </div>

                {/* Input Section */}
                <div className="bg-slate-800/50 backdrop-blur-sm rounded-2xl border border-slate-700 p-6 mb-6">
                    <label className="block text-sm font-medium text-slate-300 mb-3">
                        Enter Trading Strategy
                    </label>
                    <textarea
                        value={strategy}
                        onChange={(e) => setStrategy(e.target.value)}
                        placeholder="Example: Buy when RSI < 30, sell when RSI > 70..."
                        className="w-full h-40 px-4 py-3 bg-slate-900/50 border border-slate-600 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                    />

                    <div className="flex gap-4 mt-4">
                        <button
                            onClick={handleVerify}
                            disabled={loading}
                            className="px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-semibold rounded-xl transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {loading ? '🔄 Analyzing...' : '✨ Verify Strategy'}
                        </button>

                        <button
                            onClick={loadDemo}
                            disabled={loading}
                            className="px-6 py-3 bg-slate-700 hover:bg-slate-600 text-white font-semibold rounded-xl transition-all duration-200 disabled:opacity-50"
                        >
                            📋 Load Demo
                        </button>
                    </div>

                    {error && (
                        <div className="mt-4 px-4 py-3 bg-red-500/10 border border-red-500/30 rounded-xl text-red-400">
                            ❌ {error}
                        </div>
                    )}
                </div>

                {/* Loading State */}
                {loading && (
                    <div className="bg-slate-800/50 backdrop-blur-sm rounded-2xl border border-slate-700 p-12 text-center">
                        <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-blue-500 border-t-transparent mb-4"></div>
                        <p className="text-slate-300 text-lg">
                            Calling 8 AI models in parallel...
                        </p>
                        <p className="text-slate-500 text-sm mt-2">
                            This may take 6-10 seconds
                        </p>
                    </div>
                )}

                {/* Results Section */}
                {result && !loading && (
                    <>
                        {/* Consensus Summary */}
                        {result.consensus && (
                            <div className="bg-gradient-to-br from-slate-800/70 to-slate-900/70 backdrop-blur-sm rounded-2xl border border-slate-600 p-8 mb-6">
                                <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
                                    <span className="text-3xl">🎯</span>
                                    Consensus Result
                                </h2>

                                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
                                    <div className="bg-slate-900/50 rounded-xl p-4 border border-slate-700">
                                        <div className="text-slate-400 text-sm mb-1">Average Score</div>
                                        <div className={`text-3xl font-bold ${getScoreColor(result.consensus.average_score)}`}>
                                            {result.consensus.average_score}/10
                                        </div>
                                    </div>

                                    <div className="bg-slate-900/50 rounded-xl p-4 border border-slate-700">
                                        <div className="text-slate-400 text-sm mb-1">Weighted Score</div>
                                        <div className={`text-3xl font-bold ${getScoreColor(result.consensus.weighted_average_score)}`}>
                                            {result.consensus.weighted_average_score}/10
                                        </div>
                                    </div>

                                    <div className="bg-slate-900/50 rounded-xl p-4 border border-slate-700">
                                        <div className="text-slate-400 text-sm mb-1">Agreement</div>
                                        <div className="text-3xl font-bold text-blue-400">
                                            {result.consensus.agreement_rate}%
                                        </div>
                                    </div>

                                    <div className="bg-slate-900/50 rounded-xl p-4 border border-slate-700">
                                        <div className="text-slate-400 text-sm mb-1">Confidence</div>
                                        <div className="text-3xl font-bold text-purple-400">
                                            {result.consensus.confidence}%
                                        </div>
                                    </div>
                                </div>

                                <div className="flex items-center gap-4 flex-wrap">
                                    <span className="text-slate-400">Recommendation:</span>
                                    <span className={`px-6 py-2 rounded-xl font-bold border ${getRecommendationColor(result.consensus.consensus_recommendation)}`}>
                                        {result.consensus.consensus_recommendation}
                                    </span>
                                </div>

                                <div className="mt-4 p-4 bg-slate-900/30 rounded-xl border border-slate-700">
                                    <p className="text-slate-300">{result.consensus.interpretation}</p>
                                </div>
                            </div>
                        )}

                        {/* AI Responses */}
                        {result.verification && (
                            <div className="bg-slate-800/50 backdrop-blur-sm rounded-2xl border border-slate-700 p-8">
                                <div className="flex items-center justify-between mb-6">
                                    <h2 className="text-2xl font-bold text-white flex items-center gap-3">
                                        <span className="text-3xl">🤖</span>
                                        AI Model Responses
                                    </h2>
                                    <div className="text-slate-400">
                                        {result.verification.successful_responses}/{result.verification.total_models} successful
                                        <span className="ml-4 text-slate-500">
                                            {result.verification.total_duration.toFixed(2)}s
                                        </span>
                                    </div>
                                </div>

                                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                                    {result.verification.responses.filter((r: AIResponse) => r.success).map((response: AIResponse, index: number) => (
                                        <div key={index} className="bg-slate-900/50 rounded-xl border border-slate-700 p-5 hover:border-blue-500/50 transition-all">
                                            <div className="flex items-start justify-between mb-3">
                                                <div>
                                                    <h3 className="text-lg font-semibold text-white">
                                                        {response.model_name}
                                                    </h3>
                                                    <p className="text-sm text-slate-400 capitalize">{response.role.replace(/_/g, ' ')}</p>
                                                </div>
                                                <div className="text-right">
                                                    <div className="text-xs text-slate-500">
                                                        {response.duration.toFixed(2)}s
                                                    </div>
                                                    <div className="text-xs text-blue-400">
                                                        Weight: {response.weight}x
                                                    </div>
                                                </div>
                                            </div>

                                            <div className="bg-slate-950/50 rounded-lg p-4 border border-slate-800">
                                                <p className="text-slate-300 text-sm leading-relaxed whitespace-pre-wrap">
                                                    {response.content}
                                                </p>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </>
                )}
            </div>
        </div>
    );
}
