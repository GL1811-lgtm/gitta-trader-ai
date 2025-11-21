module.exports = (sequelize, DataTypes) => {
  const StockDataPoint = sequelize.define('StockDataPoint', {
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true,
    },
    symbol: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    timestamp: {
      type: DataTypes.DATE,
      allowNull: false,
    },
    open: {
      type: DataTypes.FLOAT,
      allowNull: false,
    },
    high: {
      type: DataTypes.FLOAT,
      allowNull: false,
    },
    low: {
      type: DataTypes.FLOAT,
      allowNull: false,
    },
    close: {
      type: DataTypes.FLOAT,
      allowNull: false,
    },
    volume: {
      type: DataTypes.INTEGER,
      allowNull: false,
    },
  });
  return StockDataPoint;
};