#!/usr/bin/env python3
"""
P2P Privacy Communications Launcher
Simple launcher script that handles dependencies and starts the main application
"""

import sys
import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import importlib.util

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        messagebox.showerror(
            "Python Version Error",
            f"Python 3.7 or higher is required.\nYou have Python {sys.version_info.major}.{sys.version_info.minor}"
        )
        return False
    return True

def check_dependencies():
    """Check and install missing dependencies"""
    required_packages = {
        'cryptography': 'cryptography>=41.0.0',
        'tkinter': None,  # Usually built-in
    }
    
    optional_packages = {
        'pyaudio': 'pyaudio>=0.2.11'
    }
    
    missing_required = []
    missing_optional = []
    
    # Check required packages
    for package, pip_name in required_packages.items():
        if package == 'tkinter':
            try:
                import tkinter
            except ImportError:
                missing_required.append('tkinter (please install python3-tk)')
        else:
            if importlib.util.find_spec(package) is None:
                missing_required.append(pip_name or package)
    
    # Check optional packages
    for package, pip_name in optional_packages.items():
        if importlib.util.find_spec(package) is None:
            missing_optional.append(pip_name or package)
    
    if missing_required:
        response = messagebox.askyesno(
            "Missing Dependencies",
            f"Required packages are missing:\n\n{', '.join(missing_required)}\n\n" +
            "Do you want to install them automatically?"
        )
        
        if response:
            try:
                for package in missing_required:
                    if 'tkinter' in package:
                        messagebox.showinfo(
                            "Manual Installation Required",
                            "Please install tkinter manually:\n\n" +
                            "Ubuntu/Debian: sudo apt-get install python3-tk\n" +
                            "CentOS/RHEL: sudo yum install tkinter\n" +
                            "Windows: Reinstall Python with tkinter option checked"
                        )
                        continue
                    
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                
                messagebox.showinfo("Success", "Dependencies installed successfully!")
                
            except subprocess.CalledProcessError as e:
                messagebox.showerror(
                    "Installation Failed",
                    f"Failed to install dependencies:\n{e}\n\n" +
                    "Please install manually using:\npip install -r requirements.txt"
                )
                return False
        else:
            return False
    
    # Handle optional packages
    if missing_optional:
        response = messagebox.askyesno(
            "Optional Dependencies",
            f"Optional packages are missing (required for voice calls):\n\n{', '.join(missing_optional)}\n\n" +
            "Do you want to install them? (You can skip this and install later)"
        )
        
        if response:
            try:
                for package in missing_optional:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                messagebox.showinfo("Success", "Optional dependencies installed successfully!")
            except subprocess.CalledProcessError:
                messagebox.showwarning(
                    "Optional Installation Failed",
                    "Failed to install optional dependencies.\n" +
                    "Voice calling may not work.\n\n" +
                    "You can install pyaudio manually later if needed."
                )
    
    return True

def get_script_directory():
    """Get the directory where this script is located"""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        return os.path.dirname(sys.executable)
    else:
        # Running as script
        return os.path.dirname(os.path.abspath(__file__))

def main():
    """Main launcher function"""
    # Hide the root window initially
    root = tk.Tk()
    root.withdraw()
    
    try:
        # Check Python version
        if not check_python_version():
            return 1
        
        # Check and install dependencies
        if not check_dependencies():
            return 1
        
        # Get the script directory
        script_dir = get_script_directory()
        main_script = os.path.join(script_dir, 'main.py')
        
        # Check if main.py exists
        if not os.path.exists(main_script):
            messagebox.showerror(
                "File Not Found",
                f"Could not find main.py in {script_dir}\n\n" +
                "Please ensure the application is properly installed."
            )
            return 1
        
        # Close the hidden root window
        root.destroy()
        
        # Launch the main application
        try:
            # Change to the script directory
            original_cwd = os.getcwd()
            os.chdir(script_dir)
            
            # Import and run the main application
            sys.path.insert(0, script_dir)
            
            # Try importing the main module
            spec = importlib.util.spec_from_file_location("main", main_script)
            main_module = importlib.util.module_from_spec(spec)
            
            # Execute the main module
            spec.loader.exec_module(main_module)
            
        except Exception as e:
            # Restore original working directory
            os.chdir(original_cwd)
            
            messagebox.showerror(
                "Launch Error",
                f"Failed to start the application:\n\n{str(e)}\n\n" +
                "Please check the installation and try again."
            )
            return 1
        
        return 0
        
    except Exception as e:
        messagebox.showerror(
            "Unexpected Error",
            f"An unexpected error occurred:\n\n{str(e)}"
        )
        return 1
    
    finally:
        # Ensure root window is destroyed
        try:
            root.destroy()
        except:
            pass

if __name__ == "__main__":
    sys.exit(main())

