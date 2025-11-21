const { LearningLogEntry } = require('../models');
const { callGemini } = require('../utils/geminiProxyTemplate');

const getLearningLogs = async (req, res) => {
  try {
    const logs = await LearningLogEntry.findAll({
      order: [['timestamp', 'DESC']],
    });
    res.json(logs);
  } catch (err) {
    console.error('Error fetching learning logs:', err);
    res.status(500).json({ error: 'Failed to fetch learning logs.' });
  }
};

const chatWithMasterAgent = async (req, res) => {
  const { history, newMessage } = req.body;
  try {
    // Build context from learning logs
    const logs = await LearningLogEntry.findAll({
      order: [['timestamp', 'DESC']],
      limit: 10, // Limit context to recent logs
    });
    const context = logs.map(l => `${l.timestamp.toISOString()}: ${l.title} - ${l.summary}`).join('\n');

    const prompt = `You are an AI Master Agent. Your goal is to provide concise and technically clear responses based on the provided context and conversation history.

Context from learning logs:
${context}

Conversation history: ${JSON.stringify(history)}

User: ${newMessage}

Respond concisely with technical clarity.`;

    const geminiResponse = await callGemini({ prompt });

    res.json(geminiResponse);
  } catch (err) {
    console.error('Master Agent chat failed:', err);
    res.status(500).json({ error: 'Master Agent chat failed.' });
  }
};

module.exports = {
  getLearningLogs,
  chatWithMasterAgent,
};
