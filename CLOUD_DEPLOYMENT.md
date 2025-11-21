# 🚀 Cloud Deployment Guide - Gitta Trader AI

Complete step-by-step guide to deploy Gitta Trader AI on Google Cloud Platform (GCP) Free Tier.

## 📋 Prerequisites

- **GCP Account**: Sign up at [cloud.google.com](https://cloud.google.com) (Free tier includes $300 credit)
- **Git**: Installed on your local machine
- **SSH Client**: For connecting to the VM

## 🎯 Deployment Overview

We'll deploy the full stack:
- ✅ Backend API (Flask) on port 5001
- ✅ Frontend (React/Vite) on port 5173
- ✅ Redis for caching
- ✅ Multi-agent system (Collectors, Testers, Supervisor, Expert)
- ✅ Scheduled tasks (8 AM morning scan, 5 PM evening validation)
- ✅ Monitoring (Prometheus + Grafana)

---

## 🔧 Step 1: Create GCP VM Instance

### 1.1 Create VM
1. Go to [GCP Console](https://console.cloud.google.com)
2. Navigate to **Compute Engine** > **VM Instances**
3. Click **Create Instance**
4. Configure:
   - **Name**: `gitta-trader-ai`
   - **Region**: Choose closest to you (e.g., `us-central1`)
   - **Machine type**: `e2-micro` (Free tier eligible - 0.25-2 vCPU, 1 GB memory)
   - **Boot disk**: 
     - OS: `Debian GNU/Linux 11 (bullseye)`
     - Size: `30 GB` (Free tier includes 30 GB)
   - **Firewall**: 
     - ✅ Allow HTTP traffic
     - ✅ Allow HTTPS traffic

### 1.2 Configure Firewall Rules
1. Go to **VPC Network** > **Firewall**
2. Click **Create Firewall Rule**
3. Configure:
   - **Name**: `gitta-trader-ports`
   - **Direction**: Ingress
   - **Targets**: All instances in network
   - **Source IP ranges**: `0.0.0.0/0` (or restrict to your IP for security)
   - **Protocols and ports**: 
     - `tcp:5001` (Backend API)
     - `tcp:5173` (Frontend)
     - `tcp:3001` (Grafana)
     - `tcp:9090` (Prometheus)
4. Click **Create**

### 1.3 Reserve Static IP (Optional but Recommended)
1. Go to **VPC Network** > **External IP addresses**
2. Find your VM's IP
3. Click **Type** dropdown > **Static**
4. Give it a name and confirm

---

## 🚀 Step 2: Deploy Application

### 2.1 Connect to VM
```bash
# From GCP Console, click "SSH" button next to your VM
# Or use gcloud CLI:
gcloud compute ssh gitta-trader-ai --zone=us-central1-a
```

### 2.2 Run Automated Setup Script
```bash
# Download and run the setup script
curl -o setup.sh https://raw.githubusercontent.com/YOUR_USERNAME/gitta-trader-ai/main/gcp_setup.sh
chmod +x setup.sh
./setup.sh
```

**OR** manually follow these steps:

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
sudo apt-get install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone repository
git clone https://github.com/YOUR_USERNAME/gitta-trader-ai.git
cd gitta-trader-ai
```

### 2.3 Configure Environment Variables
```bash
# Copy production template
cp .env.production .env

# Edit with your API keys
nano .env
```

**Required configurations:**
```ini
# Get your VM's external IP
VITE_BACKEND_URL=http://YOUR_VM_EXTERNAL_IP:5001/api
CORS_ORIGINS=http://YOUR_VM_EXTERNAL_IP:5173

# Add your API keys
GROQ_API_KEY=your_actual_groq_key
YOUTUBE_API_KEY=your_actual_youtube_key
# ... other keys
```

Save and exit (`Ctrl+X`, then `Y`, then `Enter`)

### 2.4 Start Application
```bash
# Build and start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

---

## ✅ Step 3: Verify Deployment

### 3.1 Check Services
```bash
# All services should show "Up"
docker-compose ps

# Check health
curl http://localhost:5001/health
```

Expected response:
```json
{"status": "healthy", "database": "connected", "timestamp": "..."}
```

### 3.2 Access Application
Open in your browser:
- **Frontend**: `http://YOUR_VM_EXTERNAL_IP:5173`
- **Backend API**: `http://YOUR_VM_EXTERNAL_IP:5001/api/health`
- **Grafana**: `http://YOUR_VM_EXTERNAL_IP:3001` (username: `admin`, password: `admin`)
- **Prometheus**: `http://YOUR_VM_EXTERNAL_IP:9090`

### 3.3 Test API Endpoints
```bash
# Get latest report
curl http://YOUR_VM_EXTERNAL_IP:5001/api/reports/latest

# Trigger workflow
curl -X POST http://YOUR_VM_EXTERNAL_IP:5001/api/workflow/run

# Check scheduled jobs
curl http://YOUR_VM_EXTERNAL_IP:5001/api/scheduler/jobs
```

---

## 📊 Step 4: Monitor & Maintain

### 4.1 View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### 4.2 Restart Services
```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
```

### 4.3 Update Application
```bash
cd gitta-trader-ai
git pull
docker-compose down
docker-compose up -d --build
```

### 4.4 Check Resource Usage
```bash
# Disk usage
df -h

# Memory usage
free -h

# Docker stats
docker stats
```

---

## 🔒 Step 5: Security Hardening (Recommended)

### 5.1 Restrict Firewall
Update firewall rule to allow only your IP:
```bash
# In GCP Console > VPC Network > Firewall
# Change Source IP ranges from 0.0.0.0/0 to YOUR_IP/32
```

### 5.2 Set Up HTTPS (Optional)
Use Let's Encrypt with Nginx:
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### 5.3 Enable Automatic Updates
```bash
sudo apt-get install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

---

## 🎯 Step 6: Set Up Domain (Optional)

### 6.1 Point Domain to VM
1. Get your VM's static IP
2. In your domain registrar (GoDaddy, Namecheap, etc.):
   - Add **A Record**: `@` → `YOUR_VM_IP`
   - Add **A Record**: `www` → `YOUR_VM_IP`

### 6.2 Update Environment
```bash
nano .env
```
Update:
```ini
VITE_BACKEND_URL=http://yourdomain.com:5001/api
CORS_ORIGINS=http://yourdomain.com
```

Restart:
```bash
docker-compose restart
```

---

## 🆘 Troubleshooting

### Issue: Services won't start
```bash
# Check logs
docker-compose logs

# Check disk space
df -h

# Rebuild
docker-compose down
docker-compose up -d --build
```

### Issue: Can't access from browser
```bash
# Check firewall rules in GCP Console
# Verify services are running
docker-compose ps

# Check if ports are listening
sudo netstat -tulpn | grep -E '5001|5173'
```

### Issue: Out of memory
```bash
# Check memory
free -h

# Reduce services (disable Grafana/Prometheus if needed)
# Edit docker-compose.yml and comment out grafana/prometheus sections
```

### Issue: Database errors
```bash
# Reset database
docker-compose exec backend python -c "from backend.database.db import db; db.init_db()"
```

---

## 📈 Cost Optimization

**GCP Free Tier includes:**
- ✅ 1 e2-micro VM (up to 30 GB storage)
- ✅ 1 GB network egress per month
- ✅ $300 credit for 90 days

**To stay within free tier:**
- Use e2-micro instance
- Monitor network egress
- Stop VM when not in use: `gcloud compute instances stop gitta-trader-ai`
- Start when needed: `gcloud compute instances start gitta-trader-ai`

---

## 🎉 Success!

Your Gitta Trader AI is now running 24/7 on Google Cloud Platform!

**Next Steps:**
1. Monitor the morning scan (8 AM) and evening validation (5 PM)
2. Check Grafana dashboards for system metrics
3. Set up Telegram notifications for alerts
4. Configure Google Drive archiving for backups

**Support:**
- Check logs: `docker-compose logs -f`
- System status: `http://YOUR_IP:5001/api/system/status`
- Health check: `http://YOUR_IP:5001/health`
