import React, { useState, useEffect } from 'react';

interface TickerIndex {
    name: string;
    value: number;
    change: number;
    changePercent: number;
}

const TickerBar: React.FC = () => {
    const [indices, setIndices] = useState<TickerIndex[]>([]);

    useEffect(() => {
        fetchIndices();
        const interval = setInterval(fetchIndices, 3000); // Update every 3s
        return () => clearInterval(interval);
    }, []);

    const fetchIndices = async () => {
        try {
            const response = await fetch('http://localhost:5000/api/dashboard/ticker');
            if (response.ok) {
                const data = await response.json();
                setIndices(data.indices || []);
            }
        } catch (error) {
            console.error('Failed to fetch ticker:', error);
        }
    };

    return (
        <div className="bg-base-300 border-b border-base-100">
            <div className="flex items-center gap-8 px-6 py-2 overflow-x-auto">
                {indices.map((index) => {
                    const isPositive = index.change >= 0;
                    return (
                        <div
                            key={index.name}
                            className="flex items-center gap-2 whitespace-nowrap"
                        >
                            <span className="font-semibold text-sm">{index.name}</span>
                            <span className="font-bold">{index.value.toLocaleString('en-IN', { maximumFractionDigits: 2 })}</span>
                            <span className={`text-xs font-semibold ${isPositive ? 'text-accent' : 'text-danger'}`}>
                                {isPositive ? '+' : ''}{index.change.toFixed(2)} ({index.changePercent >= 0 ? '+' : ''}{index.changePercent.toFixed(2)}%)
                            </span>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default TickerBar;
