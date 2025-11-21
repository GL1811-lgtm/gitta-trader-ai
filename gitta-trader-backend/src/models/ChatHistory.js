module.exports = (sequelize, DataTypes) => {
  const ChatHistory = sequelize.define('ChatHistory', {
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
    symbol: {
      type: DataTypes.STRING,
      allowNull: true, // Can be null for general chats
    },
    messages: {
      type: DataTypes.JSONB, // Stores JSON array of messages
      allowNull: false,
      defaultValue: [],
    },
  });
  return ChatHistory;
};