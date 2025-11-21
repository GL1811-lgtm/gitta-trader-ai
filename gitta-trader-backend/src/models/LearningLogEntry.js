module.exports = (sequelize, DataTypes) => {
  const LearningLogEntry = sequelize.define('LearningLogEntry', {
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true,
    },
    timestamp: {
      type: DataTypes.DATE,
      defaultValue: DataTypes.NOW,
    },
    title: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    summary: {
      type: DataTypes.TEXT,
      allowNull: false,
    },
    accuracyChange: {
      type: DataTypes.FLOAT,
      allowNull: true,
    },
  });
  return LearningLogEntry;
};