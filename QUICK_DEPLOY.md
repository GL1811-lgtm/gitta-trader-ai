# 🚀 Quick Start: Cloud Deployment Guide

Complete guide to deploy Gitta Trader AI to the cloud with free database and Google Drive backups.

---

## Option 1: Railway.app (Recommended ⭐)

**Why Railway?** Easiest setup, includes free PostgreSQL, generous free tier.

### Step 1: Prepare Your Project

```bash
# Make sure all changes are committed
git add .
git commit -m "Prepare for cloud deployment"
```

### Step 2: Run Deployment Script

**On Windows:**
```powershell
.\deploy_railway.ps1
```

**On Mac/Linux:**
```bash
chmod +x deploy_railway.sh
./deploy_railway.sh
```

### Step 3: Access Your App

```bash
# Get your app URL
railway open

# View logs
railway logs

# Check status
railway status
```

**Done!** Your app is live with PostgreSQL database 🎉

---

## Option 2: Google Cloud Platform (GCP)

**Why GCP?** Always-free e2-micro instance, full control, 30GB storage.

### Follow Existing Guide

See [`CLOUD_DEPLOYMENT.md`](file:///c:/Users/91950/Desktop/gitta-trader-ai/CLOUD_DEPLOYMENT.md) for detailed GCP setup.

**Key difference:** With new config, it works with both SQLite and PostgreSQL!

---

## Google Drive Setup

### Quick Setup (5 minutes)

Run the interactive wizard:

```bash
python setup_google_drive.py
```

The wizard will:
1. ✅ Check your `credentials.json`
2. ✅ Ask for your Google Drive Folder ID
3. ✅ Update your `.env` file
4. ✅ Test the connection

### Manual Setup

If you prefer manual setup, see [`GOOGLE_DRIVE_SETUP.md`](file:///c:/Users/91950/Desktop/gitta-trader-ai/GOOGLE_DRIVE_SETUP.md)

**Already have credentials.json?** Just need to add folder ID to `.env`:

```ini
GOOGLE_DRIVE_FOLDER_ID=your_folder_id_here
```

---

## Testing Your Setup

### Test Database Connection

```bash
python test_cloud_db.py
```

This will verify:
- ✅ Database configuration
- ✅ Connection to PostgreSQL or SQLite
- ✅ Tables exist
- ✅ CRUD operations work

### Test Google Drive

```bash
python test_google_drive_integration.py
```

This will verify:
- ✅ Credentials are valid
- ✅ Connection to Google Drive
- ✅ Can upload files
- ✅ Can list backups
- ✅ Database backup works

---

## Configuration

### Environment Variables

Your `.env` file should have:

```ini
# Database (for cloud deployment)
DATABASE_URL=postgresql://user:pass@host:port/db  # Railway sets this automatically

# Google Drive (for backups)
GOOGLE_DRIVE_FOLDER_ID=your_folder_id_here
GOOGLE_DRIVE_ENABLED=true
BACKUP_ENABLED=true

# API Keys
GEMINI_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
# ... other keys
```

### What Gets Backed Up?

✅ **Database** - Full backup at 11 PM daily  
✅ **Reports** - Daily, morning, and evening reports  
✅ **Auto cleanup** - Keeps last 7 days of backups

---

## Common Commands

### Railway Deployment

```bash
# Deploy/Update
railway up

# View logs
railway logs

# Open app in browser
railway open

# Run commands in production
railway run python test_cloud_db.py
```

### Google Drive Operations

```bash
# Manual database backup
python -c "from backend.services.google_drive_service import backup_now; backup_now()"

# List all backups
python -c "from backend.services.google_drive_service import list_all_backups; backups = list_all_backups(); print(f'{len(backups)} backups found')"

# Restore latest backup
python -c "from backend.services.google_drive_service import restore_latest_backup; restore_latest_backup()"
```

---

## Verification Checklist

Before going live, verify:

- [ ] Database connection works (`python test_cloud_db.py`)
- [ ] Google Drive connection works (`python test_google_drive_integration.py`)
- [ ] All API keys are set in `.env`
- [ ] App deploys successfully to Railway/GCP
- [ ] Can access app via public URL
- [ ] Agents are running and collecting data
- [ ] Backups are being created in Google Drive

---

## Troubleshooting

### Database Issues

**Problem:** Can't connect to database

**Solution:**
```bash
# Check DATABASE_URL is set (Railway sets this automatically)
railway variables

# On GCP, make sure SQLite path is correct
echo $DATABASE_PATH
```

### Google Drive Issues

**Problem:** Can't connect to Google Drive

**Solution:**
1. Check `credentials.json` exists
2. Verify folder ID in `.env`
3. Make sure folder is shared with service account email
4. Run: `python test_google_drive_integration.py`

### Deployment Issues

**Problem:** Railway deployment fails

**Solution:**
```bash
# Check logs
railway logs

# Verify all dependencies are in requirements.txt
pip freeze > requirements.txt

# Redeploy
railway up --detach
```

---

## Cost Summary

All options below are **FREE**:

| Platform | Database | Storage | What You Get |
|----------|----------|---------|--------------|
| **Railway** | PostgreSQL 500MB | 1GB | 500 hours/month |
| **GCP** | SQLite | 30GB | Always-free e2-micro |
| **Google Drive** | N/A | 15GB free | Unlimited backups* |

*Within 15GB free tier

---

## Next Steps

Once deployed:

1. **Configure Scheduled Tasks** - Set up morning (8 AM) and evening (5 PM) reports
2. **Add Monitoring** - Set up Grafana dashboards
3. **Phase 1-4 Agents** - Start implementing your multi-agent system!

Ready to proceed with the 4-phase plan? Let me know! 🚀
