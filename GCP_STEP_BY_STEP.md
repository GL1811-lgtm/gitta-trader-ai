# 🚀 GCP Step-by-Step Deployment Guide

**You're currently here:** GCP Compute Engine → Overview (showing 0 VMs)

Follow these exact steps to deploy Gitta Trader AI to Google Cloud Platform.

---

## ✅ Step 1: Create VM Instance (You are here!)

### 1.1 Click "Create Instance"

In your current page, click the blue **"Create Instance"** button at the top.

### 1.2 Configure VM Settings

Fill in the following (screenshot each section if unsure):

#### **Name and Region**
- **Name:** `gitta-trader-ai`
- **Region:** Choose closest to India (e.g., `asia-south1` - Mumbai)
- **Zone:** `asia-south1-a` (or any -a/-b/-c)

#### **Machine Configuration**
- **Series:** `E2`
- **Machine type:** Click "CHANGE" → Select **`e2-micro`**
  - ⚠️ **CRITICAL:** This MUST be `e2-micro` to stay FREE
  - Shows: "0.25-2 vCPU, 1 GB memory"
  - Should say "Free tier eligible" ✅

#### **Boot Disk**
- Click "CHANGE"
- **Operating System:** `Debian`
- **Version:** `Debian GNU/Linux 11 (bullseye)`
- **Boot disk type:** `Standard persistent disk`
- **Size:** `30 GB` (maximum free tier)
- Click "SELECT"

#### **Firewall**
- ✅ Check **"Allow HTTP traffic"**
- ✅ Check **"Allow HTTPS traffic"**

### 1.3 Click "CREATE"

Wait 1-2 minutes for VM to be created.

---

## ✅ Step 2: Configure Firewall Rules

### 2.1 Go to Firewall Settings

In the left menu:
1. Click on **"VPC network"** (scroll down if needed)
2. Click **"Firewall"**

### 2.2 Create Firewall Rule

1. Click **"Create Firewall Rule"** (top)
2. Fill in:
   - **Name:** `gitta-trader-ports`
   - **Direction of traffic:** `Ingress`
   - **Action on match:** `Allow`
   - **Targets:** `All instances in the network`
   - **Source filter:** `IPv4 ranges`
   - **Source IPv4 ranges:** `0.0.0.0/0`
   - **Protocols and ports:**
     - ✅ Check "TCP"
     - Enter: `5001, 5173, 3001, 9090`

3. Click **"CREATE"**

---

## ✅ Step 3: Connect to VM and Deploy

### 3.1 Go Back to VM Instances

- Navigate back to: **Compute Engine → VM instances**
- You should see your `gitta-trader-ai` VM running

### 3.2 Connect via SSH

- Click the **"SSH"** button next to your VM
- A terminal window will open in your browser

### 3.3 Run These Commands

Copy and paste each command one by one:

```bash
# 1. Update system
sudo apt-get update && sudo apt-get upgrade -y

# 2. Install Git
sudo apt-get install -y git

# 3. Install Python and pip
sudo apt-get install -y python3 python3-pip python3-venv

# 4. Install Node.js (for frontend)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 5. Clone your repository (if pushed to GitHub)
# OR upload your code using:
# - Google Cloud Console → Cloud Shell → Upload file
# - Or use git clone if you've pushed to GitHub

# For now, let's verify installations
python3 --version
node --version
npm --version
```

---

## ✅ Step 4: Upload Your Code

You have 2 options:

### Option A: Use Git (Recommended)

```bash
# If you've pushed to GitHub:
git clone https://github.com/YOUR_USERNAME/gitta-trader-ai.git
cd gitta-trader-ai
```

### Option B: Upload Files

1. In the SSH terminal, click the **⚙️ gear icon** (top right)
2. Click **"Upload file"**
3. Upload your entire `gitta-trader-ai` folder as a zip
4. Unzip:
```bash
unzip gitta-trader-ai.zip
cd gitta-trader-ai
```

---

## ✅ Step 5: Install Dependencies and Run

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
npm install

# Build frontend
npm run build

# Start backend
cd backend
python3 api/app.py
```

---

## ✅ Step 6: Get Your Public IP

### 6.1 Find Your VM's External IP

- Go back to: **Compute Engine → VM instances**
- Look for **"External IP"** column
- Copy that IP address (e.g., `34.93.123.456`)

### 6.2 Access Your Application

Open in browser:
- **Frontend:** `http://YOUR_EXTERNAL_IP:5173`
- **Backend API:** `http://YOUR_EXTERNAL_IP:5001/health`

---

## ✅ Step 7: Make IP Static (Optional but Recommended)

### 7.1 Reserve Static IP

1. Go to: **VPC network → External IP addresses**
2. Find your VM's IP
3. Click **Type dropdown** → Select **"Static"**
4. Give it a name: `gitta-trader-static-ip`
5. Click **"RESERVE"**

Now your IP won't change even if you stop/start the VM!

---

## 🎯 Quick Commands Reference

Once deployed, you can manage your VM:

```bash
# Start VM
gcloud compute instances start gitta-trader-ai --zone=asia-south1-a

# Stop VM
gcloud compute instances stop gitta-trader-ai --zone=asia-south1-a

# SSH into VM
gcloud compute ssh gitta-trader-ai --zone=asia-south1-a

# View logs
cd gitta-trader-ai
tail -f logs/gitta_trader.log
```

---

## 🆘 Troubleshooting

### Can't access from browser?
- ✅ Check firewall rules are created
- ✅ Verify backend is running: `curl http://localhost:5001/health`
- ✅ Check VM external IP is correct

### Out of memory?
- e2-micro has only 1GB RAM
- Stop unnecessary services
- Or upgrade to e2-small (will incur charges)

### Backend won't start?
```bash
# Check Python version
python3 --version  # Should be 3.7+

# Check logs
python3 backend/api/app.py
```

---

## 📊 Current Setup Status

✅ **Google Drive:** Configured with folder ID  
✅ **Database:** Using SQLite (local file)  
✅ **Backups:** Will auto-backup to Google Drive at 11 PM  
✅ **Free Tier:** Using e2-micro (always free)  

---

## What To Do Right Now

**You are on this screen:**
![GCP Compute Engine Overview](file:///C:/Users/91950/.gemini/antigravity/brain/cf388e9c-26a5-466a-98e0-f379e7e57641/uploaded_image_1763697970492.png)

**Next action:** Click the blue **"Create Instance"** button!

Then follow **Step 1.2** above to configure the VM settings.

---

Need help with any step? Just let me know where you're stuck! 🚀
