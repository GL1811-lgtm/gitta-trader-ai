# Automated ngrok Setup Script for Angel One API
# Run this script to automatically download and start ngrok

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Automated ngrok Setup for Angel One API" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Create ngrok directory
$ngrokDir = "C:\ngrok"
Write-Host "1. Creating ngrok directory..." -ForegroundColor Yellow
if (-not (Test-Path $ngrokDir)) {
    New-Item -Path $ngrokDir -ItemType Directory | Out-Null
    Write-Host "   ✓ Directory created: $ngrokDir" -ForegroundColor Green
}
else {
    Write-Host "   ✓ Directory already exists: $ngrokDir" -ForegroundColor Green
}

# Step 2: Download ngrok
Write-Host ""
Write-Host "2. Downloading ngrok for Windows..." -ForegroundColor Yellow
$ngrokZip = "$ngrokDir\ngrok.zip"
$ngrokUrl = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"

try {
    Invoke-WebRequest -Uri $ngrokUrl -OutFile $ngrokZip -UseBasicParsing
    Write-Host "   ✓ Download complete!" -ForegroundColor Green
}
catch {
    Write-Host "   ✗ Download failed: $_" -ForegroundColor Red
    exit 1
}

# Step 3: Extract ngrok
Write-Host ""
Write-Host "3. Extracting ngrok..." -ForegroundColor Yellow
try {
    Expand-Archive -Path $ngrokZip -DestinationPath $ngrokDir -Force
    Remove-Item $ngrokZip
    Write-Host "   ✓ Extracted successfully!" -ForegroundColor Green
}
catch {
    Write-Host "   ✗ Extraction failed: $_" -ForegroundColor Red
    exit 1
}

# Step 4: Add to PATH
Write-Host ""
Write-Host "4. Adding ngrok to system PATH..." -ForegroundColor Yellow
$currentPath = [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::User)
if ($currentPath -notlike "*$ngrokDir*") {
    [Environment]::SetEnvironmentVariable("Path", "$currentPath;$ngrokDir", [EnvironmentVariableTarget]::User)
    $env:Path = "$env:Path;$ngrokDir"
    Write-Host "   ✓ Added to PATH!" -ForegroundColor Green
}
else {
    Write-Host "   ✓ Already in PATH!" -ForegroundColor Green
}

# Step 5: Verify installation
Write-Host ""
Write-Host "5. Verifying installation..." -ForegroundColor Yellow
$ngrokExe = "$ngrokDir\ngrok.exe"
if (Test-Path $ngrokExe) {
    Write-Host "   ✓ ngrok installed successfully!" -ForegroundColor Green
}
else {
    Write-Host "   ✗ ngrok.exe not found!" -ForegroundColor Red
    exit 1
}

# Step 6: Start ngrok tunnel
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  STARTING NGROK TUNNEL" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting tunnel to port 5001..." -ForegroundColor Yellow
Write-Host ""
Write-Host "IMPORTANT: Copy the HTTPS URL that appears below!" -ForegroundColor Magenta
Write-Host "Use it as your Angel One Redirect URL" -ForegroundColor Magenta
Write-Host ""
Write-Host "Example: https://abc123.ngrok-free.app/api/angelone/callback" -ForegroundColor Magenta
Write-Host ""
Write-Host "Press Ctrl+C to stop ngrok" -ForegroundColor Gray
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Start ngrok
& "$ngrokDir\ngrok.exe" http 5001
