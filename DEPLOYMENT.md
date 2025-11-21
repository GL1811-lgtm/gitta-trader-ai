# 🚀 Gitta Trader AI - Deployment Guide

This guide covers how to deploy Gitta Trader AI locally or on a server (like Google Cloud Platform).

## 📋 Prerequisites
- **Docker** & **Docker Compose** (Recommended)
- **Python 3.10+** (For local run)
- **Node.js 18+** (For frontend)

## 🐳 Docker Deployment (Easiest)

1.  **Build and Run**:
    ```bash
    docker-compose up --build -d
    ```
    This starts:
    - Backend API (Port 5001)
    - Frontend (Port 80)
    - Redis (Port 6379)
    - Celery Worker

2.  **Verify**:
    - Check logs: `docker-compose logs -f`
    - Open `http://localhost`

## 💻 Local Development

1.  **Backend**:
    ```bash
    cd backend
    pip install -r requirements.txt
    python api/app.py
    ```

2.  **Frontend**:
    ```bash
    npm install
    npm run dev
    ```

## 🔑 Environment Variables (.env)

Create a `.env` file in the root directory:

```ini
# Core
FLASK_ENV=production
SECRET_KEY=your_secret_key

# Database
DATABASE_URL=sqlite:///backend/data/gitta.db

# Redis
REDIS_URL=redis://localhost:6379/0

# APIs (Optional but Recommended)
ANGEL_ONE_API_KEY=your_key
GEMINI_API_KEY=your_key

# Google Drive (For Archiving)
GOOGLE_DRIVE_CREDENTIALS_PATH=backend/config/service_account.json
GOOGLE_DRIVE_FOLDER_ID=your_folder_id
```

## ☁️ Google Cloud Platform (Free Tier)

1.  **Create VM**: e2-micro instance (Free Tier).
2.  **Install Docker**: Follow official Docker guide for Debian/Ubuntu.
3.  **Clone Repo**: `git clone <your-repo-url>`
4.  **Run**: `docker-compose up -d`
5.  **Static IP**: Reserve a static external IP for your VM.
