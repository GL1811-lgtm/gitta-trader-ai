const express = require('express');
const { getGeminiAnalysis } = require('../controllers/geminiController');
const { requireAuth } = require('../middleware/auth');

const router = express.Router();

router.post('/analysis', requireAuth, getGeminiAnalysis);

module.exports = router;
