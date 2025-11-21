const { StockDataPoint } = require('../models');
const { fetchIntraday } = require('../utils/financeProvider');

const getHistoricalStockData = async (req, res) => {
  const { symbol } = req.params;
  try {
    const historicalData = await fetchIntraday(symbol); // This fetches 1-min data
    res.json(historicalData);
  } catch (err) {
    console.error(`Error fetching historical data for ${symbol}:`, err);
    res.status(500).json({ error: 'Failed to fetch historical stock data.' });
  }
};

const getStockPrediction = async (req, res) => {
  const { symbol } = req.params;
  // This is a placeholder. In a real application, you would
  // call an internal AI model or a third-party prediction service.
  try {
    // Simulate a prediction
    const prediction = {
      symbol,
      signal: Math.random() > 0.5 ? 'BUY' : 'SELL',
      confidence: Math.random(),
      reason: `Based on simulated analysis of ${symbol} market trends and technical indicators.`,
    };
    res.json(prediction);
  } catch (err) {
    console.error(`Error generating prediction for ${symbol}:`, err);
    res.status(500).json({ error: 'Failed to generate stock prediction.' });
  }
};

module.exports = {
  getHistoricalStockData,
  getStockPrediction,
};