import React, { useEffect, useState } from 'react';
import '../styles/futuristic.css';
import Evolution3D from './Evolution3D';
import { api } from '../services/api';

interface AgentStatus {
    id: string;
    name: string;
    status: string;
    activity: string;
}

interface EvolutionStatus {
    generation: number;
    population_size: number;
    best_fitness: number;
    avg_fitness: number;
}

export default function NeuralDashboard() {
    const [agents, setAgents] = useState<AgentStatus[]>([]);
    const [evolution, setEvolution] = useState<EvolutionStatus | null>(null);
    const [organisms, setOrganisms] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, 5000); // Update every 5 seconds
        return () => clearInterval(interval);
    }, []);

    const fetchData = async () => {
        try {
            // Fetch agent statuses
            const agentData = await api.getActiveAgents();
            setAgents(agentData);

            // Fetch evolution status
            const evolutionResp = await fetch('http://localhost:5000/api/evolution/status');
            const evolutionData = await evolutionResp.json();
            setEvolution(evolutionData);

            // Generate mock organisms for 3D viz (in production, fetch from API)
            const mockOrganisms = Array.from({ length: 20 }, (_, i) => ({
                id: `org_${i}`,
                fitness: Math.random(),
                generation: evolutionData.generation || 0,
                energy: Math.random() * 100
            }));
            setOrganisms(mockOrganisms);

            setLoading(false);
        } catch (error) {
            console.error('Error fetching data:', error);
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
                <div className="neural-spinner"></div>
            </div>
        );
    }

    return (
        <div style={{ padding: '20px', minHeight: '100vh', background: '#0a0e1a' }}>
            {/* Neural Grid Background */}
            <div className="neural-grid"></div>

            {/* Header */}
            <header style={{ marginBottom: '40px', textAlign: 'center' }}>
                <h1 className="neon-text" style={{ fontSize: '3rem', marginBottom: '10px' }}>
                    GITTA TRADER AI V2.0
                </h1>
                <p style={{ color: '#94a3b8', fontSize: '1.1rem' }}>
                    Neural Evolution Trading System
                </p>
            </header>

            {/* Evolution Stats Cards */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '20px', marginBottom: '40px' }}>
                <div className="stat-card">
                    <div style={{ fontSize: '0.9rem', color: '#94a3b8', marginBottom: '8px' }}>Generation</div>
                    <div className="stat-value">{evolution?.generation || 0}</div>
                </div>

                <div className="stat-card">
                    <div style={{ fontSize: '0.9rem', color: '#94a3b8', marginBottom: '8px' }}>Population</div>
                    <div className="stat-value">{evolution?.population_size || 0}</div>
                </div>

                <div className="stat-card">
                    <div style={{ fontSize: '0.9rem', color: '#94a3b8', marginBottom: '8px' }}>Best Fitness</div>
                    <div className="stat-value">{evolution?.best_fitness?.toFixed(4) || '0.0000'}</div>
                </div>

                <div className="stat-card">
                    <div style={{ fontSize: '0.9rem', color: '#94a3b8', marginBottom: '8px' }}>Avg Fitness</div>
                    <div className="stat-value">{evolution?.avg_fitness?.toFixed(4) || '0.0000'}</div>
                </div>
            </div>

            {/* 3D Evolution Visualizer */}
            <div style={{ marginBottom: '40px' }}>
                <Evolution3D organisms={organisms} currentGeneration={evolution?.generation || 0} />
            </div>

            {/* Active Agents Grid */}
            <div>
                <h2 style={{ color: '#00f3ff', fontSize: '1.8rem', marginBottom: '20px', textAlign: 'center' }}>
                    Active Agents
                </h2>
                <div className="agent-grid">
                    {agents.length > 0 ? (
                        agents.map((agent) => (
                            <div key={agent.id} className="glass-card" style={{ padding: '20px' }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                                    <h3 style={{ color: '#e0e7ff', fontSize: '1.1rem', margin: 0 }}>{agent.name}</h3>
                                    <div
                                        style={{
                                            width: '8px',
                                            height: '8px',
                                            borderRadius: '50%',
                                            background: agent.status === 'active' ? '#10b981' : '#94a3b8',
                                            boxShadow: agent.status === 'active' ? '0 0 10px #10b981' : 'none'
                                        }}
                                    ></div>
                                </div>
                                <div style={{ fontSize: '0.9rem', color: '#94a3b8', marginBottom: '8px' }}>
                                    Status: <span style={{ color: agent.status === 'active' ? '#10b981' : '#94a3b8' }}>{agent.status}</span>
                                </div>
                                <div className="data-stream" style={{ fontSize: '0.85rem', color: '#64748b', paddingTop: '8px' }}>
                                    {agent.activity || 'Idle'}
                                </div>
                            </div>
                        ))
                    ) : (
                        <div className="glass-card" style={{ padding: '40px', textAlign: 'center', gridColumn: '1 / -1' }}>
                            <p style={{ color: '#94a3b8' }}>No active agents found</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
