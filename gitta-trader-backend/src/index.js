const express = require('express');
const http = require('http');
const cors = require('cors');
const dotenv = require('dotenv');
const { Server } = require('socket.io');

dotenv.config();

const { sequelize } = require('./models');

// Import Routes
const authRoutes = require('./routes/auth');
const dashboardRoutes = require('./routes/dashboard');
const alertsRoutes = require('./routes/alerts');
const analysisRoutes = require('./routes/analysis');
const geminiRoutes = require('./routes/gemini');
const learningRoutes = require('./routes/learning');
const settingsRoutes = require('./routes/settings');

// Import Socket Handlers
const { setupStocksSocket } = require('./sockets/stocksSocket');
const { setupAgentsSocket } = require('./sockets/agentsSocket');
const errorHandler = require('./middleware/errorHandler');
const logger = require('./middleware/logger');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: process.env.CORS_ORIGIN || '*', // Be specific in production
    methods: ['GET', 'POST', 'PUT', 'DELETE'],
  },
});

// Middleware
app.use(cors({
  origin: process.env.CORS_ORIGIN || '*',
}));
app.use(express.json()); // For parsing application/json
app.use(logger); // Use the logger middleware

// API Routes
app.use('/api/auth', authRoutes);
app.use('/api/dashboard', dashboardRoutes);
app.use('/api/alerts', alertsRoutes);
app.use('/api/analysis', analysisRoutes);
app.use('/api/gemini', geminiRoutes);
app.use('/api/learning', learningRoutes);
app.use('/api/settings', settingsRoutes);

// Error handling middleware (should be last)
app.use(errorHandler);

// Initialize Sockets
setupStocksSocket(io);
setupAgentsSocket(io);

const PORT = process.env.PORT || 4000;

(async () => {
  try {
    await sequelize.authenticate();
    console.log('Database connection has been established successfully.');
    await sequelize.sync({ alter: true }); // Use migrations in production
    console.log('Database synchronized.');

    server.listen(PORT, () => console.log(`Server running on port ${PORT}`));
  } catch (err) {
    console.error('Failed to start server:', err);
    process.exit(1); // Exit process with failure
  }
})();