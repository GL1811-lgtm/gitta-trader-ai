import React, { useState, useEffect } from 'react';

interface Screen {
    id: string;
    name: string;
    type: 'Bullish' | 'Bearish';
    count: number;
    icon: string;
}

interface TradingScreensProps {
    onViewAll?: () => void;
}

const TradingScreens: React.FC<TradingScreensProps> = ({ onViewAll }) => {
    const [screens, setScreens] = useState<Screen[]>([]);

    useEffect(() => {
        fetchScreens();
        const interval = setInterval(fetchScreens, 30000);
        return () => clearInterval(interval);
    }, []);

    const fetchScreens = async () => {
        try {
            const response = await fetch('http://localhost:5000/api/dashboard/screens');
            if (response.ok) {
                const data = await response.json();
                setScreens(data.screens || []);
            }
        } catch (error) {
            console.error('Failed to fetch trading screens:', error);
        }
    };

    const getScreenIcon = (name: string) => {
        if (name.includes('Resistance')) return '📈';
        if (name.includes('MACD')) return '📊';
        if (name.includes('RSI')) return '📉';
        if (name.includes('Support')) return '🎯';
        return '💹';
    };

    return (
        <div className="bg-base-200 rounded-lg p-6">
            <h3 className="text-xl font-bold mb-4">Trading Screens</h3>

            <div className="space-y-3">
                {screens.map((screen) => (
                    <button
                        key={screen.id}
                        className="w-full bg-base-300 hover:bg-base-100 p-4 rounded-lg transition-colors flex items-center justify-between group"
                    >
                        <div className="flex items-center gap-4">
                            <span className={`px-3 py-1 rounded text-xs font-bold ${screen.type === 'Bullish' ? 'bg-accent/20 text-accent' : 'bg-danger/20 text-danger'
                                }`}>
                                {screen.type}
                            </span>
                            <span className="font-semibold text-left">{screen.name}</span>
                        </div>

                        <div className="flex items-center gap-3">
                            <span className="text-2xl">{getScreenIcon(screen.name)}</span>
                            <span className="text-gray-400 group-hover:text-gray-200 transition-colors">→</span>
                        </div>
                    </button>
                ))}
            </div>

            <button
                onClick={onViewAll}
                className="w-full mt-4 py-2 text-accent hover:bg-base-300 rounded transition-colors font-semibold"
            >
                View all screeners →
            </button>
        </div>
    );
};

export default TradingScreens;
