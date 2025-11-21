const sequelize = require('../config/sequelize');
const { DataTypes } = require('sequelize');

const User = require('./User')(sequelize, DataTypes);
const UserSetting = require('./UserSetting')(sequelize, DataTypes);
const Alert = require('./Alert')(sequelize, DataTypes);
const LearningLogEntry = require('./LearningLogEntry')(sequelize, DataTypes);
const StockDataPoint = require('./StockDataPoint')(sequelize, DataTypes);
const ChatHistory = require('./ChatHistory')(sequelize, DataTypes);

// Define associations
User.hasOne(UserSetting, { foreignKey: 'userId', onDelete: 'CASCADE' });
UserSetting.belongsTo(User, { foreignKey: 'userId' });

User.hasMany(ChatHistory, { foreignKey: 'userId', onDelete: 'CASCADE' });
ChatHistory.belongsTo(User, { foreignKey: 'userId' });

const db = {
  sequelize,
  User,
  UserSetting,
  Alert,
  LearningLogEntry,
  StockDataPoint,
  ChatHistory,
};

module.exports = db;