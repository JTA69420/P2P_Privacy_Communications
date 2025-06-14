#!/usr/bin/env python3
"""
Build script for P2P Privacy Communications
Creates launcher executable and installer package
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_tools():
    """Check if required build tools are available"""
    tools = {
        'pyinstaller': 'pip install pyinstaller',
        'makensis': 'Install NSIS from https://nsis.sourceforge.io/'
    }
    
    missing = []
    
    # Check PyInstaller
    try:
        subprocess.run(['pyinstaller', '--version'], 
                      capture_output=True, check=True)
        print("✓ PyInstaller found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        missing.append(('PyInstaller', tools['pyinstaller']))
    
    # Check NSIS
    nsis_paths = [
        r'C:\Program Files (x86)\NSIS\makensis.exe',
        r'C:\Program Files\NSIS\makensis.exe',
        'makensis.exe'  # In PATH
    ]
    
    nsis_found = False
    for path in nsis_paths:
        try:
            subprocess.run([path, '/VERSION'], 
                          capture_output=True, check=True)
            print(f"✓ NSIS found at {path}")
            nsis_found = True
            break
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    if not nsis_found:
        missing.append(('NSIS', tools['makensis']))
    
    if missing:
        print("\n❌ Missing required tools:")
        for tool, install_cmd in missing:
            print(f"  {tool}: {install_cmd}")
        return False
    
    return True

def build_launcher():
    """Build the launcher executable using PyInstaller"""
    print("\n🔨 Building launcher executable...")
    
    try:
        # Clean previous builds
        if os.path.exists('build'):
            shutil.rmtree('build')
        if os.path.exists('dist'):
            shutil.rmtree('dist')
        
        # Build using PyInstaller
        cmd = [
            'pyinstaller',
            '--onefile',
            '--windowed',
            '--name=P2P_Launcher',
            '--distpath=.',
            'launcher.py'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Launcher executable built successfully")
            return True
        else:
            print(f"❌ PyInstaller failed:\n{result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error building launcher: {e}")
        return False

def build_installer():
    """Build the installer using NSIS"""
    print("\n📦 Building installer...")
    
    # Find NSIS makensis
    nsis_paths = [
        r'C:\Program Files (x86)\NSIS\makensis.exe',
        r'C:\Program Files\NSIS\makensis.exe',
        'makensis.exe'
    ]
    
    makensis = None
    for path in nsis_paths:
        if os.path.exists(path) or path == 'makensis.exe':
            makensis = path
            break
    
    if not makensis:
        print("❌ NSIS makensis not found")
        return False
    
    try:
        # Build installer
        result = subprocess.run(
            [makensis, 'installer.nsi'],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            print("✓ Installer built successfully")
            print(f"📁 Installer: P2P_Privacy_Communications_Installer.exe")
            return True
        else:
            print(f"❌ NSIS failed:\n{result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error building installer: {e}")
        return False

def create_portable_package():
    """Create a portable ZIP package"""
    print("\n📂 Creating portable package...")
    
    try:
        import zipfile
        
        files_to_include = [
            'main.py',
            'launcher.py',
            'requirements.txt',
            'README.md',
            'LICENSE.txt',
            'run.bat',
            'run.ps1'
        ]
        
        # Add launcher executable if it exists
        if os.path.exists('P2P_Launcher.exe'):
            files_to_include.append('P2P_Launcher.exe')
        
        with zipfile.ZipFile('P2P_Privacy_Communications_Portable.zip', 'w', 
                           zipfile.ZIP_DEFLATED) as zipf:
            for file in files_to_include:
                if os.path.exists(file):
                    zipf.write(file)
                    print(f"  Added: {file}")
                else:
                    print(f"  ⚠️  Missing: {file}")
        
        print("✓ Portable package created: P2P_Privacy_Communications_Portable.zip")
        return True
        
    except Exception as e:
        print(f"❌ Error creating portable package: {e}")
        return False

def cleanup():
    """Clean up build artifacts"""
    print("\n🧹 Cleaning up build artifacts...")
    
    cleanup_dirs = ['build', 'dist', '__pycache__']
    cleanup_files = ['*.pyc', '*.pyo']
    
    for dir_name in cleanup_dirs:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  Removed: {dir_name}/")
    
    # Clean up spec file artifacts
    for file in ['launcher.spec']:
        if os.path.exists(file):
            os.remove(file)
            print(f"  Removed: {file}")

def main():
    """Main build function"""
    print("🚀 P2P Privacy Communications - Build Script")
    print("=" * 50)
    
    # Check current directory
    required_files = ['main.py', 'launcher.py', 'installer.nsi']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        print("Please run this script from the project directory.")
        return 1
    
    # Check build tools
    if not check_tools():
        print("\n❌ Please install the missing tools and try again.")
        return 1
    
    # Build launcher executable
    if not build_launcher():
        print("\n❌ Failed to build launcher executable.")
        return 1
    
    # Build installer
    installer_success = build_installer()
    
    # Create portable package
    portable_success = create_portable_package()
    
    # Clean up
    cleanup()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Build Summary:")
    print(f"  Launcher executable: {'✓' if os.path.exists('P2P_Launcher.exe') else '❌'}")
    print(f"  Installer package: {'✓' if installer_success else '❌'}")
    print(f"  Portable package: {'✓' if portable_success else '❌'}")
    
    if installer_success or portable_success:
        print("\n🎉 Build completed successfully!")
        
        if installer_success:
            print("\n📦 To distribute the application:")
            print("  1. Share P2P_Privacy_Communications_Installer.exe for easy installation")
        
        if portable_success:
            print("  2. Share P2P_Privacy_Communications_Portable.zip for portable use")
        
        print("\n⚠️  Note: Recipients will need Python 3.7+ installed to run the application.")
        return 0
    else:
        print("\n❌ Build failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

