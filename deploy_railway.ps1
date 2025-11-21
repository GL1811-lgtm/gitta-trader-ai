# Railway Deployment Script for Windows (PowerShell)
# This script automates the deployment to Railway.app

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "         GITTA TRADER AI - RAILWAY DEPLOYMENT" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Railway CLI is installed
$railwayInstalled = Get-Command railway -ErrorAction SilentlyContinue

if (-not $railwayInstalled) {
    Write-Host "📦 Railway CLI not found. Installing..." -ForegroundColor Yellow
    Write-Host ""
    
    # Install using npm (most common on Windows)
    if (Get-Command npm -ErrorAction SilentlyContinue) {
        npm install -g @railway/cli
        Write-Host "✅ Railway CLI installed" -ForegroundColor Green
    } else {
        Write-Host "❌ npm not found. Please install Node.js first:" -ForegroundColor Red
        Write-Host "   Visit: https://nodejs.org/" -ForegroundColor Red
        Write-Host ""
        Write-Host "Or install Railway CLI manually:" -ForegroundColor Yellow
        Write-Host "   Visit: https://docs.railway.app/develop/cli#installation" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host "🔐 Logging in to Railway..." -ForegroundColor Cyan
railway login

Write-Host ""
Write-Host "📋 Creating new Railway project..." -ForegroundColor Cyan
Write-Host "   Project name: gitta-trader-ai" -ForegroundColor Gray
Write-Host ""

# Initialize Railway project
railway init

Write-Host ""
Write-Host "🐘 Adding PostgreSQL database..." -ForegroundColor Cyan
railway add --plugin postgresql

Write-Host ""
Write-Host "⚙️  Setting up environment variables..." -ForegroundColor Cyan
Write-Host ""

# Check if .env file exists
if (-not (Test-Path .env)) {
    Write-Host "⚠️  .env file not found. Please create one from .env.example" -ForegroundColor Yellow
    exit 1
}

# Read important variables from .env and set them in Railway
Get-Content .env | ForEach-Object {
    $line = $_.Trim()
    
    # Skip comments and empty lines
    if ($line -match "^#" -or $line -eq "") {
        return
    }
    
    # Parse key=value
    if ($line -match "^([^=]+)=(.*)$") {
        $key = $matches[1].Trim()
        $value = $matches[2].Trim().Trim('"')
        
        # Skip DATABASE_URL (Railway sets this automatically)
        if ($key -eq "DATABASE_URL") {
            return
        }
        
        # Set in Railway if value is not placeholder
        if ($value -and $value -notmatch "^your_") {
            Write-Host "Setting $key..." -ForegroundColor Gray
            railway variables --set "$key=$value"
        }
    }
}

# Set production environment
Write-Host "Setting ENVIRONMENT=production..." -ForegroundColor Gray
railway variables --set ENVIRONMENT=production

Write-Host ""
Write-Host "🚀 Deploying to Railway..." -ForegroundColor Cyan
railway up

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Green
Write-Host "✅ DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Your application is now deploying to Railway" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Get your app URL: railway open" -ForegroundColor White
Write-Host "2. View logs:        railway logs" -ForegroundColor White
Write-Host "3. Check status:     railway status" -ForegroundColor White
Write-Host ""
Write-Host "Database connection:" -ForegroundColor Yellow
Write-Host "- Railway automatically sets DATABASE_URL for PostgreSQL" -ForegroundColor White
Write-Host "- Your app will use PostgreSQL in production" -ForegroundColor White
Write-Host ""
Write-Host "To update your deployment, just run:" -ForegroundColor Yellow
Write-Host "  railway up" -ForegroundColor White
Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
