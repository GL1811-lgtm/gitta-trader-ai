const { UserSetting } = require('../models');

const getSettings = async (req, res) => {
  try {
    const settings = await UserSetting.findOne({ where: { userId: req.user.id } });
    if (!settings) {
      return res.status(404).json({ error: 'User settings not found.' });
    }
    res.json(settings);
  } catch (err) {
    console.error('Error fetching user settings:', err);
    res.status(500).json({ error: 'Failed to fetch user settings.' });
  }
};

const updateSettings = async (req, res) => {
  const updates = req.body;
  try {
    let settings = await UserSetting.findOne({ where: { userId: req.user.id } });
    if (!settings) {
      // If settings don't exist, create them
      settings = await UserSetting.create({ userId: req.user.id, ...updates });
    } else {
      Object.assign(settings, updates);
      await settings.save();
    }
    res.json(settings);
  } catch (err) {
    console.error('Error updating user settings:', err);
    res.status(500).json({ error: 'Failed to update user settings.' });
  }
};

module.exports = {
  getSettings,
  updateSettings,
};