const express = require('express');
const { getLearningLogs, chatWithMasterAgent } = require('../controllers/learningController');
const { requireAuth } = require('../middleware/auth');

const router = express.Router();

router.get('/logs', requireAuth, getLearningLogs);
router.post('/chat', requireAuth, chatWithMasterAgent);

module.exports = router;