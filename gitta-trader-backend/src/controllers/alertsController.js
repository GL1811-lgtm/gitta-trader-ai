const { Alert } = require('../models');

const getAllAlerts = async (req, res) => {
  try {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 10;
    const offset = (page - 1) * limit;

    const { count, rows } = await Alert.findAndCountAll({
      limit,
      offset,
      order: [['timestamp', 'DESC']],
    });

    res.json({
      totalItems: count,
      totalPages: Math.ceil(count / limit),
      currentPage: page,
      alerts: rows,
    });
  } catch (err) {
    console.error('Error fetching alerts:', err);
    res.status(500).json({ error: 'Failed to fetch alerts.' });
  }
};

module.exports = {
  getAllAlerts,
};