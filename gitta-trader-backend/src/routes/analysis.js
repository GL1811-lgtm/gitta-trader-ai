const express = require('express');
const { getHistoricalStockData, getStockPrediction } = require('../controllers/analysisController');
const { requireAuth } = require('../middleware/auth');

const router = express.Router();

router.get('/stock/historical/:symbol', requireAuth, getHistoricalStockData);
router.get('/stock/prediction/:symbol', requireAuth, getStockPrediction);

module.exports = router;