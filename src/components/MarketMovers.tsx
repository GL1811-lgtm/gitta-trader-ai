import React, { useState, useEffect } from 'react';

interface Stock {
    symbol: string;
    name: string;
    price: number;
    change: number;
    changePercent: number;
    volume: number;
}

type TabType = 'gainers' | 'losers' | 'volume';

interface MarketMoversProps {
    onStockClick?: (symbol: string, name: string) => void;
    onViewAll?: () => void;
}

const MarketMovers: React.FC<MarketMoversProps> = ({ onStockClick, onViewAll }) => {
    const [activeTab, setActiveTab] = useState<TabType>('gainers');
    const [index, setIndex] = useState('NIFTY 100');
    const [gainers, setGainers] = useState<Stock[]>([]);
    const [losers, setLosers] = useState<Stock[]>([]);
    const [volumeShockers, setVolumeShockers] = useState<Stock[]>([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        fetchMarketMovers();
        const interval = setInterval(fetchMarketMovers, 10000); // Update every 10s
        return () => clearInterval(interval);
    }, [index]);

    const fetchMarketMovers = async () => {
        setLoading(true);
        try {
            const response = await fetch(`http://localhost:5000/api/market/movers?index=${index}`);
            if (response.ok) {
                const data = await response.json();
                setGainers(data.gainers || []);
                setLosers(data.losers || []);
                setVolumeShockers(data.volumeShockers || []);
            }
        } catch (error) {
            console.error('Failed to fetch market movers:', error);
        } finally {
            setLoading(false);
        }
    };

    const currentStocks = activeTab === 'gainers' ? gainers : activeTab === 'losers' ? losers : volumeShockers;

    const renderStockRow = (stock: Stock) => {
        const isPositive = stock.change >= 0;

        return (
            <div key={stock.symbol} className="flex items-center py-3 border-b border-base-300 last:border-b-0 hover:bg-base-300 transition-colors px-2 rounded">
                {/* Company Logo & Name */}
                <div className="flex items-center gap-3 flex-1 min-w-0">
                    <div className="w-10 h-10 rounded-full bg-base-300 flex items-center justify-center flex-shrink-0">
                        <span className="text-xs font-bold">{stock.symbol.slice(0, 2)}</span>
                    </div>
                    <div className="flex-1 min-w-0">
                        <div className="font-semibold text-sm truncate">{stock.name}</div>
                    </div>
                </div>

                {/* Market Price */}
                <div className="text-right w-32">
                    <div className="font-bold text-base">₹{stock.price.toLocaleString('en-IN', { maximumFractionDigits: 2 })}</div>
                    <div className={`text-sm font-semibold ${isPositive ? 'text-accent' : 'text-danger'}`}>
                        {isPositive ? '+' : ''}{stock.change.toFixed(2)} ({stock.changePercent.toFixed(2)}%)
                    </div>
                </div>

                {/* Volume */}
                <div className="text-right w-28 hidden lg:block">
                    <div className="text-xs text-gray-400">VOLUME</div>
                    <div className="text-sm font-semibold">{(stock.volume / 100000).toFixed(2)}L</div>
                </div>
            </div>
        );
    };

    return (
        <div className="bg-base-200 rounded-lg p-6">
            <div className="flex justify-between items-center mb-4">
                <h3 className="text-xl font-bold">Top market movers</h3>

                {/* Index Selector */}
                <select
                    value={index}
                    onChange={(e) => setIndex(e.target.value)}
                    className="bg-base-300 px-3 py-2 rounded text-sm border border-gray-600 focus:outline-none focus:ring-2 focus:ring-accent"
                >
                    <option value="NIFTY 50">NIFTY 50</option>
                    <option value="NIFTY 100">NIFTY 100</option>
                    <option value="NIFTY 500">NIFTY 500</option>
                </select>
            </div>

            {/* Tabs */}
            <div className="flex gap-6 mb-4 border-b border-base-300">
                <button
                    onClick={() => setActiveTab('gainers')}
                    className={`pb-2 font-semibold transition-colors ${activeTab === 'gainers'
                        ? 'text-accent border-b-2 border-accent'
                        : 'text-gray-400 hover:text-gray-200'
                        }`}
                >
                    Gainers
                </button>
                <button
                    onClick={() => setActiveTab('losers')}
                    className={`pb-2 font-semibold transition-colors ${activeTab === 'losers'
                        ? 'text-danger border-b-2 border-danger'
                        : 'text-gray-400 hover:text-gray-200'
                        }`}
                >
                    Losers
                </button>
                <button
                    onClick={() => setActiveTab('volume')}
                    className={`pb-2 font-semibold transition-colors ${activeTab === 'volume'
                        ? 'text-info border-b-2 border-info'
                        : 'text-gray-400 hover:text-gray-200'
                        }`}
                >
                    Volume shockers
                </button>
            </div>

            {/* Header Row */}
            <div className="flex items-center py-2 text-xs text-gray-400 font-semibold border-b border-base-300 px-2">
                <div className="flex-1">COMPANY</div>
                <div className="text-right w-32">MARKET PRICE (1D)</div>
                <div className="text-right w-28 hidden lg:block">VOLUME</div>
            </div>

            {/* Stock List */}
            <div className="mt-2">
                {loading ? (
                    <div className="flex justify-center py-8">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-accent"></div>
                    </div>
                ) : currentStocks.length > 0 ? (
                    currentStocks.map(renderStockRow)
                ) : (
                    <div className="text-center py-8 text-gray-400">
                        No data available
                    </div>
                )}
            </div>

            {/* View All Button */}
            {currentStocks.length > 0 && (
                <button
                    onClick={onViewAll}
                    className="w-full mt-4 py-2 text-accent hover:bg-base-300 rounded transition-colors font-semibold"
                >
                    View all →
                </button>
            )}
        </div>
    );
};

export default MarketMovers;
