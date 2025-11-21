const axios = require('axios');
const dotenv = require('dotenv');
dotenv.config();

const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
const GEMINI_API_URL = process.env.GEMINI_API_URL; // e.g., https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent

const callGemini = async ({ prompt, history = [] }) => {
  if (!GEMINI_API_KEY || !GEMINI_API_URL) {
    console.error('GEMINI_API_KEY or GEMINI_API_URL not set in environment variables.');
    return { error: 'Gemini API not configured.' };
  }

  const messages = history.map(msg => ({
    role: msg.sender === 'user' ? 'user' : 'model',
    parts: [{ text: msg.text }],
  }));

  messages.push({
    role: 'user',
    parts: [{ text: prompt }],
  });

  try {
    const response = await axios.post(
      `${GEMINI_API_URL}?key=${GEMINI_API_KEY}`,
      {
        contents: messages,
      },
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );

    const geminiResponse = response.data.candidates[0].content.parts[0].text;
    return { response: geminiResponse };
  } catch (error) {
    console.error('Error calling Gemini API:', error.response ? error.response.data : error.message);
    return { error: 'Failed to get response from Gemini API.' };
  }
};

module.exports = {
  callGemini,
};