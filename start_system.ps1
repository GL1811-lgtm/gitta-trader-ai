# Start Gitta Trader AI System

Write-Host "Starting Gitta Trader AI..." -ForegroundColor Green

# Start Backend
Write-Host "Starting Backend (Flask)..." -ForegroundColor Cyan
Start-Process -FilePath "python" -ArgumentList "backend/api/app.py" -NoNewWindow
# Note: In a real deployment, you might want to run this in a separate window or background job
# For dev, we'll just let it run. If you want separate window:
# Start-Process -FilePath "python" -ArgumentList "backend/api/app.py"

# Start Frontend
Write-Host "Starting Frontend (Vite)..." -ForegroundColor Cyan
Start-Process -FilePath "npm" -ArgumentList "run dev" -NoNewWindow

Write-Host "System started! Access the dashboard at http://localhost:5173" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop."
