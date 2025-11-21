import React, { useState, useEffect } from 'react';
import { HolographicCard } from '../ui/HolographicCard';
import { NeonButton } from '../ui/NeonButton';
import { Evolution3D } from '../visualizers/Evolution3D';
import { PerformanceChart } from '../charts/PerformanceChart';
import { api } from '../../services/api';
import { Activity, Brain, Zap, Shield, Terminal } from 'lucide-react';

export const NeuralDashboard: React.FC = () => {
    const [evolutionStatus, setEvolutionStatus] = useState<any>(null);
    const [activeAgents, setActiveAgents] = useState<any[]>([]);
    const [isEvolving, setIsEvolving] = useState(false);

    const fetchData = async () => {
        try {
            const status = await api.getEvolutionStatus();
            setEvolutionStatus(status);

            const agents = await api.getActiveAgents();
            if (agents) {
                setActiveAgents(agents);
            }
        } catch (error) {
            console.error("Failed to fetch dashboard data:", error);
        }
    };

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, 2000); // Poll every 2 seconds
        return () => clearInterval(interval);
    }, []);

    const handleEvolve = async () => {
        setIsEvolving(true);
        try {
            await api.evolve();
            await fetchData(); // Refresh immediately
        } catch (error) {
            console.error("Evolution failed:", error);
        } finally {
            setIsEvolving(false);
        }
    };

    // Filter for collectors and testers
    const collectors = activeAgents.filter(a => a.type === 'Collector');
    const testers = activeAgents.filter(a => a.type === 'Tester');

    return (
        <div className="min-h-screen bg-[var(--bg-dark)] text-white p-8 relative overflow-hidden">
            {/* Background Grid */}
            <div className="absolute inset-0 bg-[linear-gradient(rgba(0,243,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(0,243,255,0.03)_1px,transparent_1px)] bg-[size:40px_40px] pointer-events-none" />

            {/* Header */}
            <header className="flex justify-between items-center mb-8 relative z-10">
                <div>
                    <h1 className="text-5xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-r from-[var(--neon-cyan)] to-[var(--neon-purple)]">
                        GITTA TRADER <span className="text-white text-2xl font-light">V2.0</span>
                    </h1>
                    <p className="text-[var(--text-secondary)] mt-2 tracking-widest uppercase text-sm">
                        Autonomous Neural Trading System
                    </p>
                </div>
                <div className="flex gap-4">
                    <NeonButton variant="cyan">System Status: ONLINE</NeonButton>
                    <NeonButton variant="danger">Emergency Stop</NeonButton>
                </div>
            </header>

            {/* Main Grid */}
            <div className="grid grid-cols-12 gap-6 relative z-10">

                {/* Left Column: Stats */}
                <div className="col-span-3 space-y-6">
                    <HolographicCard title="Evolution Engine">
                        <div className="space-y-4">
                            <div className="flex justify-between items-center">
                                <span className="text-gray-400">Generation</span>
                                <span className="text-2xl font-mono text-[var(--neon-cyan)]">#{evolutionStatus?.generation || 0}</span>
                            </div>
                            <div className="flex justify-between items-center">
                                <span className="text-gray-400">Best Fitness</span>
                                <span className="text-2xl font-mono text-[var(--neon-green)]">{(evolutionStatus?.best_fitness || 0).toFixed(4)}</span>
                            </div>
                            <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
                                <div className={`h-full bg-[var(--neon-purple)] w-3/4 ${isEvolving ? 'animate-pulse' : ''}`} />
                            </div>
                            {isEvolving && <p className="text-xs text-[var(--neon-purple)] text-center animate-pulse">EVOLVING...</p>}
                        </div>
                    </HolographicCard>

                    <HolographicCard title="Active Collectors">
                        <div className="space-y-3 max-h-[300px] overflow-y-auto custom-scrollbar">
                            {collectors.length > 0 ? collectors.map((agent) => (
                                <div key={agent.id} className="flex items-center gap-3 p-2 rounded bg-white/5">
                                    <div className={`w-2 h-2 rounded-full ${agent.status === 'Active' ? 'bg-[var(--neon-green)] animate-pulse' : 'bg-gray-500'}`} />
                                    <div className="flex flex-col">
                                        <span className="text-sm font-medium">{agent.name}</span>
                                        <span className="text-xs text-gray-400">{agent.activity || agent.status}</span>
                                    </div>
                                </div>
                            )) : (
                                <p className="text-sm text-gray-500">No active collectors</p>
                            )}
                        </div>
                    </HolographicCard>
                </div>

                {/* Center Column: Visualizer */}
                <div className="col-span-6 space-y-6">
                    <HolographicCard className="h-[400px] flex items-center justify-center border-[var(--neon-cyan)] p-0 overflow-hidden">
                        <Evolution3D />
                    </HolographicCard>
                    <PerformanceChart />
                </div>

                {/* Right Column: Logs & Actions */}
                <div className="col-span-3 space-y-6">
                    <HolographicCard title="System Logs" className="h-[400px]">
                        <div className="font-mono text-xs space-y-2 text-gray-400 h-full overflow-y-auto custom-scrollbar">
                            <p><span className="text-[var(--neon-cyan)]">[SYSTEM]</span> Dashboard initialized</p>
                            {evolutionStatus && <p><span className="text-[var(--neon-green)]">[EVO]</span> Gen #{evolutionStatus.generation} active</p>}
                            {collectors.map(c => (
                                <p key={`log-${c.id}`}><span className="text-[var(--neon-blue)]">[DATA]</span> {c.name}: {c.status}</p>
                            ))}
                        </div>
                    </HolographicCard>

                    <HolographicCard title="Control Deck">
                        <div className="grid grid-cols-2 gap-4">
                            <NeonButton variant="purple" className="text-xs" onClick={handleEvolve} disabled={isEvolving}>
                                {isEvolving ? 'Evolving...' : 'Evolve'}
                            </NeonButton>
                            <NeonButton variant="cyan" className="text-xs">Backtest</NeonButton>
                        </div>
                    </HolographicCard>
                </div>

            </div>
        </div>
    );
};

