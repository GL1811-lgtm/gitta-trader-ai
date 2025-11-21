const { callGemini } = require('../utils/geminiProxyTemplate');

const getGeminiAnalysis = async (req, res) => {
  const { prompt, history } = req.body;
  try {
    const geminiResponse = await callGemini({ prompt, history });
    res.json(geminiResponse);
  } catch (err) {
    console.error('Gemini analysis failed:', err);
    res.status(500).json({ error: 'Gemini analysis failed.' });
  }
};

module.exports = {
  getGeminiAnalysis,
};
