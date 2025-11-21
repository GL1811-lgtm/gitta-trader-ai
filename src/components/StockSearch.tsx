import React, { useState, useEffect } from 'react';

interface StockSearchProps {
    onStockSelect?: (stock: any) => void;
}

interface StockResult {
    symbol: string;
    name: string;
    exchange: string;
    token?: string;
}

interface StockPrice {
    ltp: number;
    open: number;
    high: number;
    low: number;
    close: number;
    change: number;
    changePercent: number;
}

const StockSearch: React.FC<StockSearchProps> = ({ onStockSelect }) => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState<StockResult[]>([]);
    const [selectedStock, setSelectedStock] = useState<StockResult | null>(null);
    const [stockPrice, setStockPrice] = useState<StockPrice | null>(null);
    const [loading, setLoading] = useState(false);
    const [showDropdown, setShowDropdown] = useState(false);

    // Search stocks as user types
    useEffect(() => {
        if (query.length < 2) {
            setResults([]);
            setShowDropdown(false);
            return;
        }

        const searchStocks = async () => {
            try {
                const response = await fetch(`http://localhost:5000/api/stocks/search?q=${encodeURIComponent(query)}`);
                if (response.ok) {
                    const data = await response.json();
                    setResults(data.results || []);
                    setShowDropdown(true);
                }
            } catch (error) {
                console.error('Stock search error:', error);
                setResults([]);
            }
        };

        const debounce = setTimeout(searchStocks, 300);
        return () => clearTimeout(debounce);
    }, [query]);

    const fetchStockPrice = async (stock: StockResult) => {
        setLoading(true);
        try {
            const response = await fetch(`http://localhost:5000/api/stocks/price/${stock.symbol}`);
            if (response.ok) {
                const data = await response.json();
                setStockPrice(data);
            }
        } catch (error) {
            console.error('Price fetch error:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleStockSelect = (stock: StockResult) => {
        setSelectedStock(stock);
        setQuery(stock.symbol);
        setShowDropdown(false);
        fetchStockPrice(stock);
        onStockSelect?.(stock);
    };

    const handleClear = () => {
        setQuery('');
        setSelectedStock(null);
        setStockPrice(null);
        setResults([]);
    };

    return (
        <div className="w-full max-w-2xl mx-auto">
            {/* Search Input */}
            <div className="relative mb-4">
                <div className="relative">
                    <input
                        type="text"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        onFocus={() => query.length >= 2 && setShowDropdown(true)}
                        placeholder="Search stocks (e.g., RELIANCE, TCS, INFY)..."
                        className="w-full px-4 py-3 pl-12 bg-base-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-accent text-lg"
                    />
                    <svg
                        className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                    {query && (
                        <button
                            onClick={handleClear}
                            className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-200"
                        >
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    )}
                </div>

                {/* Search Results Dropdown */}
                {showDropdown && results.length > 0 && (
                    <div className="absolute z-10 w-full mt-2 bg-base-200 rounded-lg shadow-lg max-h-96 overflow-y-auto">
                        {results.map((stock, index) => (
                            <button
                                key={`${stock.symbol}-${index}`}
                                onClick={() => handleStockSelect(stock)}
                                className="w-full px-4 py-3 text-left hover:bg-base-300 transition-colors flex justify-between items-center border-b border-base-300 last:border-b-0"
                            >
                                <div>
                                    <div className="font-bold text-lg">{stock.symbol}</div>
                                    <div className="text-sm text-gray-400">{stock.name}</div>
                                </div>
                                <div className="text-xs text-gray-500">{stock.exchange}</div>
                            </button>
                        ))}
                    </div>
                )}
            </div>

            {/* Stock Price Display */}
            {selectedStock && (
                <div className="bg-base-200 rounded-lg p-6">
                    <div className="flex justify-between items-start mb-4">
                        <div>
                            <h2 className="text-3xl font-bold mb-1">{selectedStock.symbol}</h2>
                            <p className="text-gray-400">{selectedStock.name}</p>
                        </div>
                        <span className="px-3 py-1 bg-base-300 rounded text-sm">{selectedStock.exchange}</span>
                    </div>

                    {loading ? (
                        <div className="flex justify-center py-8">
                            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-accent"></div>
                        </div>
                    ) : stockPrice ? (
                        <div>
                            <div className="mb-6">
                                <div className="text-5xl font-bold mb-2">
                                    ₹{stockPrice.ltp.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                                </div>
                                <div className={`text-xl font-semibold ${stockPrice.change >= 0 ? 'text-accent' : 'text-danger'}`}>
                                    {stockPrice.change >= 0 ? '+' : ''}{stockPrice.change.toFixed(2)} ({stockPrice.changePercent.toFixed(2)}%)
                                </div>
                            </div>

                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                <div className="bg-base-300 p-4 rounded-lg">
                                    <div className="text-gray-400 text-sm mb-1">Open</div>
                                    <div className="text-xl font-bold">₹{stockPrice.open.toFixed(2)}</div>
                                </div>
                                <div className="bg-base-300 p-4 rounded-lg">
                                    <div className="text-gray-400 text-sm mb-1">High</div>
                                    <div className="text-xl font-bold text-accent">₹{stockPrice.high.toFixed(2)}</div>
                                </div>
                                <div className="bg-base-300 p-4 rounded-lg">
                                    <div className="text-gray-400 text-sm mb-1">Low</div>
                                    <div className="text-xl font-bold text-danger">₹{stockPrice.low.toFixed(2)}</div>
                                </div>
                                <div className="bg-base-300 p-4 rounded-lg">
                                    <div className="text-gray-400 text-sm mb-1">Prev Close</div>
                                    <div className="text-xl font-bold">₹{stockPrice.close.toFixed(2)}</div>
                                </div>
                            </div>

                            <div className="mt-4 flex gap-3">
                                <button className="flex-1 bg-accent text-white py-3 rounded-lg font-semibold hover:bg-accent/80 transition-colors">
                                    Add to Watchlist
                                </button>
                                <button className="flex-1 bg-info text-white py-3 rounded-lg font-semibold hover:bg-info/80 transition-colors">
                                    Trade
                                </button>
                            </div>
                        </div>
                    ) : (
                        <p className="text-center text-gray-400 py-4">Price data not available</p>
                    )}
                </div>
            )}
        </div>
    );
};

export default StockSearch;
