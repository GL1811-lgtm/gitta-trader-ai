import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { HolographicCard } from '../ui/HolographicCard';

const data = [
    { time: '09:15', value: 25000 },
    { time: '10:00', value: 25200 },
    { time: '11:00', value: 24800 },
    { time: '12:00', value: 25500 },
    { time: '13:00', value: 26000 },
    { time: '14:00', value: 25800 },
    { time: '15:00', value: 26500 },
    { time: '15:30', value: 27000 },
];

export const PerformanceChart: React.FC = () => {
    const [chartData, setChartData] = React.useState<any[]>([]);
    const [loading, setLoading] = React.useState(true);

    React.useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch('http://localhost:5000/api/analytics/performance');
                if (response.ok) {
                    const data = await response.json();
                    // Transform data if necessary, or use directly if API returns compatible format
                    // Assuming API returns array of { time: 'HH:MM', value: number }
                    // If API returns empty or different format, fallback to mock for demo
                    if (Array.isArray(data) && data.length > 0) {
                        setChartData(data);
                    } else {
                        // Fallback mock data for demonstration if API returns empty
                        setChartData([
                            { time: '09:15', value: 25000 },
                            { time: '10:00', value: 25200 },
                            { time: '11:00', value: 24800 },
                            { time: '12:00', value: 25500 },
                            { time: '13:00', value: 26000 },
                            { time: '14:00', value: 25800 },
                            { time: '15:00', value: 26500 },
                            { time: '15:30', value: 27000 },
                        ]);
                    }
                }
            } catch (error) {
                console.error("Failed to fetch performance data:", error);
                // Fallback on error
                setChartData([
                    { time: '09:15', value: 25000 },
                    { time: '10:00', value: 25200 },
                    { time: '11:00', value: 24800 },
                    { time: '12:00', value: 25500 },
                    { time: '13:00', value: 26000 },
                    { time: '14:00', value: 25800 },
                    { time: '15:00', value: 26500 },
                    { time: '15:30', value: 27000 },
                ]);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
        const interval = setInterval(fetchData, 60000); // Refresh every minute
        return () => clearInterval(interval);
    }, []);

    if (loading) {
        return (
            <HolographicCard title="Live Performance" className="h-full min-h-[300px]">
                <div className="h-[250px] w-full flex items-center justify-center text-cyan-500">
                    Loading...
                </div>
            </HolographicCard>
        );
    }

    return (
        <HolographicCard title="Live Performance" className="h-full min-h-[300px]">
            <div className="h-[250px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={chartData}>
                        <defs>
                            <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="var(--neon-cyan)" stopOpacity={0.3} />
                                <stop offset="95%" stopColor="var(--neon-cyan)" stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                        <XAxis dataKey="time" stroke="#666" tick={{ fill: '#666' }} />
                        <YAxis stroke="#666" tick={{ fill: '#666' }} />
                        <Tooltip
                            contentStyle={{ backgroundColor: 'rgba(0,0,0,0.8)', border: '1px solid var(--neon-cyan)', borderRadius: '8px' }}
                            itemStyle={{ color: 'var(--neon-cyan)' }}
                        />
                        <Area
                            type="monotone"
                            dataKey="value"
                            stroke="var(--neon-cyan)"
                            fillOpacity={1}
                            fill="url(#colorValue)"
                        />
                    </AreaChart>
                </ResponsiveContainer>
            </div>
        </HolographicCard>
    );
};
