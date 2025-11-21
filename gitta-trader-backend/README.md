# Gitta Trader AI - Backend

This is the backend system for the Gitta Trader AI frontend, providing user authentication, data serving, real-time WebSocket communication, and secure proxying to the Google Gemini AI API.

## Quick Start

1.  **Copy files:** Ensure all backend files are copied into the `gitta-trader-backend` directory.
2.  **Environment Variables:** Create a `.env` file in the `gitta-trader-backend` directory by copying `.env.example` and filling in the required values:
    *   `DATABASE_URL`: Your PostgreSQL connection string (e.g., `postgres://user:password@host:port/database_name`).
    *   `JWT_SECRET`: A strong, secret key for JWT token signing.
    *   `FINANCE_API_KEY`: Your API key for the chosen financial data provider (e.g., Alpha Vantage).
    *   `GEMINI_API_KEY`: Your Google Gemini API key.
    *   `GEMINI_API_URL`: The endpoint URL for the Google Gemini API.
    *   `CORS_ORIGIN`: Restrict this to your frontend domain in production (e.g., `http://localhost:3000`).
3.  **Install Dependencies:**
    ```bash
    npm install
    ```
4.  **Run the Server:**
    ```bash
    npm run dev
    ```
    (or `npm start` for production)

## Notes & Production Tips

*   **Gemini API Key:** Never expose `GEMINI_API_KEY` to the frontend. All Gemini calls must be proxied via `/api/gemini` endpoints.
*   **Financial Data Provider:** Alpha Vantage has strict rate limits. For production, consider a paid provider or a dedicated WebSocket feed for real-time data.
*   **Security:** Implement HTTPS, use a strong `JWT_SECRET`, rotate keys regularly, and restrict CORS origins to your frontend domain.
*   **Database Migrations:** Replace `sequelize.sync({ alter: true })` with a proper database migration system (e.g., `sequelize-cli`) for production environments.
*   **Rate-limits & Caching:** `fetchIntraday` calls the financial API on each request. Implement caching (e.g., with Redis) for production to reduce API calls and improve performance.
*   **Scaling:** For many concurrent WebSocket clients, consider moving background tick ingestion into a separate worker process rather than on-demand per socket connection.
*   **Testing:** Create a test user via `/api/auth/register`, then use the returned JWT token in the `Authorization: Bearer <token>` header for authenticated requests.