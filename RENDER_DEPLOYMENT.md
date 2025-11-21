# 🚀 Render Deployment Guide - Super Simple!

Deploy Gitta Trader AI to Render.com with **FREE PostgreSQL database** in under 10 minutes.

---

## ✅ Prerequisites

- ✅ GitHub account (you have this!)
- ✅ Render account (you have this!)
- ✅ Your code (ready to go!)

---

## 🎯 Step 1: Push Code to GitHub (AUTOMATED!)

### Just Run This Command:

```powershell
.\deploy_to_render.ps1
```

**That's it!** The script will:
1. ✅ Initialize git (if needed)
2. ✅ Create .gitignore
3. ✅ Commit all files
4. ✅ Ask for your GitHub username
5. ✅ Push to GitHub

### If You Don't Have a Repo Yet:

1. Go to: https://github.com/new
2. **Repository name:** `gitta-trader-ai`
3. **Private** (recommended - your API keys!)
4. Click **"Create repository"**
5. Run the script again

---

## 🎯 Step 2: Deploy on Render

### 2.1 Create Web Service

1. Go to: **https://dashboard.render.com**
2. Click **"New +"** → **"Web Service"**
3. Click **"Connect account"** (if first time) → Authorize GitHub
4. Find **"gitta-trader-ai"** in the list
5. Click **"Connect"**

### 2.2 Configure Service

Render auto-fills most settings from `render.yaml`, but verify:

- **Name:** `gitta-trader-ai-backend` (or whatever you prefer)
- **Region:** Choose closest to you
- **Branch:** `main`
- **Build Command:** (leave empty)
- **Start Command:** `gunicorn --bind 0.0.0.0:$PORT backend.api.app:app`
- **Plan:** ⭐ **Free** ⭐

### 2.3 Add Environment Variables

Click **"Advanced"** → Scroll to **"Environment Variables"**

Add these one by one (click "+ Add Environment Variable" for each):

```ini
GEMINI_API_KEY=<your_gemini_api_key>
GROQ_API_KEY=<your_groq_api_key>
YOUTUBE_API_KEY=<your_youtube_api_key>
OPENAI_API_KEY=<your_openai_api_key>
GOOGLE_DRIVE_FOLDER_ID=<your_google_drive_folder_id>
GOOGLE_DRIVE_ENABLED=true
GOOGLE_DRIVE_CREDENTIALS_PATH=credentials.json
BACKUP_ENABLED=true
ENVIRONMENT=production
CLOUD_PLATFORM=render
ANGEL_ONE_API_KEY=<your_angel_one_api_key>
ANGEL_ONE_SECRET_KEY=<your_angel_one_secret_key>
ANGEL_ONE_TOTP_SECRET=<your_angel_one_totp_secret>
ANGEL_ONE_CLIENT_ID=<your_angel_one_client_id>
ANGEL_ONE_PASSWORD=<your_angel_one_password>
```

### 2.4 Click "Create Web Service"

Render will:
1. 📦 Build your app (2-3 minutes)
2. 🚀 Deploy to a free server
3. 🌐 Give you a live URL!

---

## 🎯 Step 3: Add PostgreSQL Database (Optional)

### 3.1 Create Database

1. Click **"New +"** → **"PostgreSQL"**
2. **Name:** `gitta-trader-db`
3. **Region:** Same as your web service
4. **Plan:** ⭐ **Free** ⭐ (1GB storage)
5. Click **"Create Database"**

### 3.2 Connect to Web Service

1. Go back to your **Web Service**
2. Click **"Environment"** tab
3. Add new variable:
   - **Key:** `DATABASE_URL`
   - **Value:** Click "Add from Database" → Select `gitta-trader-db` → Select "Internal Database URL"

### 3.3 Redeploy

The web service will auto-redeploy with the new database URL!

---

## ✅ Verification

### Check Deployment Status

1. In Render dashboard, your service should show **"Live"** 🟢
2. Click on the service name
3. You'll see your URL: `https://gitta-trader-ai.onrender.com`

### Test Your App

```bash
# Health check
curl https://your-app-url.onrender.com/health

# Should return:
{"status": "healthy", "database": "connected"}
```

### View Logs

- Click **"Logs"** tab in Render dashboard
- See real-time logs
- Check for any errors

---

## 🔄 Auto-Deploy

Every time you push to GitHub:
1. Render automatically detects the change
2. Rebuilds your app
3. Deploys the new version

**Zero downtime deployments!** ✨

---

## 🎁 What You Get FREE

| Feature | Free Tier |
|---------|-----------|
| **Web Service** | 750 hours/month |
| **PostgreSQL** | 1 GB storage |
| **Bandwidth** | 100 GB/month |
| **Auto-deploy** | Unlimited |
| **SSL/HTTPS** | Included |
| **Custom domain** | Supported |

> ⚠️ **Note:** Free services **sleep after 15 minutes** of inactivity. First request after sleep takes 30-60 seconds to wake up.

---

## 📊 Monitoring

### Dashboard Shows:

- ✅ Service status (Live/Building/Failed)
- ✅ Recent deployments
- ✅ Resource usage (CPU, Memory)
- ✅ Request logs
- ✅ Build logs

### Set Up Alerts (Optional):

1. Click service → **"Settings"**
2. Add **"Health Check Path"**: `/health`
3. Get email alerts if service goes down

---

## 🔧 Troubleshooting

### Build Fails

Check logs for:
- Missing dependencies → Update `requirements.txt`
- Python version → Render uses Python 3.11 by default

### Service Won't Start

1. Check **Start Command** is correct:
   ```
   gunicorn --bind 0.0.0.0:$PORT backend.api.app:app
   ```
2. Verify all environment variables are set
3. Check logs for specific errors

### Database Connection Issues

1. Verify `DATABASE_URL` is set
2. Check database is running (should show "Available")
3. Use **Internal Database URL** (not External)

---

## 🚀 Updating Your App

```powershell
# Make your changes
# Then:
git add .
git commit -m "Updated feature X"
git push origin main

# Render auto-deploys!
```

---

## 💰 Cost Breakdown

**Current setup: $0.00/month**

Only charged if you exceed:
- 750 hours/month (always free with 1 service)
- 1 GB database storage
- 100 GB bandwidth

**You're safe!** Your app stays FREE! ✅

---

## 📋 Quick Command Reference

```powershell
# Initial deployment
.\deploy_to_render.ps1

# Update deployment
git add .
git commit -m "Update"
git push

# View local setup
python backend/config.py

# Test Google Drive
python test_google_drive_integration.py
```

---

## 🎉 You're Live!

Once deployed:
1. ✅ Your app is accessible 24/7
2. ✅ Free PostgreSQL database
3. ✅ Auto-deploy on git push
4. ✅ Google Drive backups working
5. ✅ SSL/HTTPS included

**Ready to proceed with your 4-phase multi-agent system!** 🚀

---

## Need Help?

Common Issues:
- **Logs:** See Render dashboard → Logs tab
- **Rebuild:** Dashboard → Manual Deploy → Deploy latest commit
- **Scale:** Settings → Change instance type (will incur charges)

Support:
- Render Docs: https://render.com/docs
- Community: https://community.render.com
