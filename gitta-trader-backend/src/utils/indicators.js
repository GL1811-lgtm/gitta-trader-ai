// Simple Moving Average (SMA)
const simpleMA = (data, period) => {
  if (data.length < period) return null;
  const sum = data.slice(-period).reduce((acc, val) => acc + val.close, 0);
  return sum / period;
};

// Relative Strength Index (RSI)
const rsi = (data, period) => {
  if (data.length < period) return null;

  let gains = 0;
  let losses = 0;

  for (let i = data.length - period; i < data.length; i++) {
    const change = data[i].close - data[i - 1].close;
    if (change > 0) {
      gains += change;
    } else {
      losses -= change; // make it positive
    }
  }

  const avgGain = gains / period;
  const avgLoss = losses / period;

  if (avgLoss === 0) return 100; // Avoid division by zero
  const rs = avgGain / avgLoss;
  return 100 - (100 / (1 + rs));
};

// Moving Average Convergence Divergence (MACD)
const exponentialMA = (data, period, property = 'close') => {
  if (data.length === 0) return [];
  const k = 2 / (period + 1);
  let emaArray = [data[0][property]]; // First EMA is just the first data point

  for (let i = 1; i < data.length; i++) {
    const ema = (data[i][property] * k) + (emaArray[i - 1] * (1 - k));
    emaArray.push(ema);
  }
  return emaArray;
};

const macd = (data, fastPeriod = 12, slowPeriod = 26, signalPeriod = 9) => {
  if (data.length < slowPeriod) return null;

  const closes = data.map(d => d.close);

  const ema12 = exponentialMA(data, fastPeriod);
  const ema26 = exponentialMA(data, slowPeriod);

  // MACD Line: 12-period EMA - 26-period EMA
  const macdLine = ema12.slice(ema12.length - ema26.length).map((val, i) => val - ema26[i]);

  // Signal Line: 9-period EMA of MACD Line
  const signalLine = exponentialMA(macdLine.map(val => ({ close: val })), signalPeriod).map(d => d.close); // Wrap in object for EMA function

  // Histogram: MACD Line - Signal Line
  const histogram = macdLine.slice(macdLine.length - signalLine.length).map((val, i) => val - signalLine[i]);

  return {
    macdLine: macdLine[macdLine.length - 1],
    signalLine: signalLine[signalLine.length - 1],
    histogram: histogram[histogram.length - 1],
  };
};


module.exports = {
  simpleMA,
  rsi,
  macd,
};