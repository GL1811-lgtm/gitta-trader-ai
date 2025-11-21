import React, { useEffect, useRef, useState } from 'react';

interface StockChartModalProps {
    symbol: string;
    name: string;
    onClose: () => void;
}

const StockChartModal: React.FC<StockChartModalProps> = ({ symbol, name, onClose }) => {
    const chartContainerRef = useRef<HTMLDivElement>(null);
    const [watchlist, setWatchlist] = useState<string[]>([]);
    const [showWatchlist, setShowWatchlist] = useState(true);

    useEffect(() => {
        // Load TradingView widget
        if (chartContainerRef.current) {
            const script = document.createElement('script');
            script.src = 'https://s3.tradingview.com/tv.js';
            script.async = true;
            script.onload = () => {
                if (window.TradingView) {
                    new window.TradingView.widget({
                        container_id: 'tradingview_chart',
                        autosize: true,
                        symbol: `NSE:${symbol}`,
                        interval: '5',
                        timezone: 'Asia/Kolkata',
                        theme: 'dark',
                        style: '1',
                        locale: 'en',
                        toolbar_bg: '#1e222d',
                        enable_publishing: false,
                        hide_side_toolbar: false,
                        allow_symbol_change: true,
                        studies: ['RSI@tv-basicstudies', 'MACD@tv-basicstudies'],
                        save_image: false,
                    });
                }
            };
            document.body.appendChild(script);
        }

        // Load mock watchlist
        setWatchlist(['RELIANCE', 'TCS', 'INFY', 'HDFCBANK', 'ICICIBANK']);
    }, [symbol]);

    const addToWatchlist = () => {
        if (!watchlist.includes(symbol)) {
            setWatchlist([...watchlist, symbol]);
        }
    };

    return (
        <div className="fixed inset-0 z-50 bg-black bg-opacity-90 flex">
            {/* Main Chart Area */}
            <div className="flex-1 flex flex-col">
                {/* Header */}
                <div className="bg-base-300 p-4 flex items-center justify-between border-b border-base-100">
                    <div className="flex items-center gap-4">
                        <h2 className="text-2xl font-bold">{symbol}</h2>
                        <div className="flex gap-2">
                            <button className="px-3 py-1 bg-base-200 rounded text-sm hover:bg-base-100">5m</button>
                            <button className="px-3 py-1 bg-base-200 rounded text-sm hover:bg-base-100">1h</button>
                            <button className="px-3 py-1 bg-base-200 rounded text-sm hover:bg-base-100">1d</button>
                            <button className="px-3 py-1 bg-base-200 rounded text-sm hover:bg-base-100">1w</button>
                        </div>
                    </div>

                    <div className="flex items-center gap-3">
                        <button
                            onClick={addToWatchlist}
                            className="px-4 py-2 bg-accent text-white rounded hover:bg-accent/80 text-sm font-semibold"
                        >
                            + Watchlist
                        </button>
                        <button
                            onClick={onClose}
                            className="p-2 hover:bg-base-200 rounded transition-colors"
                        >
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>
                </div>

                {/* Chart Container */}
                <div ref={chartContainerRef} className="flex-1 bg-base-200">
                    <div id="tradingview_chart" className="w-full h-full"></div>
                </div>
            </div>

            {/* Right Sidebar - Watchlist */}
            {showWatchlist && (
                <div className="w-80 bg-base-300 border-l border-base-100 overflow-y-auto">
                    <div className="p-4">
                        <div className="flex items-center justify-between mb-4">
                            <h3 className="font-bold text-lg">Watchlist</h3>
                            <button
                                onClick={() => setShowWatchlist(false)}
                                className="p-1 hover:bg-base-200 rounded"
                            >
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                                </svg>
                            </button>
                        </div>

                        <div className="space-y-2">
                            {watchlist.map((stock) => (
                                <div
                                    key={stock}
                                    className="p-3 bg-base-200 rounded hover:bg-base-100 cursor-pointer transition-colors"
                                >
                                    <div className="font-semibold">{stock}</div>
                                    <div className="text-sm text-gray-400">NSE</div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}

            {/* Watchlist Toggle Button (when hidden) */}
            {!showWatchlist && (
                <button
                    onClick={() => setShowWatchlist(true)}
                    className="absolute right-4 top-20 p-2 bg-base-300 rounded-l hover:bg-base-200"
                >
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                </button>
            )}
        </div>
    );
};

// Declare TradingView on window
declare global {
    interface Window {
        TradingView: any;
    }
}

export default StockChartModal;
