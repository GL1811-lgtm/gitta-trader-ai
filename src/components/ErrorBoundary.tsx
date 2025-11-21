import React, { Component, ErrorInfo, ReactNode } from 'react';
import { Card } from '../../components/UI';

interface Props {
    children: ReactNode;
}

interface State {
    hasError: boolean;
    error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
    public state: State = {
        hasError: false,
        error: null
    };

    public static getDerivedStateFromError(error: Error): State {
        return { hasError: true, error };
    }

    public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
        console.error("Uncaught error:", error, errorInfo);
    }

    public render() {
        if (this.state.hasError) {
            return (
                <div className="p-6">
                    <Card className="border-red-500/50 bg-red-900/10">
                        <h2 className="text-xl font-bold text-red-400 mb-2">Something went wrong</h2>
                        <p className="text-slate-300 mb-4">
                            The application encountered an unexpected error.
                        </p>
                        <pre className="bg-black/30 p-4 rounded text-xs text-red-300 overflow-auto font-mono">
                            {this.state.error?.toString()}
                        </pre>
                        <button
                            className="mt-4 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded transition-colors"
                            onClick={() => window.location.reload()}
                        >
                            Reload Application
                        </button>
                    </Card>
                </div>
            );
        }

        return this.props.children;
    }
}
