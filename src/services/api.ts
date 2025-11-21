const API_BASE_URL = 'http://localhost:5000/api';

export const api = {
    async getEvolutionStatus() {
        const response = await fetch(`${API_BASE_URL}/evolution/status`);
        if (!response.ok) throw new Error('Failed to fetch evolution status');
        return response.json();
    },

    async evolve() {
        const response = await fetch(`${API_BASE_URL}/evolution/evolve`, {
            method: 'POST',
        });
        if (!response.ok) throw new Error('Failed to trigger evolution');
        return response.json();
    },

    async getSystemHealth() {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (!response.ok) {
            // Fallback if endpoint fails or doesn't exist yet
            return { status: 'unknown', uptime: 0 };
        }
        return response.json();
    },

    async getActiveAgents() {
        // Placeholder - ideally fetch from /api/agents/status
        try {
            const response = await fetch(`${API_BASE_URL}/agents/status`);
            if (response.ok) return response.json();
        } catch (e) {
            console.warn("Failed to fetch agents", e);
        }
        return [];
    },

    async getPerformanceData() {
        const response = await fetch(`${API_BASE_URL}/analytics/performance`);
        if (!response.ok) throw new Error('Failed to fetch performance data');
        return response.json();
    }
};
