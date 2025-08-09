#!/bin/bash

# LSDAI-Simplified Setup Script
# Automated installation and setup for LSDAI-Simplified project

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install system dependencies
install_system_deps() {
    print_status "Installing system dependencies..."
    
    # Update package list
    if command_exists apt-get; then
        sudo apt-get update -qq
        sudo apt-get install -y -qq python3 python3-pip python3-venv git wget curl aria2 build-essential
        print_success "System dependencies installed"
    elif command_exists yum; then
        sudo yum install -y python3 python3-pip git wget curl aria2 gcc gcc-c++ make
        print_success "System dependencies installed"
    elif command_exists brew; then
        brew install python3 git wget curl aria2
        print_success "System dependencies installed"
    else
        print_warning "Could not detect package manager. Please install dependencies manually."
    fi
}

# Function to create virtual environment
create_venv() {
    print_status "Creating Python virtual environment..."
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_success "Virtual environment created"
    else
        print_warning "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip setuptools wheel
    print_success "pip upgraded"
}

# Function to install Python dependencies
install_python_deps() {
    print_status "Installing Python dependencies..."
    
    # Check if requirements.txt exists
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        print_success "Python dependencies installed"
    else
        print_warning "requirements.txt not found, installing basic dependencies"
        pip install requests tqdm jupyterlab notebook ipywidgets gitpython
        print_success "Basic Python dependencies installed"
    fi
}

# Function to create project structure
create_project_structure() {
    print_status "Creating project structure..."
    
    # Create necessary directories
    mkdir -p scripts modules data shared_models/Stable-diffusion shared_models/VAE shared_models/Lora shared_models/ControlNet shared_models/embeddings webui_installations downloads configs logs
    
    print_success "Project structure created"
}

# Function to setup Jupyter configuration
setup_jupyter() {
    print_status "Setting up Jupyter configuration..."
    
    # Create Jupyter config directory
    mkdir -p ~/.jupyter
    
    # Create Jupyter configuration
    cat > ~/.jupyter/jupyter_notebook_config.py << 'EOF'
# LSDAI-Simplified Jupyter Configuration
c = get_config()

# Server configuration
c.NotebookApp.ip = '127.0.0.1'
c.NotebookApp.port = 8888
c.NotebookApp.open_browser = False
c.NotebookApp.token = ''
c.NotebookApp.password = ''
c.NotebookApp.allow_root = True

# Extensions
c.NotebookApp.nbserver_extensions = {
    'jupyterlab': True,
    'notebook': True,
}

# Security settings for local development
c.NotebookApp.allow_origin = '*'
c.NotebookApp.disable_check_xsrf = True

# Auto-reload
c.InteractiveShellApp.extensions = ['autoreload']
c.InteractiveShellApp.exec_lines = ['%autoreload 2']
EOF
    
    print_success "Jupyter configuration created"
}

# Function to create basic configuration file
create_config() {
    print_status "Creating basic configuration file..."
    
    cat > config.json << 'EOF'
{
  "environment": {
    "platform": "auto-detected",
    "base_path": "./LSDAI-Simplified",
    "console_mode": false
  },
  "webui": {
    "selected": "forge",
    "launch_args": "--xformers --cuda-stream",
    "managed": true
  },
  "models": {
    "selected_sd15": [],
    "selected_sdxl": [],
    "text_input": "",
    "managed_downloads": true
  },
  "verbosity": "normal",
  "hardware": {
    "optimization_profile": "auto",
    "optimized": true
  }
}
EOF
    
    print_success "Configuration file created"
}

# Function to create auto-execution script
create_auto_execute() {
    print_status "Creating auto-execution script..."
    
    cat > auto_execute.py << 'EOF'
#!/usr/bin/env python3
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
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/execution.log'),
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
        if os.name == 'nt':  # Windows
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
        output_path = notebook_path.replace('.ipynb', '_executed.ipynb')
        
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
EOF
    
    print_success "Auto-execution script created"
}

# Function to display completion message
show_completion() {
    print_success "LSDAI-Simplified setup completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Activate virtual environment: source venv/bin/activate"
    echo "2. Start Jupyter: jupyter notebook"
    echo "3. Open LSDAI-Simplified.ipynb and run cells"
    echo "4. For Windows: Use LSDAI-Simplified-Windows.ipynb"
    echo ""
    echo "Configuration files created:"
    echo "- config.json: Project configuration"
    echo "- auto_execute.py: Auto-execution script"
    echo ""
    echo "Project structure ready in:"
    echo "- scripts/: Core scripts"
    echo "- modules/: Core modules"  
    echo "- data/: Model data"
    echo "- shared_models/: Shared model storage"
    echo "- logs/: Execution logs"
}

# Main installation process
main() {
    echo "🚀 LSDAI-Simplified Setup Script"
    echo "===================================="
    
    # Check if Python 3 is available
    if ! command_exists python3; then
        print_error "Python 3 is required but not installed"
        exit 1
    fi
    
    # Install system dependencies
    install_system_deps
    
    # Create virtual environment
    create_venv
    
    # Install Python dependencies
    install_python_deps
    
    # Create project structure
    create_project_structure
    
    # Setup Jupyter configuration
    setup_jupyter
    
    # Create configuration file
    create_config
    
    # Create auto-execution script
    create_auto_execute
    
    # Show completion message
    show_completion
}

# Run main function
main "$@"