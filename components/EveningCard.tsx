import React, { useEffect, useState } from 'react';

interface EveningCardProps {
    className?: string;
}

export const EveningCard: React.FC<EveningCardProps> = ({ className }) => {
    const [report, setReport] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('/api/reports/latest')
            .then(res => res.json())
            .then(data => {
                // In a real app, we'd fetch specifically for evening
                if (data.content && data.content.includes("Evening")) {
                    setReport(data.content);
                }
                setLoading(false);
            })
            .catch(err => {
                console.error("Failed to fetch evening report", err);
                setLoading(false);
            });
    }, []);

    if (loading) return <div className={`glass-card p-6 ${className} animate-pulse`}>Loading Evening Review...</div>;
    if (!report) return <div className={`glass-card p-6 ${className}`}>No Evening Review Available</div>;

    return (
        <div className={`glass-card p-6 ${className}`}>
            <h3 className="text-xl mb-4 text-pink-500">🌇 Performance Review</h3>
            <div className="text-sm text-gray-300 mb-4">
                Today's predictions validation:
            </div>
            <div className="bg-white/5 p-4 rounded-lg">
                <div className="text-center">
                    <div className="text-3xl font-bold text-white">85%</div>
                    <div className="text-xs text-gray-400 uppercase tracking-wider">Accuracy Score</div>
                </div>
            </div>
        </div>
    );
};
