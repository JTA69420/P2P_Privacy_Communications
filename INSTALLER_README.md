# P2P Privacy Communications - Installer Package

This directory contains everything needed to build and distribute the P2P Privacy Communications application with a professional Windows installer.

## 📁 Files Overview

### Core Application
- **`main.py`** - Main P2P communications application
- **`launcher.py`** - Smart launcher that handles dependencies
- **`requirements.txt`** - Python dependencies
- **`LICENSE.txt`** - Software license

### Build System
- **`installer.nsi`** - NSIS installer script
- **`build_installer.py`** - Automated build script
- **`build.bat`** - Windows batch file to run build
- **`launcher.spec`** - PyInstaller specification

### User Scripts
- **`run.bat`** - Simple Windows launcher
- **`run.ps1`** - PowerShell launcher with better error handling

## 🚀 Quick Start - Building the Installer

### Method 1: Automatic Build (Recommended)

1. **Double-click `build.bat`** or run in Command Prompt:
   ```cmd
   build.bat
   ```

2. **Follow the prompts** - the script will:
   - Check for Python
   - Install PyInstaller automatically
   - Build the launcher executable
   - Create the installer (if NSIS is available)
   - Create a portable ZIP package

### Method 2: Manual Build

1. **Install build tools:**
   ```cmd
   pip install pyinstaller
   ```
   
   Download and install NSIS from: https://nsis.sourceforge.io/

2. **Run the build script:**
   ```cmd
   python build_installer.py
   ```

## 📦 Output Files

After building, you'll get:

### For End Users
- **`P2P_Privacy_Communications_Installer.exe`** - Full Windows installer with uninstaller
- **`P2P_Privacy_Communications_Portable.zip`** - Portable package (no installation required)
- **`P2P_Launcher.exe`** - Standalone launcher executable

### What the Installer Includes
- ✅ Automatic Python dependency checking
- ✅ Smart dependency installation
- ✅ Desktop and Start Menu shortcuts
- ✅ Professional uninstaller
- ✅ Windows registry integration
- ✅ Component selection (core app, dependencies, shortcuts)

## 🎯 Distribution

### For Easy Installation
Share **`P2P_Privacy_Communications_Installer.exe`** - recipients can:
1. Double-click to run
2. Follow the installation wizard
3. Choose installation options
4. Launch from Desktop/Start Menu

### For Portable Use
Share **`P2P_Privacy_Communications_Portable.zip`** - recipients can:
1. Extract anywhere
2. Run `P2P_Launcher.exe` or `run.bat`
3. No installation required

## ⚙️ Installer Features

### Installation Options
- **Core Application** (required) - Main program files
- **Python Dependencies** (optional) - Auto-install cryptography, pyaudio
- **Desktop Shortcut** (optional) - Quick access from desktop
- **Start Menu Shortcuts** (optional) - Program group with shortcuts

### Smart Dependency Handling
- Checks for Python 3.7+ installation
- Offers to install missing packages
- Graceful handling of optional components (like audio)
- Clear error messages with solutions

### Uninstaller
- Complete removal of all installed files
- Registry cleanup
- Shortcut removal
- Accessible from Windows "Add or Remove Programs"

## 🛠️ Build Requirements

### For Building Installer
- **Python 3.7+** with pip
- **PyInstaller** (`pip install pyinstaller`)
- **NSIS** (https://nsis.sourceforge.io/) - for Windows installer

### For End Users
- **Python 3.7+** (automatically checked by installer)
- **Windows 7/10/11** (installer supports all versions)

## 🔧 Customization

### Modifying the Installer
Edit `installer.nsi` to:
- Change installation directory
- Add/remove components
- Modify installer appearance
- Add custom actions

### Customizing the Launcher
Edit `launcher.py` to:
- Change dependency checking logic
- Modify error messages
- Add pre-launch checks
- Customize startup behavior

## 🐛 Troubleshooting

### Build Issues

**"PyInstaller not found"**
```cmd
pip install pyinstaller
```

**"NSIS not found"**
- Download from https://nsis.sourceforge.io/
- Install to default location
- Or add to PATH

**"Python not found"**
- Install Python from https://python.org
- Ensure "Add to PATH" is checked during installation

### Runtime Issues

**"Failed to start application"**
- Check Python installation
- Verify all files are present
- Run from command line for detailed errors

**"Audio not working"**
- Install PyAudio: `pip install pyaudio`
- On Windows: `pip install pipwin && pipwin install pyaudio`

## 📋 File Structure After Installation

```
C:\Program Files\P2P Privacy Communications\
├── main.py                 # Main application
├── launcher.py             # Launcher script
├── P2P_Launcher.exe        # Compiled launcher
├── requirements.txt        # Dependencies
├── README.md              # Documentation
├── LICENSE.txt            # License
├── run.bat               # Batch launcher
├── run.ps1               # PowerShell launcher
└── Uninstall.exe         # Uninstaller
```

## 🎨 Advanced Features

### Silent Installation
```cmd
P2P_Privacy_Communications_Installer.exe /S
```

### Custom Install Directory
```cmd
P2P_Privacy_Communications_Installer.exe /D=C:\MyApps\P2P
```

### Component Selection
Users can choose:
- Which components to install
- Whether to install Python dependencies
- Shortcut creation preferences

## 📞 Support

For installer issues:
1. Check build requirements are met
2. Review error messages in build output
3. Ensure all source files are present
4. Try building components individually

For application issues:
1. Check the main README.md
2. Verify Python and dependencies
3. Test with portable version first

---

**Ready to build?** Just run `build.bat` and you'll have a professional installer ready for distribution! 🚀

