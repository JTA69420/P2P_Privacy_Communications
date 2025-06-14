@echo off
echo P2P Privacy Communications - Starting...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH!
    echo Please install Python 3.7 or higher from https://python.org
    pause
    exit /b 1
)

REM Check if dependencies are installed
echo Checking dependencies...
python -c "import cryptography" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Failed to install dependencies!
        echo Please run: pip install -r requirements.txt
        pause
        exit /b 1
    )
)

REM Run the application
echo Starting P2P Communications...
echo.
python main.py

if errorlevel 1 (
    echo Application encountered an error!
    pause
)

