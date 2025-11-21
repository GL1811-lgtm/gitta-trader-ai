import React, { useState, useEffect, FC } from 'react';
import { simpleMarkdownToHtml } from '../utils';
import { Card, SectionTitle, Button } from '../components/UI';

const Reports: FC = () => {
    const [report, setReport] = useState<string>('');
    const [filename, setFilename] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);
    const [workflowLoading, setWorkflowLoading] = useState<boolean>(false);
    const [message, setMessage] = useState<string>('');

    const fetchReport = async () => {
        setLoading(true);
        try {
            const res = await fetch('/api/reports/latest');
            if (res.ok) {
                const data = await res.json();
                setReport(data.content);
                setFilename(data.filename);
            } else {
                setReport('No report found or error fetching report.');
            }
        } catch (e) {
            setReport('Error connecting to API.');
        } finally {
            setLoading(false);
        }
    };

    const runWorkflow = async () => {
        setWorkflowLoading(true);
        setMessage('');
        try {
            const res = await fetch('/api/workflow/run', { method: 'POST' });
            const data = await res.json();
            if (res.ok) {
                setMessage(`Success: ${data.message}`);
            } else {
                setMessage(`Error: ${data.error}`);
            }
        } catch (e) {
            setMessage('Error triggering workflow.');
        } finally {
            setWorkflowLoading(false);
        }
    };

    useEffect(() => {
        fetchReport();
    }, []);

    return (
        <div className="animate-fade-in space-y-6">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                    <SectionTitle className="mb-1">Daily Strategy Reports</SectionTitle>
                    <p className="text-slate-400 text-sm">Latest report: {filename || 'None'}</p>
                </div>
                <Button
                    onClick={runWorkflow}
                    isLoading={workflowLoading}
                >
                    Run New Analysis
                </Button>
            </div>

            {message && (
                <div className={`p-4 rounded-lg ${message.startsWith('Success') ? 'bg-green-900/50 text-green-200 border border-green-800' : 'bg-red-900/50 text-red-200 border border-red-800'}`}>
                    {message}
                </div>
            )}

            <Card>
                {loading ? (
                    <div className="flex items-center justify-center h-64">
                        <p className="text-slate-400">Loading report...</p>
                    </div>
                ) : (
                    <div
                        className="prose prose-invert max-w-none"
                        dangerouslySetInnerHTML={{ __html: simpleMarkdownToHtml(report) }}
                    />
                )}
            </Card>
        </div>
    );
};

export default Reports;
