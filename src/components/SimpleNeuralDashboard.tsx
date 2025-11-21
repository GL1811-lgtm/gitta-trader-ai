import React, { useEffect, useState } from 'react';
import '../styles/futuristic.css';

interface AgentStatus {
    id: string;
    name: string;
    status: string;
    activity: string;
}

export default function SimpleNeuralDashboard() {
    const [loading, setLoading] = useState(false);

    return (
        <div style={{ padding: '20px', minHeight: '100vh', background: '#0a0e1a', color: '#e0e7ff' }}>
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
                    <div className="stat-value">5</div>
                </div>

                <div className="stat-card">
                    <div style={{ fontSize: '0.9rem', color: '#94a3b8', marginBottom: '8px' }}>Population</div>
                    <div className="stat-value">100</div>
                </div>

                <div className="stat-card">
                    <div style={{ fontSize: '0.9rem', color: '#94a3b8', marginBottom: '8px' }}>Best Fitness</div>
                    <div className="stat-value">0.8523</div>
                </div>

                <div className="stat-card">
                    <div style={{ fontSize: '0.9rem', color: '#94a3b8', marginBottom: '8px' }}>Avg Fitness</div>
                    <div className="stat-value">0.6234</div>
                </div>
            </div>

            {/* Active Agents Grid */}
            <div>
                <h2 style={{ color: '#00f3ff', fontSize: '1.8rem', marginBottom: '20px', textAlign: 'center' }}>
                    Active Agents
                </h2>
                <div className="agent-grid">
                    <div className="glass-card" style={{ padding: '20px' }}>
                        <h3 style={{ color: '#e0e7ff', fontSize: '1.1rem' }}>NSE Data Collector</h3>
                        <div style={{ fontSize: '0.9rem', color: '#10b981', marginTop: '10px' }}>Status: Active</div>
                    </div>
                    <div className="glass-card" style={{ padding: '20px' }}>
                        <h3 style={{ color: '#e0e7ff', fontSize: '1.1rem' }}>Scalper Strategy</h3>
                        <div style={{ fontSize: '0.9rem', color: '#10b981', marginTop: '10px' }}>Status: Active</div>
                    </div>
                    <div className="glass-card" style={{ padding: '20px' }}>
                        <h3 style={{ color: '#e0e7ff', fontSize: '1.1rem' }}>Swing Trader</h3>
                        <div style={{ fontSize: '0.9rem', color: '#10b981', marginTop: '10px' }}>Status: Active</div>
                    </div>
                </div>
            </div>
        </div>
    );
}
