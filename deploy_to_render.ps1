# Automated Render Deployment Script
# This script will prepare and push your code to GitHub for Render deployment

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "     GITTA TRADER AI - RENDER DEPLOYMENT SETUP" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Git is not installed!" -ForegroundColor Red
    Write-Host "   Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "   Then run this script again." -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "✅ Git is installed" -ForegroundColor Green
Write-Host ""

# Check if already a git repo
if (-not (Test-Path .git)) {
    Write-Host "📦 Initializing Git repository..." -ForegroundColor Cyan
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
}
else {
    Write-Host "✅ Git repository already exists" -ForegroundColor Green
}
Write-Host ""

# Configure git if needed
$gitUserName = git config user.name
if (-not $gitUserName) {
    Write-Host "⚙️  Git user not configured. Let's set it up:" -ForegroundColor Yellow
    $userName = Read-Host "Enter your name"
    $userEmail = Read-Host "Enter your email"
    git config user.name "$userName"
    git config user.email "$userEmail"
    Write-Host "✅ Git user configured" -ForegroundColor Green
    Write-Host ""
}

# Create .gitignore if it doesn't exist
if (-not (Test-Path .gitignore)) {
    Write-Host "📝 Creating .gitignore..." -ForegroundColor Cyan
    @"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment variables
.env
.env.local
.env.production

# Database
*.db
*.sqlite
*.sqlite3

# Logs
logs/
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Node
node_modules/
npm-debug.log*

# Credentials (NEVER commit these!)
credentials.json

# Ngrok
ngrok.exe
tunnel_url.txt
"@ | Out-File -FilePath .gitignore -Encoding UTF8
    Write-Host "✅ .gitignore created" -ForegroundColor Green
}
else {
    Write-Host "✅ .gitignore already exists" -ForegroundColor Green
}
Write-Host ""

# Add all files
Write-Host "📦 Staging files for commit..." -ForegroundColor Cyan
git add .

# Commit
Write-Host "💾 Creating commit..." -ForegroundColor Cyan
$commitMessage = "Prepare for Render deployment with Google Drive integration"
git commit -m "$commitMessage"
Write-Host "✅ Files committed" -ForegroundColor Green
Write-Host ""

# Check if remote exists
$remotes = git remote
if ($remotes -contains "origin") {
    Write-Host "✅ GitHub remote already configured" -ForegroundColor Green
    Write-Host ""
    Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Cyan
    git push origin main
    Write-Host "✅ Code pushed to GitHub!" -ForegroundColor Green
}
else {
    Write-Host "⚠️  No GitHub remote found" -ForegroundColor Yellow
    Write-Host "   You need to create a GitHub repository first." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📋 Quick steps:" -ForegroundColor Cyan
    Write-Host "   1. Go to: https://github.com/new" -ForegroundColor White
    Write-Host "   2. Repository name: gitta-trader-ai" -ForegroundColor White
    Write-Host "   3. Make it Private (recommended)" -ForegroundColor White
    Write-Host "   4. Click 'Create repository'" -ForegroundColor White
    Write-Host ""
    
    $createNow = Read-Host "Have you created the repository? (y/n)"
    
    if ($createNow -eq "y") {
        $githubUsername = Read-Host "Enter your GitHub username"
        $repoUrl = "https://github.com/$githubUsername/gitta-trader-ai.git"
        
        Write-Host ""
        Write-Host "🔗 Adding remote: $repoUrl" -ForegroundColor Cyan
        git remote add origin $repoUrl
        
        # Rename branch to main if needed
        $currentBranch = git branch --show-current
        if ($currentBranch -ne "main") {
            Write-Host "📝 Renaming branch to 'main'..." -ForegroundColor Cyan
            git branch -M main
        }
        
        Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Cyan
        git push -u origin main
        
        Write-Host ""
        Write-Host "✅ Code pushed to GitHub!" -ForegroundColor Green
    }
    else {
        Write-Host ""
        Write-Host "⏸️  Deployment paused." -ForegroundColor Yellow
        Write-Host "   Run this script again after creating the repository." -ForegroundColor Yellow
        pause
        exit 0
    }
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Green
Write-Host "✅ GITHUB SETUP COMPLETE!" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next Steps for Render Deployment:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Go to: https://render.com" -ForegroundColor White
Write-Host "2. Click 'New +' → 'Web Service'" -ForegroundColor White
Write-Host "3. Connect your GitHub repository: gitta-trader-ai" -ForegroundColor White
Write-Host "4. Render will auto-detect the configuration!" -ForegroundColor White
Write-Host ""
Write-Host "5. Add these environment variables:" -ForegroundColor Yellow
Write-Host "   - GEMINI_API_KEY" -ForegroundColor White
Write-Host "   - GROQ_API_KEY" -ForegroundColor White
Write-Host "   - YOUTUBE_API_KEY" -ForegroundColor White
Write-Host "   - GOOGLE_DRIVE_FOLDER_ID" -ForegroundColor White
Write-Host "   - GOOGLE_DRIVE_ENABLED=true" -ForegroundColor White
Write-Host "   - BACKUP_ENABLED=true" -ForegroundColor White
Write-Host "   - All other keys from your .env file" -ForegroundColor White
Write-Host ""
Write-Host "6. Click 'Create Web Service'" -ForegroundColor White
Write-Host "7. Wait 3-5 minutes for deployment" -ForegroundColor White
Write-Host "8. Get your live URL!" -ForegroundColor White
Write-Host ""
Write-Host "💡 Tip: See RENDER_DEPLOYMENT.md for detailed instructions" -ForegroundColor Cyan
Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan

pause
