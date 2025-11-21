const express = require('express');
const { getAllAlerts } = require('../controllers/alertsController');
const { requireAuth } = require('../middleware/auth');

const router = express.Router();

router.get('/', requireAuth, getAllAlerts);

module.exports = router;