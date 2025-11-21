# User Guide - Gitta Trader AI

Welcome to Gitta Trader AI! This guide will help you get started with the multi-AI verification system.

---

## 📖 Table of Contents

1. [Getting Started](#getting-started)
2. [Using AI Research Page](#using-ai-research-page)
3. [Understanding Verification Results](#understanding-verification-results)
4. [Configuration Options](#configuration-options)
5. [Troubleshooting](#troubleshooting)

---

## 1. Getting Started

### Installation

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   npm install
   ```

2. **Set Up API Key:**
   - Get free API key from [openrouter.ai](https://openrouter.ai)
   - Add to `.env` file:
     ```
     OPENROUTER_API_KEY=sk-or-v1-your-key-here
     ```

3. **Start the Application:**
   ```bash
   # Terminal 1: Backend
   python backend/api/app.py
   
   # Terminal 2: Frontend
   npm run dev
   ```

4. **Open in Browser:**
   - Navigate to `http://localhost:5173`

---

## 2. Using AI Research Page

### Step 1: Navigate to AI Research

- Click **"AI Research"** in the left sidebar
- You'll see the AI verification interface

### Step 2: Enter a Trading Strategy

**Option A: Type Your Own**
```
Example:
Buy when RSI < 30 (oversold)
Sell when RSI > 70 (overbought)
Stop Loss: 2%
Take Profit: 4%
```

**Option B: Load Demo**
- Click **"Load Demo"** button
- Pre-configured strategy will appear

### Step 3: Verify the Strategy

1. Click **"Verify Strategy"** button
2. Wait ~8 seconds for AI analysis
3. See loading spinner while 8 models work

### Step 4: Review Results

You'll see:
- **Consensus Summary Card** (top)
  - Average Score (1-10)
  - Confidence Percentage
  - Recommendation (VIABLE/MODERATE/RISKY)
  - Agreement Rate

- **Individual AI Responses** (below)
  - 8 separate cards
  - Model name and role
  - Analysis content
  - Processing time

---

## 3. Understanding Verification Results

### Confidence Score

**What it means:**
- **80-100%:** High confidence, very reliable
- **70-79%:** Good confidence, acceptable
- **60-69%:** Moderate confidence, review carefully
- **<60%:** Low confidence, strategy rejected

**How it's calculated:**
```
Confidence = (0.4 × Agreement Rate) + 
            (0.2 × Response Count) + 
            (0.2 × Score Consistency) +
            (0.2 × Data Completeness)
```

### Recommendations

**VIABLE:**
- Strategy has good potential
- Multiple models agree
- No major red flags
- ✅ Proceed to testing

**MODERATE:**
- Mixed opinions from models
- Some risks identified
- ⚠️ Review carefully before testing

**RISKY:**
- High risk factors identified
- Models disagree significantly
- ❌ Not recommended for testing

### Individual Scores

Each AI model provides:
- **Score (1-10):** Strategy viability rating
- **Analysis:** Detailed reasoning
- **Duration:** How long the model took

**Score Guide:**
- 8-10: Excellent strategy
- 6-7: Good strategy
- 4-5: Mediocre strategy
- 1-3: Poor strategy

---

## 4. Configuration Options

### Adjust Confidence Threshold

Default is 70%. To change:

**In Code** (for developers):
```python
# backend/agents/collectors/base_collector.py
collector = BaseCollectorAgent(
    "collector-id",
    "Source Name",
    confidence_threshold=75.0  # Require 75% confidence
)
```

### Enable/Disable Specific Models

**Edit:** `backend/ai/config/models_config.py`

```python
{
    "id": "model-id",
    "enabled": False,  # Set to False to disable
    ...
}
```

### Adjust Model Weights

Higher weight = more influence on consensus:

```python
{
    "id": "model-id",
    "weight": 1.5,  # Increase influence
    ...
}
```

---

## 5. Troubleshooting

### "Multi-AI system not available"

**Cause:** OPENROUTER_API_KEY not set

**Solution:**
1. Check `.env` file exists
2. Verify API key is correct
3. Restart backend server

### Verification Taking Too Long

**Normal:** 6-10 seconds  
**If longer:**
- Check internet connection
- Some models may timeout (30s limit)
- Check logs: `backend/data/logs/`

### Low Confidence Scores Consistently

**Possible reasons:**
1. Strategy is genuinely risky
2. Vague or incomplete description
3. Conflicting indicators

**Solution:**
- Add more detail to strategy
- Clarify entry/exit rules
- Specify risk management

### Models Not Responding

**Check:**
1. API key validity at openrouter.ai
2. Internet connection
3. Free tier limits (generous, unlikely)

**View logs:**
```bash
cat backend/data/logs/supervisor.log
```

### UI Not Loading

**Backend not started:**
```bash
python backend/api/app.py
```

**Check port:**
- Backend: `http://localhost:5001`
- Frontend: `http://localhost:5173`

---

## 📊 Tips for Best Results

### Writing Good Strategies

✅ **Do:**
- Specify clear entry/exit rules
- Include risk management (stop loss, take profit)
- Mention timeframe
- Describe indicators used

❌ **Don't:**
- Use vague language
- Skip risk management
- Contradict yourself
- Use overly complex jargon

### Example Good Strategy

```
Trading Strategy: RSI Mean Reversion on NIFTY 50

Entry Rules:
- BUY when RSI(14) < 30 on 15-minute chart
- Confirm with price below 20 EMA

Exit Rules:
- SELL when RSI(14) > 50
- Or stop loss at 2% below entry
- Take profit at 4% above entry

Risk Management:
- Max position size: 5% of capital
- Max 3 trades per day
- Only trade during market hours (9:30 AM - 3:30 PM)

Timeframe: 15 minutes
Indicators: RSI(14), EMA(20)
```

---

## 🎯 Quick Reference

**Start System:**
```bash
python backend/api/app.py  # Backend
npm run dev                # Frontend
```

**Access UI:**  
`http://localhost:5173`

**API Endpoints:**
- Verify: `POST /api/ai/verify`
- Models: `GET /api/ai/models`
- Stats: `GET /api/ai/stats`
- Demo: `GET /api/demo/multi-ai-research`

**Test System:**
```bash
python test_multi_ai_system.py
```

---

## 📚 Additional Resources

- **Multi-AI System:** [OPENROUTER_INTEGRATION.md](OPENROUTER_INTEGRATION.md)
- **Deployment:** [CLOUD_DEPLOYMENT.md](CLOUD_DEPLOYMENT.md)
- **Changes:** [CHANGELOG.md](CHANGELOG.md)
- **Main README:** [README.md](README.md)

---

## 🆘 Getting Help

**Still stuck?**
1. Check the troubleshooting section above
2. Review logs in `backend/data/logs/`
3. Test with demo: Click "Load Demo" button
4. Verify API key at [openrouter.ai](https://openrouter.ai)

---

**Guide Version:** 1.0  
**Last Updated:** 2025-11-20  
**Status:** Complete ✅
