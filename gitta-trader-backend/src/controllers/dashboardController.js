const { Alert, StockDataPoint } = require('../models');
const { fetchLatestTick } = require('../utils/financeProvider');

const getDashboardData = async (req, res) => {
  try {
    // Fetch recent alerts (e.g., last 3)
    const todaysRecommendations = await Alert.findAll({
      limit: 3,
      order: [['timestamp', 'DESC']],
    });

    // Fetch more recent alerts for the list
    const recentAlerts = await Alert.findAll({
      limit: 5, // Adjust as needed
      order: [['timestamp', 'DESC']],
      attributes: ['instrument', 'timestamp', 'type'], // Only fetch necessary fields
    });

    // Simulate market indices (replace with real data integration)
    const marketIndices = [
      { name: 'NIFTY 50', value: 23450.75, change: 0.5, changeType: 'up' },
      { name: 'BANK NIFTY', value: 50123.40, change: -0.2, changeType: 'down' },
      // Add more indices as needed
    ];

    // Simulate overall confidence (could be derived from AI models)
    const overallConfidence = 94.7;

    res.json({
      overallConfidence,
      marketIndices,
      todaysRecommendations,
      recentAlerts,
    });
  } catch (err) {
    console.error('Error fetching dashboard data:', err);
    res.status(500).json({ error: 'Failed to fetch dashboard data.' });
  }
};

module.exports = {
  getDashboardData,
};