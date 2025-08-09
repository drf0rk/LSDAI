#!/bin/bash

# LSDAI-Simplified Universal Installer
# Cross-platform installation script for Linux, macOS, and Windows (via WSL/WSL2)

set -e  # Exit on any error

# Global variables
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"
VENV_DIR="$PROJECT_DIR/venv"
LOGS_DIR="$PROJECT_DIR/logs"

# Colors for output
if command -v tput >/dev/null 2>&1; then
    RED=$(tput setaf 1)
    GREEN=$(tput setaf 2)
    YELLOW=$(tput setaf 3)
    BLUE=$(tput setaf 4)
    NC=$(tput sgr0)  # No Color
else
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    NC='\033[0m'
fi

# Logging function
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Create logs directory if it doesn't exist
    mkdir -p "$LOGS_DIR"
    
    # Log to file
    echo "[$timestamp] [$level] $message" >> "$LOGS_DIR/install.log"
    
    # Output to console with colors
    case "$level" in
        "INFO")  echo -e "${BLUE}[INFO]${NC} $message" ;;
        "SUCCESS") echo -e "${GREEN}[SUCCESS]${NC} $message" ;;
        "WARNING") echo -e "${YELLOW}[WARNING]${NC} $message" ;;
        "ERROR") echo -e "${RED}[ERROR]${NC} $message" ;;
    esac
}

# Function to detect platform
detect_platform() {
    local platform
    local os_type
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        platform="Linux"
        if [[ -f /etc/os-release ]]; then
            os_type=$(source /etc/os-release && echo "$ID")
        else
            os_type="unknown"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        platform="macOS"
        os_type="macos"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "win32" ]]; then
        platform="Windows"
        os_type="windows"
    else
        platform="Unknown"
        os_type="unknown"
    fi
    
    echo "$platform|$os_type"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install system dependencies
install_system_deps() {
    log "INFO" "Installing system dependencies..."
    
    local platform_info
    platform_info=$(detect_platform)
    local platform=$(echo "$platform_info" | cut -d'|' -f1)
    local os_type=$(echo "$platform_info" | cut -d'|' -f2)
    
    log "INFO" "Detected platform: $platform ($os_type)"
    
    case "$platform" in
        "Linux")
            if command_exists apt-get; then
                log "INFO" "Using apt-get package manager..."
                sudo apt-get update -qq
                sudo apt-get install -y -qq python3 python3-pip python3-venv git wget curl aria2 build-essential
            elif command_exists yum; then
                log "INFO" "Using yum package manager..."
                sudo yum install -y python3 python3-pip git wget curl aria2 gcc gcc-c++ make
            elif command_exists dnf; then
                log "INFO" "Using dnf package manager..."
                sudo dnf install -y python3 python3-pip git wget curl aria2 gcc gcc-c++ make
            elif command_exists zypper; then
                log "INFO" "Using zypper package manager..."
                sudo zypper install -y python3 python3-pip git wget curl aria2 gcc gcc-c++ make
            else
                log "WARNING" "No known package manager found. Please install dependencies manually."
                return 1
            fi
            ;;
        "macOS")
            if command_exists brew; then
                log "INFO" "Using Homebrew package manager..."
                brew update
                brew install python3 git wget curl aria2
            else
                log "WARNING" "Homebrew not found. Please install Homebrew or dependencies manually."
                log "INFO" "Visit https://brew.sh to install Homebrew."
                return 1
            fi
            ;;
        "Windows")
            log "INFO" "Windows platform detected. Assuming dependencies are available."
            log "INFO" "If using WSL/WSL2, this script will work as Linux."
            ;;
        *)
            log "WARNING" "Unsupported platform: $platform"
            log "INFO" "Please install dependencies manually:"
            log "INFO" "  - Python 3.8+"
            log "INFO" "  - Git"
            log "INFO" "  - wget/curl"
            log "INFO" "  - aria2c (optional but recommended)"
            ;;
    esac
    
    log "SUCCESS" "System dependencies installation completed"
    return 0
}

# Function to check Python version
check_python_version() {
    log "INFO" "Checking Python version..."
    
    if ! command_exists python3; then
        log "ERROR" "Python 3 is required but not found"
        return 1
    fi
    
    local version
    version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    
    local major minor
    major=$(echo "$version" | cut -d'.' -f1)
    minor=$(echo "$version" | cut -d'.' -f2)
    
    if [[ $major -lt 3 ]] || [[ $major -eq 3 && $minor -lt 8 ]]; then
        log "ERROR" "Python $major.$minor not supported. Need 3.8+"
        return 1
    fi
    
    log "SUCCESS" "Python $major.$minor is compatible"
    return 0
}

# Function to create virtual environment
create_venv() {
    log "INFO" "Creating Python virtual environment..."
    
    if [[ -d "$VENV_DIR" ]]; then
        log "WARNING" "Virtual environment already exists. Removing and recreating..."
        rm -rf "$VENV_DIR"
    fi
    
    # Create virtual environment
    if ! python3 -m venv "$VENV_DIR"; then
        log "ERROR" "Failed to create virtual environment"
        return 1
    fi
    
    log "SUCCESS" "Virtual environment created"
    
    # Determine paths for the virtual environment
    if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "win32" ]]; then
        PYTHON_EXE="$VENV_DIR/Scripts/python.exe"
        PIP_EXE="$VENV_DIR/Scripts/pip.exe"
    else
        PYTHON_EXE="$VENV_DIR/bin/python"
        PIP_EXE="$VENV_DIR/bin/pip"
    fi
    
    # Upgrade pip
    log "INFO" "Upgrading pip..."
    if "$PYTHON_EXE" -m pip install --upgrade pip setuptools wheel; then
        log "SUCCESS" "pip upgraded successfully"
    else
        log "WARNING" "pip upgrade failed, continuing anyway"
    fi
    
    return 0
}

# Function to install Python packages
install_python_packages() {
    log "INFO" "Installing Python packages..."
    
    # Determine paths
    if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "win32" ]]; then
        PYTHON_EXE="$VENV_DIR/Scripts/python.exe"
        PIP_EXE="$VENV_DIR/Scripts/pip.exe"
    else
        PYTHON_EXE="$VENV_DIR/bin/python"
        PIP_EXE="$VENV_DIR/bin/pip"
    fi
    
    # Check if requirements.txt exists
    if [[ -f "$PROJECT_DIR/requirements.txt" ]]; then
        log "INFO" "Installing from requirements.txt..."
        if "$PIP_EXE" install -r "$PROJECT_DIR/requirements.txt"; then
            log "SUCCESS" "Python packages installed from requirements.txt"
        else
            log "WARNING" "Failed to install from requirements.txt, installing basic packages"
            install_basic_packages "$PYTHON_EXE" "$PIP_EXE"
        fi
    else
        log "INFO" "requirements.txt not found, installing basic packages"
        install_basic_packages "$PYTHON_EXE" "$PIP_EXE"
    fi
    
    return 0
}

# Function to install basic packages
install_basic_packages() {
    local python_exe="$1"
    local pip_exe="$2"
    
    local packages=(
        "requests>=2.25.0"
        "tqdm>=4.60.0"
        "jupyterlab>=3.0.0"
        "notebook>=6.0.0"
        "ipywidgets>=7.0.0"
        "gitpython>=3.0.0"
        "jupyter-server"
        "papermill"
        "nbformat"
    )
    
    for package in "${packages[@]}"; do
        log "INFO" "Installing $package..."
        if "$pip_exe" install "$package"; then
            log "SUCCESS" "Installed $package"
        else
            log "ERROR" "Failed to install $package"
            return 1
        fi
    done
    
    return 0
}

# Function to create project structure
create_project_structure() {
    log "INFO" "Creating project structure..."
    
    local directories=(
        "scripts"
        "modules"
        "data"
        "shared_models/Stable-diffusion"
        "shared_models/VAE"
        "shared_models/Lora"
        "shared_models/ControlNet"
        "shared_models/embeddings"
        "webui_installations"
        "downloads"
        "configs"
        "logs"
    )
    
    for directory in "${directories[@]}"; do
        local dir_path="$PROJECT_DIR/$directory"
        if ! mkdir -p "$dir_path"; then
            log "ERROR" "Failed to create directory: $directory"
            return 1
        fi
        log "SUCCESS" "Created directory: $directory"
    done
    
    return 0
}

# Function to setup Jupyter configuration
setup_jupyter_config() {
    log "INFO" "Setting up Jupyter configuration..."
    
    # Determine paths
    if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "win32" ]]; then
        PYTHON_EXE="$VENV_DIR/Scripts/python.exe"
        JUPYTER_CMD="$PYTHON_EXE -m jupyter"
    else
        PYTHON_EXE="$VENV_DIR/bin/python"
        JUPYTER_CMD="$PYTHON_EXE -m jupyter"
    fi
    
    # Create Jupyter config directory
    local jupyter_config_dir="$HOME/.jupyter"
    mkdir -p "$jupyter_config_dir"
    
    # Create Jupyter configuration
    local config_content
    config_content='# LSDAI-Simplified Jupyter Configuration
c = get_config()

# Server configuration
c.NotebookApp.ip = "127.0.0.1"
c.NotebookApp.port = 8888
c.NotebookApp.open_browser = False
c.NotebookApp.token = ""
c.NotebookApp.password = ""
c.NotebookApp.allow_root = True

# Extensions
c.NotebookApp.nbserver_extensions = {
    "jupyterlab": True,
    "notebook": True,
}

# Security settings for local development
c.NotebookApp.allow_origin = "*"
c.NotebookApp.disable_check_xsrf = True

# Auto-reload
c.InteractiveShellApp.extensions = ["autoreload"]
c.InteractiveShellApp.exec_lines = ["%autoreload 2"]
'
    
    local config_file="$jupyter_config_dir/jupyter_notebook_config.py"
    echo "$config_content" > "$config_file"
    
    log "SUCCESS" "Jupyter configuration created"
    
    # Install JupyterLab extensions (optional)
    log "INFO" "Installing JupyterLab extensions..."
    local extensions=("@jupyter-widgets/jupyterlab-manager" "@jupyter-server/resource-usage")
    
    for extension in "${extensions[@]}"; do
        if $JUPYTER_CMD labextension install "$extension" >/dev/null 2>&1; then
            log "SUCCESS" "Installed extension: $extension"
        else
            log "WARNING" "Failed to install extension: $extension (continuing anyway)"
        fi
    done
    
    return 0
}

# Function to create configuration files
create_config_files() {
    log "INFO" "Creating configuration files..."
    
    # Detect platform info
    local platform_info
    platform_info=$(detect_platform)
    local platform=$(echo "$platform_info" | cut -d'|' -f1)
    local os_type=$(echo "$platform_info" | cut -d'|' -f2)
    
    # Create main configuration
    local config_content
    config_content="{
  \"environment\": {
    \"platform\": \"$platform\",
    \"os_type\": \"$os_type\",
    \"base_path\": \"$PROJECT_DIR\",
    \"console_mode\": false
  },
  \"webui\": {
    \"selected\": \"forge\",
    \"launch_args\": \"--xformers --cuda-stream\",
    \"managed\": true
  },
  \"models\": {
    \"selected_sd15\": [],
    \"selected_sdxl\": [],
    \"text_input\": \"\",
    \"managed_downloads\": true
  },
  \"verbosity\": \"normal\",
  \"hardware\": {
    \"optimization_profile\": \"auto\",
    \"optimized\": true
  }
}"
    
    echo "$config_content" > "$PROJECT_DIR/config.json"
    log "SUCCESS" "Configuration file created"
    
    # Create basic requirements.txt if it doesn't exist
    if [[ ! -f "$PROJECT_DIR/requirements.txt" ]]; then
        local requirements_content
        requirements_content='# LSDAI-Simplified Requirements
requests>=2.25.0
tqdm>=4.60.0
jupyterlab>=3.0.0
notebook>=6.0.0
ipywidgets>=7.0.0
gitpython>=3.0.0
jupyter-server
papermill
nbformat
'
        echo "$requirements_content" > "$PROJECT_DIR/requirements.txt"
        log "SUCCESS" "Requirements file created"
    fi
    
    return 0
}

# Function to create auto-execution script
create_auto_execute_script() {
    log "INFO" "Creating auto-execution script..."
    
    # Determine Python path for script
    if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "win32" ]]; then
        PYTHON_PATH="venv\\\\Scripts\\\\python.exe"
    else
        PYTHON_PATH="venv/bin/python"
    fi
    
    local script_content
    script_content='#!/usr/bin/env python3
"""
LSDAI-Simplified Auto-execution Script
Designed for automatic notebook execution and WebUI management.
"""

import os
import sys
import json
import subprocess
import time
import signal
import threading
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/execution.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class AutoExecutor:
    """Automatic notebook executor"""
    
    def __init__(self):
        self.project_dir = Path.cwd()
        self.notebook_dir = self.project_dir
        self.notebooks = [
            "LSDAI-Simplified.ipynb",
            "LSDAI-Simplified-Windows.ipynb"
        ]
        self.server_process = None
        self.execution_status = {}
        self.stop_event = threading.Event()
        
    def get_python_executable(self) -> str:
        """Get Python executable from virtual environment"""
        if os.name == "nt":  # Windows
            return str(self.project_dir / "venv" / "Scripts" / "python.exe")
        else:  # Linux/macOS
            return str(self.project_dir / "venv" / "bin" / "python")
    
    def start_jupyter_server(self) -> bool:
        """Start Jupyter server in background"""
        logger.info("Starting Jupyter server...")
        
        python_exe = self.get_python_executable()
        
        cmd = [
            python_exe, "-m", "jupyter", "notebook",
            "--no-browser",
            "--port=8888",
            "--ip=127.0.0.1",
            "--allow-root",
            f"--notebook-dir={self.notebook_dir}"
        ]
        
        try:
            # Start server process
            self.server_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Wait for server to start
            logger.info("Waiting for Jupyter server to start...")
            time.sleep(10)
            
            # Check if server is running
            if self.server_process.poll() is None:
                logger.info("Jupyter server started successfully")
                return True
            else:
                logger.error("Jupyter server failed to start")
                return False
                
        except Exception as e:
            logger.error(f"Failed to start Jupyter server: {e}")
            return False
    
    def stop_jupyter_server(self):
        """Stop Jupyter server"""
        if self.server_process:
            logger.info("Stopping Jupyter server...")
            
            try:
                self.server_process.terminate()
                try:
                    self.server_process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    self.server_process.kill()
                
                logger.info("Jupyter server stopped")
            except Exception as e:
                logger.error(f"Error stopping Jupyter server: {e}")
    
    def execute_notebook(self, notebook_path: str) -> bool:
        """Execute notebook using papermill"""
        logger.info(f"Executing notebook: {notebook_path}")
        
        python_exe = self.get_python_executable()
        output_path = notebook_path.replace(".ipynb", "_executed.ipynb")
        
        cmd = [
            python_exe, "-m", "papermill",
            notebook_path,
            output_path,
            "--kernel", "python3",
            "--log-output",
            "--progress-bar",
            "--timeout", "1800"  # 30 minutes timeout
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=1800
            )
            
            if result.returncode == 0:
                logger.info(f"Successfully executed {notebook_path}")
                return True
            else:
                logger.error(f"Failed to execute {notebook_path}: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error(f"Timeout executing {notebook_path}")
            return False
        except Exception as e:
            logger.error(f"Error executing {notebook_path}: {e}")
            return False
    
    def run_all_notebooks(self) -> bool:
        """Execute all notebooks"""
        logger.info("Starting notebook execution...")
        
        # Start Jupyter server
        if not self.start_jupyter_server():
            return False
        
        try:
            # Execute each notebook
            for notebook in self.notebooks:
                if Path(notebook).exists():
                    success = self.execute_notebook(notebook)
                    self.execution_status[notebook] = success
                    
                    if not success:
                        logger.warning(f"Failed to execute {notebook}")
                else:
                    logger.warning(f"Notebook not found: {notebook}")
            
            # Check overall success
            successful = all(self.execution_status.values())
            if successful:
                logger.info("All notebooks executed successfully")
            else:
                logger.warning("Some notebooks failed to execute")
            
            return successful
            
        finally:
            # Stop Jupyter server
            self.stop_jupyter_server()

def main():
    """Main execution function"""
    executor = AutoExecutor()
    success = executor.run_all_notebooks()
    
    if success:
        print("✅ Auto-execution completed successfully")
        sys.exit(0)
    else:
        print("❌ Auto-execution failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
'
    
    echo "$script_content" > "$PROJECT_DIR/auto_execute.py"
    
    # Make script executable on Unix-like systems
    if [[ "$OSTYPE" != "msys" ]] && [[ "$OSTYPE" != "cygwin" ]] && [[ "$OSTYPE" != "win32" ]]; then
        chmod +x "$PROJECT_DIR/auto_execute.py"
    fi
    
    log "SUCCESS" "Auto-execution script created"
    return 0
}

# Function to display completion message
show_completion() {
    local platform_info
    platform_info=$(detect_platform)
    local platform=$(echo "$platform_info" | cut -d'|' -f1)
    
    echo
    log "SUCCESS" "LSDAI-Simplified installation completed successfully!"
    echo
    echo "🎉 Installation Complete!"
    echo "===================="
    echo
    echo "📋 Platform: $platform"
    echo "📁 Installation Directory: $PROJECT_DIR"
    echo "📄 Log File: $LOGS_DIR/install.log"
    echo
    echo "🚀 Next Steps:"
    echo "1. Activate virtual environment:"
    
    if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "win32" ]]; then
        echo "   $VENV_DIR\\\\Scripts\\\\activate"
    else
        echo "   source $VENV_DIR/bin/activate"
    fi
    
    echo
    echo "2. Start JupyterLab:"
    echo "   jupyter lab"
    echo
    echo "3. Open and run the notebook:"
    echo "   LSDAI-Simplified.ipynb (Linux/macOS)"
    echo "   LSDAI-Simplified-Windows.ipynb (Windows/Console)"
    echo
    echo "📁 Project Structure Created:"
    echo "   📂 scripts/ - Core scripts"
    echo "   📂 modules/ - Core modules"
    echo "   📂 data/ - Model data"
    echo "   📂 shared_models/ - Shared model storage"
    echo "   📂 webui_installations/ - WebUI installations"
    echo "   📂 configs/ - Configuration templates"
    echo "   📂 logs/ - Execution logs"
    echo
    echo "📄 Configuration Files Created:"
    echo "   - config.json: Main configuration"
    echo "   - requirements.txt: Python dependencies"
    echo "   - auto_execute.py: Auto-execution script"
    echo
    echo "🔧 For troubleshooting, check:"
    echo "   - Log files in: $LOGS_DIR/"
    echo "   - Installation log: $LOGS_DIR/install.log"
    echo
    echo "💡 Tips:"
    echo "   - Use 'python auto_execute.py' to run notebooks automatically"
    echo "   - Edit config.json to customize settings"
    echo "   - Check logs/ directory for execution logs"
}

# Main installation function
main() {
    echo "🚀 LSDAI-Simplified Universal Installer"
    echo "======================================"
    
    # Create logs directory
    mkdir -p "$LOGS_DIR"
    
    # Detect platform
    local platform_info
    platform_info=$(detect_platform)
    local platform=$(echo "$platform_info" | cut -d'|' -f1)
    local os_type=$(echo "$platform_info" | cut -d'|' -f2)
    
    log "INFO" "Starting universal installation..."
    log "INFO" "Platform: $platform ($os_type)"
    log "INFO" "Installation directory: $PROJECT_DIR"
    
    # Check Python version
    if ! check_python_version; then
        log "ERROR" "Python version check failed"
        exit 1
    fi
    
    # Install system dependencies
    if ! install_system_deps; then
        log "ERROR" "System dependencies installation failed"
        exit 1
    fi
    
    # Create virtual environment
    if ! create_venv; then
        log "ERROR" "Virtual environment creation failed"
        exit 1
    fi
    
    # Install Python packages
    if ! install_python_packages; then
        log "ERROR" "Python packages installation failed"
        exit 1
    fi
    
    # Create project structure
    if ! create_project_structure; then
        log "ERROR" "Project structure creation failed"
        exit 1
    fi
    
    # Setup Jupyter configuration
    if ! setup_jupyter_config; then
        log "ERROR" "Jupyter configuration setup failed"
        exit 1
    fi
    
    # Create configuration files
    if ! create_config_files; then
        log "ERROR" "Configuration files creation failed"
        exit 1
    fi
    
    # Create auto-execution script
    if ! create_auto_execute_script; then
        log "ERROR" "Auto-execution script creation failed"
        exit 1
    fi
    
    # Show completion message
    show_completion
    
    log "SUCCESS" "Universal installation completed successfully!"
}

# Error handling
handle_error() {
    local exit_code=$?
    local line_number=$1
    log "ERROR" "Installation failed on line $line_number with exit code $exit_code"
    log "ERROR" "Check the log file for details: $LOGS_DIR/install.log"
    exit $exit_code
}

# Set error trap
trap 'handle_error $LINENO' ERR

# Run main function
main "$@"