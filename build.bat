@echo off
echo P2P Privacy Communications - Build Installer
echo ============================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

REM Install build dependencies
echo Installing build dependencies...
python -m pip install pyinstaller
if errorlevel 1 (
    echo WARNING: Failed to install PyInstaller
    echo You may need to install it manually: pip install pyinstaller
)

echo.
echo Starting build process...
echo.

REM Run the build script
python build_installer.py

if errorlevel 1 (
    echo.
    echo Build failed! Please check the errors above.
    pause
    exit /b 1
)

echo.
echo Build completed successfully!
echo.
echo Generated files:
if exist "P2P_Privacy_Communications_Installer.exe" echo   - P2P_Privacy_Communications_Installer.exe (Windows Installer)
if exist "P2P_Privacy_Communications_Portable.zip" echo   - P2P_Privacy_Communications_Portable.zip (Portable Package)
if exist "P2P_Launcher.exe" echo   - P2P_Launcher.exe (Standalone Launcher)

echo.
echo You can now distribute these files to users!
pause

