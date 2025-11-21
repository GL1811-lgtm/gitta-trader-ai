import React, { useState, useEffect, useRef } from 'react';

interface Stock {
    symbol: string;
    name: string;
    price: number;
    change: number;
    changePercent: number;
}

interface MostTradedStocksProps {
    onStockClick?: (symbol: string, name: string) => void;
}

const MostTradedStocks: React.FC<MostTradedStocksProps> = ({ onStockClick }) => {
    const [stocks, setStocks] = useState<Stock[]>([]);
    const [canScrollLeft, setCanScrollLeft] = useState(false);
    const [canScrollRight, setCanScrollRight] = useState(false);
    const scrollContainerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        fetchMostTraded();
        const interval = setInterval(fetchMostTraded, 30000);
        return () => clearInterval(interval);
    }, []);

    useEffect(() => {
        // Check scroll possibility when stocks change
        checkScroll();
    }, [stocks]);

    const fetchMostTraded = async () => {
        try {
            const response = await fetch('http://localhost:5000/api/dashboard/most-traded');
            if (response.ok) {
                const data = await response.json();
                setStocks(data.stocks || []);
            }
        } catch (error) {
            console.error('Failed to fetch most traded:', error);
        }
    };

    const checkScroll = () => {
        if (scrollContainerRef.current) {
            const { scrollLeft, scrollWidth, clientWidth } = scrollContainerRef.current;
            setCanScrollLeft(scrollLeft > 10);
            setCanScrollRight(scrollLeft < scrollWidth - clientWidth - 10);
        }
    };

    const scroll = (direction: 'left' | 'right') => {
        if (scrollContainerRef.current) {
            const scrollAmount = 300;
            const currentScroll = scrollContainerRef.current.scrollLeft;
            const newScroll = direction === 'left'
                ? currentScroll - scrollAmount
                : currentScroll + scrollAmount;

            scrollContainerRef.current.scrollTo({
                left: newScroll,
                behavior: 'smooth'
            });

            // Update arrows after scroll
            setTimeout(checkScroll, 300);
        }
    };

    const getCompanyInitials = (name: string) => {
        return name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();
    };

    return (
        <div className="bg-base-200 rounded-lg p-6">
            <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-bold">Most traded stocks on Groww</h3>
                <button className="text-accent hover:underline text-sm font-semibold">See more →</button>
            </div>

            {/* Carousel Container with Arrows */}
            <div className="relative px-10">
                {/* Left Arrow */}
                {canScrollLeft && (
                    <button
                        onClick={() => scroll('left')}
                        className="absolute left-0 top-1/2 -translate-y-1/2 z-20 bg-accent text-white hover:bg-accent/80 p-2 rounded-full shadow-2xl transition-all"
                        aria-label="Scroll left"
                    >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M15 19l-7-7 7-7" />
                        </svg>
                    </button>
                )}

                {/* Stocks Horizontal Scroll */}
                <div
                    ref={scrollContainerRef}
                    onScroll={checkScroll}
                    className="flex gap-4 overflow-x-auto pb-2"
                    style={{
                        scrollbarWidth: 'none',
                        msOverflowStyle: 'none'
                    }}
                >
                    {stocks.map((stock) => {
                        const isPositive = stock.changePercent >= 0;
                        return (
                            <button
                                key={stock.symbol}
                                onClick={() => onStockClick?.(stock.symbol, stock.name)}
                                className="bg-base-300 p-4 rounded-lg hover:bg-base-100 transition-colors text-left flex-shrink-0 w-56"
                            >
                                {/* Company Logo */}
                                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-accent/30 to-info/30 flex items-center justify-center mb-3">
                                    <span className="font-bold text-sm">{getCompanyInitials(stock.name)}</span>
                                </div>

                                {/* Company Name */}
                                <h4 className="font-semibold text-sm mb-2 truncate">{stock.name}</h4>

                                {/* Price */}
                                <div className="text-lg font-bold mb-1">₹{stock.price.toFixed(2)}</div>

                                {/* Change */}
                                <div className={`text-sm font-semibold ${isPositive ? 'text-accent' : 'text-danger'}`}>
                                    {isPositive ? '+' : ''}{stock.change.toFixed(2)} ({stock.changePercent.toFixed(2)}%)
                                </div>
                            </button>
                        );
                    })}
                </div>

                {/* Right Arrow */}
                {canScrollRight && (
                    <button
                        onClick={() => scroll('right')}
                        className="absolute right-0 top-1/2 -translate-y-1/2 z-20 bg-accent text-white hover:bg-accent/80 p-2 rounded-full shadow-2xl transition-all"
                        aria-label="Scroll right"
                    >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M9 5l7 7-7 7" />
                        </svg>
                    </button>
                )}
            </div>

            {/* Hide scrollbar CSS */}
            <style>{`
        div::-webkit-scrollbar {
          display: none;
        }
      `}</style>
        </div>
    );
};

export default MostTradedStocks;
