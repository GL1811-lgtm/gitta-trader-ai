const { fetchLatestTick, fetchIntraday } = require('../utils/financeProvider');
const { simpleMA, rsi, macd } = require('../utils/indicators');
const { StockDataPoint } = require('../models'); // Assuming you might want to save or retrieve

function setupStocksSocket(io) {
  const nsp = io.of('/stocks/live');

  nsp.on('connection', (socket) => {
    const { symbol } = socket.handshake.query;
    if (!symbol) {
      socket.emit('error', { message: 'symbol query param required' });
      socket.disconnect();
      return;
    }

    console.log(`Client connected to /stocks/live for symbol: ${symbol}`);

    let interval;

    const sendTick = async () => {
      try {
        const latest = await fetchLatestTick(symbol);
        if (!latest) {
          console.log(`No latest tick for ${symbol}, skipping.`);
          return;
        }

        // Fetch intraday data to calculate indicators
        const hist = await fetchIntraday(symbol);
        if (hist.length === 0) {
          console.log(`No historical data for ${symbol}, cannot calculate indicators.`);
          // Still send the latest tick if no historical data for indicators
          const payload = {
            time: latest.timestamp.toISOString(),
            open: latest.open,
            high: latest.high,
            low: latest.low,
            close: latest.close,
            volume: latest.volume,
          };
          socket.emit('tick', payload);
          return;
        }

        const ma = simpleMA(hist, 20);
        const r = rsi(hist, 14);
        const m = macd(hist);

        const payload = {
          time: latest.timestamp.toISOString(),
          open: latest.open,
          high: latest.high,
          low: latest.low,
          close: latest.close,
          volume: latest.volume,
          ma: ma !== null ? parseFloat(ma.toFixed(2)) : null,
          rsi: r !== null ? parseFloat(r.toFixed(2)) : null,
          macd: m ? {
            macdLine: parseFloat(m.macdLine.toFixed(2)),
            signalLine: parseFloat(m.signalLine.toFixed(2)),
            histogram: parseFloat(m.histogram.toFixed(2)),
          } : null,
        };
        socket.emit('tick', payload);
      } catch (err) {
        console.error(`Stocks socket error for ${symbol}:`, err);
        socket.emit('error', { message: `Failed to fetch tick for ${symbol}` });
      }
    };

    // Send initial tick immediately
    sendTick();

    interval = setInterval(sendTick, parseInt(process.env.STOCK_TICK_INTERVAL_MS || '2500', 10));

    socket.on('disconnect', () => {
      console.log(`Client disconnected from /stocks/live for symbol: ${symbol}`);
      clearInterval(interval);
    });
  });
}

module.exports = {
  setupStocksSocket
};