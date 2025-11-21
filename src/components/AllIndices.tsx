import React, { useState, useEffect } from 'react';

interface Index {
    name: string;
    symbol: string;
    ltp: number;
    ltpChng: number;
    ltpChngPercent: number;
    open: number;
    high: number;
    low: number;
    close: number;
    isFavorite?: boolean;
}

interface AllIndicesProps {
    onIndexClick?: (symbol: string, name: string) => void;
}

const AllIndices: React.FC<AllIndicesProps> = ({ onIndexClick }) => {
    const [activeTab, setActiveTab] = useState<'stock-discovery' | 'index-fno' | 'stocks-fno' | 'commodities' | 'all-indices' | 'news'>('all-indices');
    const [indianIndices, setIndianIndices] = useState<Index[]>([]);
    const [globalIndices, setGlobalIndices] = useState<Index[]>([]);
    const [showIndexMenu, setShowIndexMenu] = useState(false);
    const [selectedIndex, setSelectedIndex] = useState<string>('NIFTY');

    useEffect(() => {
        fetchIndices();
    }, []);

    const fetchIndices = async () => {
        try {
            const response = await fetch('http://localhost:5000/api/market/all-indices');
            const data = await response.json();

            if (data.indianIndices) {
                setIndianIndices(data.indianIndices);
            }
            if (data.globalIndices) {
                setGlobalIndices(data.globalIndices);
            }
        } catch (error) {
            console.error('Error fetching indices:', error);
        }
    };

    const toggleFavorite = (symbol: string, isIndian: boolean) => {
        if (isIndian) {
            setIndianIndices(prev => prev.map(idx =>
                idx.symbol === symbol ? { ...idx, isFavorite: !idx.isFavorite } : idx
            ));
        }
    };

    const renderIndexRow = (index: Index, isIndian: boolean = true) => {
        const isPositive = index.ltpChng >= 0;

        return (
            <tr
                key={index.symbol}
                className="border-b border-base-300 hover:bg-base-300 transition-colors cursor-pointer"
                onClick={() => onIndexClick?.(index.symbol, index.name)}
            >
                <td className="py-3 px-4">
                    <div className="flex items-center gap-2">
                        {isIndian && (
                            <button
                                onClick={(e) => {
                                    e.stopPropagation();
                                    toggleFavorite(index.symbol, true);
                                }}
                                className="text-warning hover:scale-110 transition-transform"
                            >
                                {index.isFavorite ? '★' : '☆'}
                            </button>
                        )}
                        <span className="font-semibold">{index.name}</span>
                    </div>
                </td>
                <td className="py-3 px-4 text-right font-bold">{index.ltp.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
                <td className={`py-3 px-4 text-right font-semibold ${isPositive ? 'text-accent' : 'text-danger'}`}>
                    {isPositive ? '+' : ''}{index.ltpChng.toFixed(2)}
                </td>
                <td className={`py-3 px-4 text-right font-semibold ${isPositive ? 'text-accent' : 'text-danger'}`}>
                    {isPositive ? '+' : ''}{index.ltpChngPercent.toFixed(2)}%
                </td>
                <td className="py-3 px-4 text-right">{index.open.toFixed(2)}</td>
                <td className="py-3 px-4 text-right text-accent">{index.high.toFixed(2)}</td>
                <td className="py-3 px-4 text-right text-danger">{index.low.toFixed(2)}</td>
                <td className="py-3 px-4 text-right">{index.close.toFixed(2)}</td>
                <td className="py-3 px-4">
                    <button className="text-info hover:underline text-sm font-semibold">VIEW COMPOSITION</button>
                </td>
            </tr>
        );
    };

    return (
        <div className="h-full overflow-y-auto bg-base-100">
            {/* Top Header with Index Selector */}
            <div className="bg-base-200 border-b border-base-300 p-4 flex items-center justify-between sticky top-0 z-10">
                <div className="flex items-center gap-4">
                    {/* Index Dropdown */}
                    <div className="relative">
                        <button
                            onClick={() => setShowIndexMenu(!showIndexMenu)}
                            className="flex items-center gap-2 px-4 py-2 bg-base-300 rounded hover:bg-base-100"
                        >
                            <span className="font-bold">{selectedIndex}</span>
                            <span className="text-accent">26,192.15 ▲</span>
                            <span className="text-accent text-sm">+139.50 (+0.54%)</span>
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                            </svg>
                        </button>

                        {/* Dropdown Menu */}
                        {showIndexMenu && (
                            <div className="absolute top-full mt-2 left-0 bg-base-200 border border-base-300 rounded-lg shadow-xl min-w-[200px] z-20">
                                <button className="w-full px-4 py-2 hover:bg-base-300 text-left flex items-center gap-2">
                                    <span>🔗</span> Option Chain
                                </button>
                                <button className="w-full px-4 py-2 hover:bg-base-300 text-left flex items-center gap-2">
                                    <span>📊</span> Charts
                                </button>
                                <button className="w-full px-4 py-2 hover:bg-base-300 text-left flex items-center gap-2">
                                    <span>📋</span> Stock Composition
                                </button>
                                <button className="w-full px-4 py-2 hover:bg-base-300 text-left flex items-center gap-2">
                                    <span>⭐</span> Favourite Strategies →
                                </button>
                            </div>
                        )}
                    </div>
                </div>

                {/* Right side buttons */}
                <div className="flex items-center gap-3">
                    <button className="px-4 py-2 hover:bg-base-300 rounded">Markets</button>
                    <button className="px-4 py-2 hover:bg-base-300 rounded">Watchlist</button>
                    <button className="px-4 py-2 hover:bg-base-300 rounded">Portfolio</button>
                    <button className="px-4 py-2 hover:bg-base-300 rounded">Orders</button>
                    <button className="px-4 py-2 hover:bg-base-300 rounded">Positions</button>
                    <button className="px-4 py-2 hover:bg-base-300 rounded">Tools</button>
                </div>
            </div>

            {/* Tabs */}
            <div className="flex gap-6 px-6 border-b border-base-300 bg-base-200">
                {[
                    { id: 'stock-discovery', label: 'Stock Discovery' },
                    { id: 'index-fno', label: 'Index F&O' },
                    { id: 'stocks-fno', label: 'Stocks F&O' },
                    { id: 'commodities', label: 'Commodities' },
                    { id: 'all-indices', label: 'All Indices' },
                    { id: 'news', label: 'News' },
                ].map((tab) => (
                    <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id as any)}
                        className={`py-3 font-semibold transition-colors ${activeTab === tab.id
                            ? 'text-info border-b-2 border-info'
                            : 'text-gray-400 hover:text-white'
                            }`}
                    >
                        {tab.label}
                    </button>
                ))}
            </div>

            {/* Content */}
            <div className="p-6">
                {/* Indian Indices Table */}
                <div className="mb-8">
                    <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                        Indian Indices
                        <span className="text-sm bg-base-300 px-2 py-1 rounded">{indianIndices.length}</span>
                    </h2>

                    <div className="bg-base-200 rounded-lg overflow-hidden">
                        <table className="w-full">
                            <thead className="bg-base-300">
                                <tr>
                                    <th className="py-3 px-4 text-left font-semibold">Name ↕</th>
                                    <th className="py-3 px-4 text-right font-semibold">LTP ↕</th>
                                    <th className="py-3 px-4 text-right font-semibold">LTP Chng ↕</th>
                                    <th className="py-3 px-4 text-right font-semibold">LTP Chng% ↕</th>
                                    <th className="py-3 px-4 text-right font-semibold">Open ↕</th>
                                    <th className="py-3 px-4 text-right font-semibold">High ↕</th>
                                    <th className="py-3 px-4 text-right font-semibold">Low ↕</th>
                                    <th className="py-3 px-4 text-right font-semibold">Close ↕</th>
                                    <th className="py-3 px-4 text-center font-semibold">Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                {indianIndices.map(index => renderIndexRow(index, true))}
                            </tbody>
                        </table>
                    </div>
                </div>

                {/* Global Indices Table */}
                <div>
                    <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                        Global Indices
                        <span className="text-sm bg-base-300 px-2 py-1 rounded">{globalIndices.length}</span>
                    </h2>

                    <div className="bg-base-200 rounded-lg overflow-hidden">
                        <table className="w-full">
                            <thead className="bg-base-300">
                                <tr>
                                    <th className="py-3 px-4 text-left font-semibold">Location / Index Name</th>
                                    <th className="py-3 px-4 text-right font-semibold">LTP ↕</th>
                                    <th className="py-3 px-4 text-right font-semibold">LTP Chng ↕</th>
                                    <th className="py-3 px-4 text-right font-semibold">LTP Chng% ↕</th>
                                    <th className="py-3 px-4 text-right font-semibold">Open</th>
                                    <th className="py-3 px-4 text-right font-semibold">High ↕</th>
                                    <th className="py-3 px-4 text-right font-semibold">Low ↕</th>
                                    <th className="py-3 px-4 text-right font-semibold">Close</th>
                                    <th className="py-3 px-4 text-center font-semibold">Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                {globalIndices.map(index => renderIndexRow(index, false))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AllIndices;
