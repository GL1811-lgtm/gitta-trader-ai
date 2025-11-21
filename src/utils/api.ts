// API utility for making requests to the backend
// Uses VITE_API_URL environment variable for production (Render)
// Falls back to local development server if not set

// Get base URL from environment variable
const rawBase = import.meta.env.VITE_API_URL || '';
const BASE = rawBase.replace(/\/$/, ''); // remove trailing slash

/**
 * Build full API URL
 * Handles both development (same-origin) and production (cross-origin) scenarios
 */
export function apiUrl(path: string): string {
    // Ensure path starts with /
    const cleanPath = path.startsWith('/') ? path : `/${path}`;

    if (BASE) {
        // Production: Use environment variable (points to backend URL)
        // Check if BASE already contains /api
        if (BASE.endsWith('/api')) {
            return `${BASE}${cleanPath}`;
        } else {
            return `${BASE}/api${cleanPath}`;
        }
    }

    // Development: Use same-origin /api
    return `/api${cleanPath}`;
}

/**
 * Fetch wrapper with automatic error handling
 */
export async function apiFetch<T = any>(
    path: string,
    options?: RequestInit
): Promise<T> {
    const url = apiUrl(path);

    try {
        const response = await fetch(url, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options?.headers,
            },
        });

        if (!response.ok) {
            throw new Error(`API error ${response.status}: ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error(`API request failed for ${url}:`, error);
        throw error;
    }
}

/**
 * Convenience methods for common HTTP methods
 */
export const api = {
    get: <T = any>(path: string) => apiFetch<T>(path, { method: 'GET' }),

    post: <T = any>(path: string, data?: any) => apiFetch<T>(path, {
        method: 'POST',
        body: data ? JSON.stringify(data) : undefined,
    }),

    put: <T = any>(path: string, data?: any) => apiFetch<T>(path, {
        method: 'PUT',
        body: data ? JSON.stringify(data) : undefined,
    }),

    delete: <T = any>(path: string) => apiFetch<T>(path, { method: 'DELETE' }),
};

// Log the API base URL on initialization (for debugging)
console.log('🌐 API Base URL:', BASE || 'same-origin /api');
console.log('🔧 Environment:', import.meta.env.MODE);

export default api;
