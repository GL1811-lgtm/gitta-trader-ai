const axios = require('axios');
const dotenv = require('dotenv');
dotenv.config();

const FINANCE_API_KEY = process.env.FINANCE_API_KEY;
const FINANCE_PROVIDER = process.env.FINANCE_PROVIDER || 'ALPHAVANTAGE';

// Helper to convert Alpha Vantage 1-min data to a consistent format
const formatAlphaVantageData = (data) => {
  const timeSeries = data['Time Series (1min)'];
  if (!timeSeries) return [];

  return Object.keys(timeSeries).map(timestamp => ({
    timestamp: new Date(timestamp),
    open: parseFloat(timeSeries[timestamp]['1. open']),
    high: parseFloat(timeSeries[timestamp]['2. high']),
    low: parseFloat(timeSeries[timestamp]['3. low']),
    close: parseFloat(timeSeries[timestamp]['4. close']),
    volume: parseInt(timeSeries[timestamp]['5. volume']),
  })).sort((a, b) => a.timestamp - b.timestamp); // Sort by time ascending
};

const fetchIntraday = async (symbol) => {
  if (FINANCE_PROVIDER === 'ALPHAVANTAGE') {
    const url = `https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=${symbol}&interval=1min&outputsize=full&apikey=${FINANCE_API_KEY}`;
    try {
      const response = await axios.get(url);
      return formatAlphaVantageData(response.data);
    } catch (error) {
      console.error('Error fetching intraday data from Alpha Vantage:', error.message);
      return [];
    }
  }
  // Add other providers here
  return [];
};

const fetchLatestTick = async (symbol) => {
  if (FINANCE_PROVIDER === 'ALPHAVANTAGE') {
    const url = `https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=${symbol}&apikey=${FINANCE_API_KEY}`;
    try {
      const response = await axios.get(url);
      const data = response.data['Global Quote'];
      if (data && Object.keys(data).length > 0) {
        return {
          timestamp: new Date(data['07. latest trading day'] + ' ' + new Date().toTimeString().split(' ')[0]), // Alpha Vantage doesn't provide time for global quote, so append current time
          open: parseFloat(data['02. open']),
          high: parseFloat(data['03. high']),
          low: parseFloat(data['04. low']),
          close: parseFloat(data['05. price']), // 'price' is the latest close
          volume: parseInt(data['06. volume']),
        };
      }
      return null;
    } catch (error) {
      console.error('Error fetching latest tick from Alpha Vantage:', error.message);
      return null;
    }
  }
  // Add other providers here
  return null;
};

module.exports = {
  fetchIntraday,
  fetchLatestTick,
};