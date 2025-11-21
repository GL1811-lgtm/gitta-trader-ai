# Questions

## Question 1: Recurring Issue - Stock Prices Not Showing (3+ hours)

**What's the Root Issue?**

The recurring problem is a **cascading failure chain**:
1. **Method Mismatch**: Backend calls non-existent Angel One API methods
2. **Server Crashes**: This causes 500 errors → entire backend stops responding
3. **Stale Processes**: Old Python processes don't die → new fixes don't apply
4. **Frontend Mismatch**: Frontend calls outdated/wrong API endpoints

**Why It Keeps Happening:**
- **Multiple backend instances running** (you need to kill ALL Python processes each time)
- **Frontend cache** not clearing between updates
- **API endpoint inconsistencies** between what frontend expects vs what backend provides

**Best Resolution:**
```powershell
# 1. KILL ALL backend processes (do this EVERY time you make a change)
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

# 2. Start ONLY ONE backend instance
cd C:\Users\91950\Desktop\gitta-trader-ai
python backend/api/app.py

# 3. Hard refresh browser with Ctrl+Shift+R (NOT just F5)
```

**Permanent Fix Needed:**
- Use a proper process manager (like `pm2` for Python or supervisord)
- Implement proper graceful shutdown in backend
- Add health checks to verify backend is actually running the latest code

---

## Question 2: Black Screen on Individual Agent Reports

**What's Happening?**

This is a **React routing/component crash**. Possible causes:
1. **Agent ID mismatch**: Frontend expects agent ID format that doesn't exist in backend
2. **Missing data**: Component tries to render data that's null/undefined → crashes
3. **API 404**: Agent detail endpoint returns 404 → no fallback UI
4. **Console errors hidden**: React error boundary not catching the crash

**Best Resolution:**

**Step 1: Check browser console** (F12 → Console tab)
- Look for red error messages when you click individual report
- Common errors: "Cannot read property of undefined" or "404 Not Found"

**Step 2: Quick Fix - Add Error Boundaries**
```typescript
// Wrap agent detail page with error boundary
<ErrorBoundary fallback={<div>Failed to load agent report</div>}>
  <AgentDetailPage />
</ErrorBoundary>
```

**Step 3: Verify Agent IDs**
- Check if agent IDs in database match what frontend is requesting
- Example: Frontend looking for "collector-agent-1" but backend has "collector_1"

**Immediate Workaround:**
Open browser DevTools (F12) → Console tab BEFORE clicking agent → see exact error → share with me

---

## Question 3: API Key Shared But No Data Collection

**Why This Happens:**

Multiple possible reasons:
1. **API Not Enabled**: Angel One API requires market data subscription (not just login)
2. **Token Expired**: Access token expires every day → needs re-authentication
3. **Rate Limiting**: Too many requests → API blocks you temporarily
4. **Wrong Market Hours**: Angel One only returns data during market hours (9:15 AM - 3:30 PM IST)
5. **Collector Agents Not Running**: Scripts exist but aren't actually executing

**Best Resolution:**

**Check 1: Verify API Token is Valid**
```powershell
cd C:\Users\91950\Desktop\gitta-trader-ai
python test_angel_one_data.py
```
If this fails → your token is expired → need to re-login

**Check 2: Verify Collectors Are Running**
```powershell
python verify_collectors.py
```
This should show "Collector Agent 1: RUNNING ✅"

**Check 3: Check Market Hours**
Angel One API **only works during**:
- **Monday-Friday, 9:15 AM - 3:30 PM IST**
- Outside these hours → empty data is NORMAL

**Check 4: Manual Test**
```powershell
python fetch_initial_data.py
```
If this works → collectors have a scheduling issue
If this fails → API credentials are wrong

**Permanent Fix:**
1. Set up **token auto-refresh** (re-authenticate daily at 9:00 AM)
2. Add **retry logic** with exponential backoff
3. Implement **data caching** so you have data even when API is down
4. Add **scheduler** to run collectors every 5 minutes during market hours only

---

## 🎯 Priority Actions (Do These NOW)

1. **Kill all Python processes** → Start fresh
2. **Open browser console** (F12) → Check for errors
3. **Run collector verification** → `python verify_collectors.py`
4. **Test API manually** → `python test_angel_one_data.py`

Share the output of these commands and I'll give you the exact next steps! 🚀

