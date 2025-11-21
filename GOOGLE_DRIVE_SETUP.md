# ☁️ Google Drive API Setup Guide

## Setup (10 minutes)

### Step 1: Go to Google Cloud Console
**Visit:** https://console.cloud.google.com/

### Step 2: Create Project (if needed)
- Click **"Select Project"** → **"New Project"**
- Name: `Gitta-Trader-Backup`
- Click **"CREATE"**

### Step 3: Enable Google Drive API
1. Go to **"APIs & Services"** → **"Library"**
2. Search: **"Google Drive API"**
3. Click **"ENABLE"**

### Step 4: Create Service Account
1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"+ CREATE CREDENTIALS"** → **"Service Account"**
3. Fill in:
   - **Service account name:** `gitta-backup`
   - Click **"CREATE AND CONTINUE"**
4. **Role:** Select **"Editor"**
5. Click **"CONTINUE"** → **"DONE"**

### Step 5: Create JSON Key
1. Click on the service account you just created
2. Go to **"KEYS"** tab
3. Click **"ADD KEY"** → **"Create new key"**
4. Select **"JSON"**
5. Click **"CREATE"**
6. **Save the downloaded file as:** `credentials.json`

### Step 6: Create Google Drive Folder
1. Go to: https://drive.google.com
2. Click **"New"** → **"Folder"**
3. Name: `Gitta-Trader-Backups`
4. **Right-click folder** → **"Share"**
5. Add the **service account email** (looks like: `gitta-backup@project-id.iam.gserviceaccount.com`)
   - You can find this email in the credentials.json file
   - Or in Google Cloud Console under service account details
6. Give **Editor** access
7. Click **"Share"**

### Step 7: Get Folder ID
1. Open the folder in Google Drive
2. Look at the URL: `https://drive.google.com/drive/folders/1aBcDeFg...`
3. Copy everything after `/folders/` - that's your folder ID

### Step 8: Place credentials.json
Move the downloaded `credentials.json` to:
```
c:\Users\91950\Desktop\gitta-trader-ai\credentials.json
```

### Step 9: Share Info
Tell me:
```
Folder ID: 1aBcDeFg...
```

I'll configure the rest!

---

## What This Enables

- ✅ Auto-backup at 11 PM daily
- ✅ Cloud storage of all reports
- ✅ Historical data preserved
- ✅ Access from anywhere

**This takes a bit longer but provides huge value!** ☁️
