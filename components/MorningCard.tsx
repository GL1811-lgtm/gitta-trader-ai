import React, { useEffect, useState } from 'react';

interface MorningCardProps {
    className?: string;
}

export const MorningCard: React.FC<MorningCardProps> = ({ className }) => {
    const [report, setReport] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('/api/reports/latest')
            .then(res => res.json())
            .then(data => {
                if (data.content && data.content.includes("Morning")) {
                    setReport(data.content);
                }
                setLoading(false);
            })
            .catch(err => {
                console.error("Failed to fetch morning report", err);
                setLoading(false);
            });
    }, []);

    if (loading) return <div className={`glass-card p-6 ${className} animate-pulse`}>Loading Morning Scan...</div>;
    if (!report) return <div className={`glass-card p-6 ${className}`}>No Morning Report Available</div>;

    // Simple parsing to extract top picks (mock)
    const lines = report.split('\n').filter(l => l.includes('|') && l.includes('**'));
    const topPicks = lines.slice(0, 3).map(line => {
        const parts = line.split('|');
        return {
            symbol: parts[1]?.replace(/\*\*/g, '').trim(),
            price: parts[2]?.trim(),
            reason: parts[3]?.trim()
        };
    });

    return (
        <div className={`glass-card p-6 ${className}`}>
            <h3 className="text-xl mb-4 text-neon">🌅 Morning Opportunities</h3>
            <div className="space-y-3">
                {topPicks.map((pick, idx) => (
                    <div key={idx} className="flex justify-between items-center border-b border-white/10 pb-2">
                        <div>
                            <div className="font-bold text-lg">{pick.symbol}</div>
                            <div className="text-xs text-gray-400">{pick.reason}</div>
                        </div>
                        <div className="text-green-400 font-mono">₹{pick.price}</div>
                    </div>
                ))}
            </div>
        </div>
    );
};
