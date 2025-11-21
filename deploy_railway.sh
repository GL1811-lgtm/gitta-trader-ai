#!/bin/bash
# Railway Deployment Script for Gitta Trader AI
# This script automates the deployment to Railway.app

set -e  # Exit on error

echo "======================================================================"
echo "         GITTA TRADER AI - RAILWAY DEPLOYMENT"
echo "======================================================================"
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Railway CLI not found. Installing..."
    echo ""
    
    # Install Railway CLI
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install railway
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        bash <(curl -fsSL https://railway.app/install.sh)
    else
        echo "❌ Unsupported OS. Please install Railway CLI manually:"
        echo "   Visit: https://docs.railway.app/develop/cli#installation"
        exit 1
    fi
    
    echo "✅ Railway CLI installed"
fi

echo "🔐 Logging in to Railway..."
railway login

echo ""
echo "📋 Creating new Railway project..."
echo "   Project name: gitta-trader-ai"
echo ""

# Initialize Railway project
railway init

echo ""
echo "🐘 Adding PostgreSQL database..."
railway add --plugin postgresql

echo ""
echo "⚙️  Setting up environment variables..."
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Please create one from .env.example"
    exit 1
fi

# Read important variables from .env and set them in Railway
while IFS='=' read -r key value; do
    # Skip comments and empty lines
    [[ $key =~ ^#.*$ ]] && continue
    [[ -z $key ]] && continue
    
    # Skip DATABASE_URL (Railway sets this automatically)
    [[ $key == "DATABASE_URL" ]] && continue
    
    # Remove quotes from value
    value="${value%\"}"
    value="${value#\"}"
    
    # Set in Railway
    if [ -n "$value" ] && [ "$value" != "your_*" ]; then
        echo "Setting $key..."
        railway variables --set "$key=$value"
    fi
done < .env

# Set production environment
railway variables --set ENVIRONMENT=production

echo ""
echo "🚀 Deploying to Railway..."
railway up

echo ""
echo "======================================================================"
echo "✅ DEPLOYMENT COMPLETE!"
echo "======================================================================"
echo ""
echo "📍 Your application is now deploying to Railway"
echo ""
echo "Next steps:"
echo "1. Get your app URL: railway open"
echo "2. View logs:        railway logs"
echo "3. Check status:     railway status"
echo ""
echo "Database connection:"
echo "- Railway automatically sets DATABASE_URL for PostgreSQL"
echo "- Your app will use PostgreSQL in production"
echo ""
echo "To update your deployment, just run:"
echo "  railway up"
echo ""
echo "======================================================================"
