# 🔑 Reddit API Setup Guide

## Quick Setup (5 minutes)

### Step 1: Create Reddit App
1. **Go to:** https://www.reddit.com/prefs/apps
2. Click **"Create App"** or **"Create Another App"**
3. Fill in the form:
   - **Name:** `Gitta-Strategy-Collector` (or anything you want)
   - **App type:** Select **"script"**
   - **Description:** (leave blank or write anything)
   - **About URL:** (leave blank)
   - **Redirect URI:** `http://localhost:8080`
4. Click **"Create app"**

### Step 2: Get Your Credentials

After creating, you'll see your app. Copy these two values:

1. **Client ID** - This is the string under your app name (looks like: `abc123def456xyz`)
   - About 14-20 characters
   
2. **Client Secret** - This is labeled as "secret" (looks like: `ABC123-xyz789_longstring`)
   - Much longer string

### Step 3: Share Credentials

Just paste them here in chat like this:
```
Reddit Client ID: abc123def456xyz
Reddit Secret: ABC123-xyz789_longstring
```

Or if you prefer:
```
ID: abc123def456xyz
Secret: ABC123-xyz789_longstring
```

---

## What This Enables

Once configured, your system will:
- ✅ Monitor r/IndiaInvestments for trading strategies
- ✅ Scan r/stocks and r/algotrading
- ✅ Auto-extract strategy discussions
- ✅ Save to database for testing

**Ready? Go get your Reddit API credentials now!** 🚀
