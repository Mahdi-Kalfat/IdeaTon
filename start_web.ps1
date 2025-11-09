# Light Detection Web Application Starter Script

Write-Host "=================================" -ForegroundColor Cyan
Write-Host "Light Detection Web Application" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Check if model exists
if (-not (Test-Path "light_detection_model.h5")) {
    Write-Host "ERROR: Model file not found!" -ForegroundColor Red
    Write-Host "Please train the model first: python train_model.py" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

Write-Host "✓ Model file found" -ForegroundColor Green

# Check if MongoDB is running (optional check)
Write-Host ""
Write-Host "Checking MongoDB connection..." -ForegroundColor Yellow
$mongoRunning = Get-Service -Name "MongoDB" -ErrorAction SilentlyContinue
if ($mongoRunning -and $mongoRunning.Status -eq "Running") {
    Write-Host "✓ MongoDB service is running" -ForegroundColor Green
} else {
    Write-Host "⚠ MongoDB service not detected" -ForegroundColor Yellow
    Write-Host "  The app will start but history won't be saved" -ForegroundColor Yellow
    Write-Host "  Install MongoDB: https://www.mongodb.com/try/download/community" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Starting web application..." -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

# Start the Flask application
python app.py
