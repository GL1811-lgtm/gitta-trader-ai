import React, { useState, useEffect } from 'react';

interface NewsItem {
    symbol: string;
    company: string;
    headline: string;
    time: string;
    changePercent: number;
    logo?: string;
}

interface StocksInNewsProps {
    onViewAll?: () => void;
}

const StocksInNews: React.FC<StocksInNewsProps> = ({ onViewAll }) => {
    const [news, setNews] = useState<NewsItem[]>([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        fetchNews();
        const interval = setInterval(fetchNews, 60000); // Update every minute
        return () => clearInterval(interval);
    }, []);

    const fetchNews = async () => {
        setLoading(true);
        try {
            const response = await fetch('http://localhost:5000/api/dashboard/news');
            if (response.ok) {
                const data = await response.json();
                setNews(data.news || []);
            }
        } catch (error) {
            console.error('Failed to fetch news:', error);
        } finally {
            setLoading(false);
        }
    };

    const getCompanyInitials = (company: string) => {
        return company.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();
    };

    return (
        <div className="bg-base-200 rounded-lg p-6">
            <h3 className="text-xl font-bold mb-4">Stocks in news today</h3>

            {loading ? (
                <div className="flex justify-center py-8">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-accent"></div>
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {news.map((item, index) => (
                        <div
                            key={`${item.symbol}-${index}`}
                            className="bg-base-300 p-4 rounded-lg hover:bg-base-100 transition-colors cursor-pointer"
                        >
                            <div className="flex items-start gap-3 mb-3">
                                {/* Company Logo */}
                                <div className="w-12 h-12 rounded bg-gradient-to-br from-accent/30 to-info/30 flex items-center justify-center flex-shrink-0">
                                    <span className="font-bold text-sm">{getCompanyInitials(item.company)}</span>
                                </div>

                                <div className="flex-1 min-w-0">
                                    <div className="flex items-center justify-between mb-1">
                                        <h4 className="font-bold text-sm">{item.company}</h4>
                                        <span className={`text-sm font-semibold ${item.changePercent >= 0 ? 'text-accent' : 'text-danger'
                                            }`}>
                                            {item.changePercent >= 0 ? '+' : ''}{item.changePercent.toFixed(2)}%
                                        </span>
                                    </div>
                                </div>
                            </div>

                            <p className="text-sm text-gray-300 line-clamp-2 mb-2">
                                {item.headline}
                            </p>

                            <span className="text-xs text-gray-500">{item.time}</span>
                        </div>
                    ))}
                </div>
            )}

            {news.length > 0 && (
                <button
                    onClick={onViewAll}
                    className="w-full mt-4 py-2 text-accent hover:bg-base-300 rounded transition-colors font-semibold"
                >
                    View all news →
                </button>
            )}
        </div>
    );
};

export default StocksInNews;
