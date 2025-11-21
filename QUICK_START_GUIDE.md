# 🚀 Quick Start Guide - Get Real Data Flowing

**Goal**: Get your Gitta Trader AI system collecting real market data in 4-6 hours.

---

## Step 1: Get Angel One API Credentials (30 minutes)

### Option A: If you already have an Angel One account

1. Login to Angel One Portal:
   - Go to https://smartapi.angelbroking.com/
   - Login with your Angel One credentials

2. Generate API Key:
   - Navigate to "API" section
   - Click "Create App"
   - Fill in app details
   - **Copy your API Key** (you'll need this)

3. Get Client ID:
   - This is your Angel One client code (e.g., A123456)
   - Found in your Angel One account profile

4. Generate TOTP Secret:
   - In API settings, enable 2FA
   - **Save the TOTP secret key** (shown as QR code secret)
   - This is used to generate time-based OTP automatically

### Option B: If you DON'T have Angel One account

1. Open Angel One account:
   - Visit: https://www.angelone.in/
   - Click "Open Demat Account"
   - Complete KYC process (takes 1-2 days)
   
2. **Alternative for immediate testing**:
   - We can use **mock data mode** temporarily
   - Skip to Step 3 and I'll set up simulated data

---

## Step 2: Configure Environment Variables (5 minutes)

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file with your credentials:
   ```bash
   ANGEL_ONE_API_KEY=your_actual_api_key
   ANGEL_ONE_CLIENT_ID=A123456
   ANGEL_ONE_PASSWORD=your_angel_one_password
   ANGEL_ONE_TOTP_SECRET=your_totp_secret_key
   ```

3. **Important**: Add `.env` to `.gitignore` (don't commit secrets!)

---

## Step 3: Test Angel One Connection (5 minutes)

Run the connection test:

```bash
cd C:\Users\91950\Desktop\gitta-trader-ai
python test_angel_one.py
```

**Expected Output**:
```
✅ Angel One API connected successfully for A123456
✅ Fetched NIFTY 50 from Angel One: 23456.78
✅ Fetched BANKNIFTY from Angel One: 45678.90
```

**If it fails**:
- Check credentials are correct
- Verify TOTP secret is correct
- Check if API is enabled in Angel One portal

---

## Step 4: Start Continuous Data Collection (2 minutes)

### Option A: Using Supervisor (Recommended)

```bash
cd C:\Users\91950\Desktop\gitta-trader-ai
python backend/agents/supervisor/run_supervisor.py
```

This will:
- Start all 5 collector agents
- Collect data every 3 seconds
- Save to database automatically
- Run 24/7 until you stop it

### Option B: Manual Collection (for testing)

```bash
python backend/agents/collectors/run_all.py
```

---

## Step 5: Verify Data is Flowing (5 minutes)

### Check 1: Database has new entries

```bash
python -c "from backend.database.db import db; import datetime; data = db.get_latest_market_data('NIFTY'); print(f'Latest NIFTY data: {data}')"
```

**Expected**: Should show recent timestamp (within last minute)

### Check 2: Frontend displays live data

1. Open browser: http://localhost:3000
2. Look for:
   - NIFTY 50 price (should be updating)
   - BANKNIFTY price (should be updating)
   - Last updated timestamp (should be recent)

### Check 3: Agent status

```bash
curl http://localhost:5000/api/agents/status
```

**Expected**: All collectors should show "Active" with recent timestamps

---

## Step 6: Implement Missing Functions (2-3 hours)

Now that you have Angel One working, let's complete the 3 missing functions.

### 6.1: Implement VIX Fetching

Edit: `backend/agents/collectors/market_data.py`

Find line 135 and replace:
```python
def get_vix(self) -> float:
    # TODO: Implement VIX fetching
    return 0.0
```

With:
```python
def get_vix(self) -> float:
    """Fetch India VIX from Angel One."""
    if self.angel_client and self.auth_token:
        try:
            vix_token = {"exchange": "NSE", "token": "99926037", "symbol": "India VIX"}
            ltp_data = self.angel_client.ltpData(
                vix_token["exchange"],
                vix_token["symbol"],
                vix_token["token"]
            )
            if ltp_data and ltp_data.get('status') and ltp_data.get('data'):
                return float(ltp_data['data']['ltp'])
        except Exception as e:
            logger.error(f"Error fetching VIX: {e}")
    return 0.0
```

### 6.2: Implement Option Chain

Find line 143 and replace the `get_option_chain()` function with actual implementation.

**Note**: Option chain requires additional Angel One API calls. I'll provide the implementation after VIX is working.

### 6.3: Implement FII/DII Data

Find line 152 and replace the `get_fii_dii_data()` function.

**Note**: FII/DII data comes from NSE website scraping or specialized APIs. I'll provide implementation.

---

## Step 7: Final Verification (10 minutes)

Run the complete test suite:

```bash
python test_end_to_end.py
```

This will verify:
- ✅ Angel One API connected
- ✅ All collectors running
- ✅ Data flowing to database
- ✅ Testers processing strategies
- ✅ Frontend displaying data
- ✅ Supervisor orchestrating everything

---

## 🎯 Success Criteria

After completing this quick start, you should have:

1. ✅ Angel One API connected and fetching real data
2. ✅ All 5 collectors running continuously
3. ✅ Database receiving updates every 3 seconds
4. ✅ Frontend showing live NIFTY/BANKNIFTY prices
5. ✅ VIX data displaying (if implemented)
6. ✅ System running 24/7 automatically

---

## ⏭️ What's Next?

After quick start is complete:

1. **Download Historical Data** (Phase 1, Day 2)
   - 20 years NIFTY data
   - 20 years BANKNIFTY data
   - 10 years Option Chain

2. **Enable Evolution System** (Phase 2)
   - Genetic algorithm for strategy optimization
   - Runs automatically every night at 11 PM

3. **Complete Implementation Guide** (Days 1-30)
   - Follow the 6-phase roadmap
   - Build full self-improving system

---

## 🆘 Troubleshooting

### Issue: Angel One connection fails
- **Check**: API credentials in .env file
- **Check**: API is enabled in Angel One portal
- **Check**: TOTP secret is correct (32-character key)

### Issue: No data in database
- **Check**: Supervisor is running (`ps aux | grep supervisor`)
- **Check**: Angel One API is connected (check logs)
- **Check**: Database file exists (`backend/data/gitta.db`)

### Issue: Frontend shows "No data"
- **Check**: Backend is running on port 5000
- **Check**: Database has entries (run query above)
- **Check**: CORS is configured correctly

---

## 📞 Need Help?

If you encounter issues:

1. **Check logs**: `backend/agents/collectors/logs/`
2. **Test API**: Run `python test_angel_one.py`
3. **Check database**: Run `python check_db.py`
4. **Ask me**: I'm here to help! Just describe the error.

---

**Ready to start?** 

Let me know if you:
- **Have Angel One credentials** → We'll configure them now
- **Need to apply for API** → I'll set up mock data temporarily
- **Want to see a demo first** → I'll show you what it looks like with sample data
