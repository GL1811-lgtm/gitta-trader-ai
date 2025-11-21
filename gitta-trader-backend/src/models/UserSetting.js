module.exports = (sequelize, DataTypes) => {
  const UserSetting = sequelize.define('UserSetting', {
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true,
    },
    userId: {
      type: DataTypes.INTEGER,
      allowNull: false,
      references: {
        model: 'Users', // This is the table name
        key: 'id',
      },
    },
    theme: {
      type: DataTypes.STRING,
      defaultValue: 'dark',
    },
    webPushNotifications: {
      type: DataTypes.BOOLEAN,
      defaultValue: false,
    },
    emailAlerts: {
      type: DataTypes.BOOLEAN,
      defaultValue: false,
    },
    confidenceThreshold: {
      type: DataTypes.INTEGER,
      defaultValue: 75, // 50-95
    },
  });
  return UserSetting;
};