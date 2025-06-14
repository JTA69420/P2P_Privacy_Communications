# P2P Privacy Communications - PowerShell Startup Script

Write-Host "P2P Privacy Communications - Starting..." -ForegroundColor Green
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }
    Write-Host "Found: $pythonVersion" -ForegroundColor Cyan
} catch {
    Write-Host "Python is not installed or not in PATH!" -ForegroundColor Red
    Write-Host "Please install Python 3.7 or higher from https://python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Change to script directory
Set-Location $PSScriptRoot

# Check if dependencies are installed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
try {
    python -c "import cryptography" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Installing dependencies..." -ForegroundColor Yellow
        python -m pip install -r requirements.txt
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to install dependencies"
        }
    } else {
        Write-Host "Dependencies already installed." -ForegroundColor Green
    }
} catch {
    Write-Host "Failed to install dependencies!" -ForegroundColor Red
    Write-Host "Please run: pip install -r requirements.txt" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Run the application
Write-Host "Starting P2P Communications..." -ForegroundColor Green
Write-Host ""

try {
    python main.py
} catch {
    Write-Host "Application encountered an error!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
}

