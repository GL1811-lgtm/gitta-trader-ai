import React, { useState, useEffect } from 'react';

interface StockDetailPageProps {
    symbol: string;
    name: string;
    onClose: () => void;
}

interface StockData {
    price: number;
    change: number;
    changePercent: number;
    open: number;
    high: number;
    low: number;
    prevClose: number;
}

const StockDetailPage: React.FC<StockDetailPageProps> = ({ symbol, name, onClose }) => {
    const [activeTab, setActiveTab] = useState<'buy' | 'sell'>('buy');
    const [orderType, setOrderType] = useState<'delivery' | 'intraday' | 'mtf'>('delivery');
    const [timePeriod, setTimePeriod] = useState('1D');
    const [quantity, setQuantity] = useState('');
    const [priceLimit, setPriceLimit] = useState('');
    const [stockData, setStockData] = useState<StockData | null>(null);

    useEffect(() => {
        // Fetch stock data
        fetchStockData();
    }, [symbol]);

    const fetchStockData = async () => {
        try {
            const response = await fetch(`/api/stocks/price/${symbol}`);
            if (response.ok) {
                const data = await response.json();
                setStockData({
                    price: data.ltp,
                    change: data.change,
                    changePercent: data.changePercent,
                    open: data.open,
                    high: data.high,
                    low: data.low,
                    prevClose: data.close
                });
                setPriceLimit(data.ltp.toFixed(2));
            }
        } catch (error) {
            console.error('Failed to fetch stock data:', error);
        }
    };

    const getCompanyInitials = () => {
        return symbol.slice(0, 2).toUpperCase();
    };

    const isPositive = stockData ? stockData.change >= 0 : true;

    return (
        <div className="fixed inset-0 z-50 bg-base-100 overflow-y-auto">
            {/* Header */}
            <div className="bg-base-200 border-b border-base-300 px-6 py-4 flex items-center justify-between sticky top-0 z-10">
                <div className="flex items-center gap-4">
                    {/* Back Button */}
                    <button
                        onClick={onClose}
                        className="p-2 hover:bg-base-300 rounded-full transition-colors"
                    >
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                        </svg>
                    </button>

                    {/* Company Info */}
                    <div className="flex items-center gap-3">
                        <div className="w-12 h-12 rounded bg-gradient-to-br from-info/30 to-accent/30 flex items-center justify-center">
                            <span className="font-bold text-lg">{getCompanyInitials()}</span>
                        </div>
                        <div>
                            <h1 className="text-xl font-bold">{name}</h1>
                            <div className="flex items-center gap-4 text-sm text-gray-400">
                                <span>NSE: ₹{stockData?.price.toFixed(2) || '0.00'}</span>
                                <span>BSE: ₹{stockData?.price.toFixed(2) || '0.00'}</span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Action Buttons */}
                <div className="flex items-center gap-3">
                    <button className="px-4 py-2 border border-base-300 rounded hover:bg-base-300 transition-colors flex items-center gap-2">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                        </svg>
                        Create Alert
                    </button>
                    <button className="px-4 py-2 border border-base-300 rounded hover:bg-base-300 transition-colors flex items-center gap-2">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                        </svg>
                        Watchlist
                    </button>
                </div>
            </div>

            {/* Main Content */}
            <div className="flex">
                {/* Left Side - Chart */}
                <div className="flex-1 p-6">
                    {/* Price and Change */}
                    <div className="mb-6">
                        <div className="text-4xl font-bold mb-2">
                            ₹{stockData?.price.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) || '0.00'}
                        </div>
                        <div className="flex items-center gap-3">
                            <span className={`text-lg font-semibold ${isPositive ? 'text-accent' : 'text-danger'}`}>
                                {isPositive ? '+' : ''}{stockData?.change.toFixed(2) || '0.00'} ({stockData?.changePercent.toFixed(2) || '0.00'}%)
                            </span>
                            <span className="text-sm text-gray-400">1D</span>
                        </div>
                    </div>

                    {/* Chart Area */}
                    <div className="bg-base-200 rounded-lg p-4 mb-4" style={{ height: '400px' }}>
                        <div className="w-full h-full flex items-center justify-center text-gray-400">
                            {/* TradingView Lightweight Chart will go here */}
                            <div className="text-center">
                                <svg className="w-16 h-16 mx-auto mb-2 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
                                </svg>
                                <p>Chart: {symbol}</p>
                                <p className="text-xs">{timePeriod} view</p>
                            </div>
                        </div>
                    </div>

                    {/* Time Period Selector */}
                    <div className="flex items-center gap-2 mb-6">
                        <span className="text-sm font-semibold mr-2">NSE</span>
                        {['1D', '1W', '1M', '3M', '6M', '1Y', '3Y', '5Y', 'All'].map((period) => (
                            <button
                                key={period}
                                onClick={() => setTimePeriod(period)}
                                className={`px-3 py-1 rounded transition-colors ${timePeriod === period
                                    ? 'bg-accent text-white'
                                    : 'bg-base-200 hover:bg-base-300'
                                    }`}
                            >
                                {period}
                            </button>
                        ))}
                        <button className="px-3 py-1 bg-base-200 hover:bg-base-300 rounded transition-colors flex items-center gap-1">
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                            </svg>
                            Terminal
                        </button>
                    </div>

                    {/* Option Chain Link */}
                    <a href="#" className="text-info hover:underline text-sm flex items-center gap-1">
                        <span>⚡</span> Option Chain
                    </a>
                </div>

                {/* Right Side - Buy/Sell Panel */}
                <div className="w-96 bg-base-200 border-l border-base-300 p-6">
                    {/* Buy/Sell Tabs */}
                    <div className="flex mb-6">
                        <button
                            onClick={() => setActiveTab('buy')}
                            className={`flex-1 py-3 font-bold transition-colors ${activeTab === 'buy'
                                ? 'text-accent border-b-2 border-accent'
                                : 'text-gray-400 border-b border-base-300'
                                }`}
                        >
                            BUY
                        </button>
                        <button
                            onClick={() => setActiveTab('sell')}
                            className={`flex-1 py-3 font-bold transition-colors ${activeTab === 'sell'
                                ? 'text-danger border-b-2 border-danger'
                                : 'text-gray-400 border-b border-base-300'
                                }`}
                        >
                            SELL
                        </button>
                    </div>

                    {/* Order Type Selector */}
                    <div className="flex gap-2 mb-6">
                        {['delivery', 'intraday', 'mtf'].map((type) => (
                            <button
                                key={type}
                                onClick={() => setOrderType(type as any)}
                                className={`px-4 py-2 rounded capitalize transition-colors ${orderType === type
                                    ? 'bg-accent/20 text-accent border border-accent'
                                    : 'bg-base-300 hover:bg-base-100'
                                    }`}
                            >
                                {type}
                            </button>
                        ))}
                        <button className="px-3 py-2 bg-base-300 rounded hover:bg-base-100">
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                            </svg>
                        </button>
                    </div>

                    {/* Quantity Input */}
                    <div className="mb-4">
                        <label className="text-sm text-gray-400 mb-2 block">Qty NSE</label>
                        <input
                            type="number"
                            value={quantity}
                            onChange={(e) => setQuantity(e.target.value)}
                            placeholder="0"
                            className="w-full px-4 py-3 bg-base-300 rounded focus:outline-none focus:ring-2 focus:ring-accent"
                        />
                    </div>

                    {/* Price Limit */}
                    <div className="mb-6">
                        <label className="text-sm text-gray-400 mb-2 block">Price Limit</label>
                        <input
                            type="number"
                            value={priceLimit}
                            onChange={(e) => setPriceLimit(e.target.value)}
                            className="w-full px-4 py-3 bg-base-300 rounded focus:outline-none focus:ring-2 focus:ring-accent"
                            step="0.05"
                        />
                    </div>

                    {/* Balance and Margin */}
                    <div className="flex justify-between text-sm mb-6">
                        <span className="text-gray-400">Balance: <span className="text-white">₹0</span></span>
                        <span className="text-gray-400">Approx req: <span className="text-white">₹0</span></span>
                    </div>

                    {/* Buy/Sell Button */}
                    <button
                        className={`w-full py-4 rounded-lg font-bold text-white text-lg transition-colors ${activeTab === 'buy'
                            ? 'bg-accent hover:bg-accent/80'
                            : 'bg-danger hover:bg-danger/80'
                            }`}
                    >
                        {activeTab === 'buy' ? 'Buy' : 'Sell'}
                    </button>

                    {/* Additional Info */}
                    <div className="mt-6 pt-6 border-t border-base-300 text-sm space-y-2">
                        <div className="flex justify-between">
                            <span className="text-gray-400">Open</span>
                            <span>₹{stockData?.open.toFixed(2) || '0.00'}</span>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-gray-400">High</span>
                            <span className="text-accent">₹{stockData?.high.toFixed(2) || '0.00'}</span>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-gray-400">Low</span>
                            <span className="text-danger">₹{stockData?.low.toFixed(2) || '0.00'}</span>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-gray-400">Prev. Close</span>
                            <span>₹{stockData?.prevClose.toFixed(2) || '0.00'}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default StockDetailPage;
