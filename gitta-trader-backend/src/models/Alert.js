module.exports = (sequelize, DataTypes) => {
  const Alert = sequelize.define('Alert', {
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true,
    },
    instrument: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    type: {
      type: DataTypes.STRING, // 'BUY' or 'SELL'
      allowNull: false,
    },
    confidence: {
      type: DataTypes.FLOAT, // 0-100
      allowNull: false,
    },
    reason: {
      type: DataTypes.TEXT,
      allowNull: true,
    },
    timestamp: {
      type: DataTypes.DATE,
      defaultValue: DataTypes.NOW,
    },
    strikePrice: {
      type: DataTypes.FLOAT,
      allowNull: true,
    },
    targetPrice: {
      type: DataTypes.FLOAT,
      allowNull: true,
    },
    stopLoss: {
      type: DataTypes.FLOAT,
      allowNull: true,
    },
  });
  return Alert;
};