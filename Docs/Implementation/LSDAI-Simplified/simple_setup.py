#!/usr/bin/env python3
"""
LSDAI-Simplified Simple Setup Script
Minimal installation script for basic setup needs.
"""

import os
import sys
import subprocess
import json
import platform
from pathlib import Path

def print_status(message):
    print(f"[INFO] {message}")

def print_success(message):
    print(f"[SUCCESS] {message}")

def print_error(message):
    print(f"[ERROR] {message}")

def run_command(command, timeout=60):
    """Run a command and return success status"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)

def check_python_version():
    """Check if Python version is compatible"""
    version = platform.python_version()
    major, minor = map(int, version.split('.')[:2])
    
    if major < 3 or (major == 3 and minor < 8):
        print_error(f"Python {major}.{minor} not supported. Need 3.8+")
        return False
    
    print_success(f"Python {major}.{minor} is compatible")
    return True

def create_venv():
    """Create virtual environment"""
    print_status("Creating virtual environment...")
    
    if Path("venv").exists():
        print_success("Virtual environment already exists")
        return True
    
    success, stdout, stderr = run_command("python3 -m venv venv")
    if success:
        print_success("Virtual environment created")
        return True
    else:
        print_error(f"Failed to create virtual environment: {stderr}")
        return False

def install_basic_packages():
    """Install basic Python packages"""
    print_status("Installing basic packages...")
    
    # Get python executable path
    if platform.system() == "Windows":
        python_exe = "venv\\Scripts\\python.exe"
        pip_exe = "venv\\Scripts\\pip.exe"
    else:
        python_exe = "venv/bin/python"
        pip_exe = "venv/bin/pip"
    
    # Upgrade pip
    success, stdout, stderr = run_command(f"{pip_exe} install --upgrade pip")
    if not success:
        print_warning(f"pip upgrade failed: {stderr}")
    
    # Install basic packages
    packages = ["requests", "tqdm", "jupyterlab", "notebook", "ipywidgets"]
    
    for package in packages:
        print_status(f"Installing {package}...")
        success, stdout, stderr = run_command(f"{pip_exe} install {package}")
        if success:
            print_success(f"Installed {package}")
        else:
            print_error(f"Failed to install {package}: {stderr}")
            return False
    
    return True

def create_basic_structure():
    """Create basic project structure"""
    print_status("Creating project structure...")
    
    directories = [
        "scripts",
        "modules", 
        "data",
        "shared_models/Stable-diffusion",
        "shared_models/VAE",
        "shared_models/Lora",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print_success(f"Created {directory}")
    
    return True

def create_basic_config():
    """Create basic configuration file"""
    print_status("Creating configuration file...")
    
    config = {
        "environment": {
            "platform": platform.system(),
            "base_path": str(Path.cwd()),
            "console_mode": False
        },
        "webui": {
            "selected": "forge",
            "launch_args": "--xformers --cuda-stream"
        },
        "models": {
            "selected_sd15": [],
            "selected_sdxl": [],
            "text_input": ""
        },
        "verbosity": "normal"
    }
    
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print_success("Configuration file created")
    return True

def create_requirements():
    """Create requirements.txt file"""
    print_status("Creating requirements.txt...")
    
    requirements = """requests>=2.25.0
tqdm>=4.60.0
jupyterlab>=3.0.0
notebook>=6.0.0
ipywidgets>=7.0.0
gitpython>=3.0.0
"""
    
    with open("requirements.txt", "w") as f:
        f.write(requirements)
    
    print_success("Requirements file created")
    return True

def show_completion():
    """Show completion message"""
    print()
    print("🎉 LSDAI-Simplified Simple Setup Complete!")
    print("=" * 45)
    print()
    print("Quick start:")
    if platform.system() == "Windows":
        print("1. Activate: venv\\Scripts\\activate")
    else:
        print("1. Activate: source venv/bin/activate")
    print("2. Start: jupyter lab")
    print("3. Open: LSDAI-Simplified.ipynb")
    print()
    print("Files created:")
    print("- venv/ - Virtual environment")
    print("- config.json - Configuration")
    print("- requirements.txt - Dependencies")
    print("- scripts/, modules/, data/ - Project structure")
    print()

def main():
    """Main installation function"""
    print("🚀 LSDAI-Simplified Simple Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create virtual environment
    if not create_venv():
        return False
    
    # Install basic packages
    if not install_basic_packages():
        return False
    
    # Create project structure
    if not create_basic_structure():
        return False
    
    # Create configuration
    if not create_basic_config():
        return False
    
    # Create requirements file
    if not create_requirements():
        return False
    
    # Show completion message
    show_completion()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("✅ Setup completed successfully!")
            sys.exit(0)
        else:
            print("❌ Setup failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        sys.exit(1)