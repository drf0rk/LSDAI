#!/usr/bin/env python3
"""
LSDAI-Simplified Complete Setup Script
Full-featured setup with JupyterLab integration and comprehensive configuration.
"""

import os
import sys
import subprocess
import json
import platform
import shutil
import venv
from pathlib import Path
import logging
import time

def setup_logging():
    """Setup logging for the setup process"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/setup.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def print_step(message):
    """Print step information"""
    print(f"🔧 {message}")

def print_success(message):
    """Print success message"""
    print(f"✅ {message}")

def print_error(message):
    """Print error message"""
    print(f"❌ {message}")

def print_warning(message):
    """Print warning message"""
    print(f"⚠️  {message}")

def run_command_safely(command, timeout=300, cwd=None):
    """Run command with comprehensive error handling"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", f"Command timed out after {timeout} seconds"
    except Exception as e:
        return False, "", str(e)

def check_system_requirements():
    """Check if system meets requirements"""
    print_step("Checking system requirements...")
    
    # Check Python version
    version = platform.python_version()
    major, minor = map(int, version.split('.')[:2])
    
    if major < 3 or (major == 3 and minor < 8):
        print_error(f"Python {major}.{minor} not supported. Need 3.8+")
        return False
    
    print_success(f"Python {version} is compatible")
    
    # Check available disk space (at least 1GB)
    try:
        total, used, free = shutil.disk_usage(".")
        free_gb = free // (1024**3)
        if free_gb < 1:
            print_error(f"Insufficient disk space: {free_gb}GB free (need at least 1GB)")
            return False
        print_success(f"Disk space: {free_gb}GB free")
    except:
        print_warning("Could not check disk space")
    
    return True

def create_enhanced_venv():
    """Create enhanced virtual environment"""
    print_step("Creating enhanced virtual environment...")
    
    venv_path = Path("venv")
    
    if venv_path.exists():
        print_warning("Virtual environment already exists, updating...")
        shutil.rmtree(venv_path)
    
    try:
        # Create virtual environment with pip
        venv.create(venv_path, with_pip=True, upgrade_deps=True)
        print_success("Virtual environment created")
        
        # Determine paths
        if platform.system() == "Windows":
            python_exe = venv_path / "Scripts" / "python.exe"
            pip_exe = venv_path / "Scripts" / "pip.exe"
        else:
            python_exe = venv_path / "bin" / "python"
            pip_exe = venv_path / "bin" / "pip"
        
        # Upgrade pip and setuptools
        success, stdout, stderr = run_command_safely(
            f'"{python_exe}" -m pip install --upgrade pip setuptools wheel'
        )
        
        if success:
            print_success("pip and setuptools upgraded")
        else:
            print_warning(f"pip upgrade failed: {stderr}")
        
        return True
        
    except Exception as e:
        print_error(f"Failed to create virtual environment: {e}")
        return False

def install_comprehensive_packages():
    """Install comprehensive Python packages"""
    print_step("Installing comprehensive Python packages...")
    
    # Get paths
    if platform.system() == "Windows":
        python_exe = "venv\\Scripts\\python.exe"
        pip_exe = "venv\\Scripts\\pip.exe"
    else:
        python_exe = "venv/bin/python"
        pip_exe = "venv/bin/pip"
    
    # Package categories
    packages = {
        "Core": [
            "requests>=2.25.0",
            "tqdm>=4.60.0", 
            "pathlib2>=2.3.0",
            "pyyaml>=6.0"
        ],
        "Jupyter": [
            "jupyterlab>=3.0.0",
            "notebook>=6.0.0",
            "ipywidgets>=7.0.0",
            "jupyter-server>=1.0.0",
            "jupyter-server-proxy>=3.0.0"
        ],
        "Development": [
            "gitpython>=3.0.0",
            "nbconvert>=6.0.0",
            "papermill>=2.3.0",
            "nbformat>=5.0.0"
        ],
        "Utilities": [
            "click>=8.0.0",
            "colorama>=0.4.0",
            "rich>=10.0.0"
        ]
    }
    
    # Install packages by category
    for category, package_list in packages.items():
        print_step(f"Installing {category} packages...")
        
        for package in package_list:
            print(f"  Installing {package}...")
            success, stdout, stderr = run_command_safely(f'"{pip_exe}" install {package}')
            
            if success:
                print(f"  ✅ {package}")
            else:
                print(f"  ❌ {package}: {stderr}")
                return False
    
    return True

def setup_jupyter_lab():
    """Setup JupyterLab with extensions"""
    print_step("Setting up JupyterLab...")
    
    # Get paths
    if platform.system() == "Windows":
        python_exe = "venv\\Scripts\\python.exe"
        jupyter_cmd = f'"{python_exe}" -m jupyter'
    else:
        python_exe = "venv/bin/python"
        jupyter_cmd = f'"{python_exe}" -m jupyter'
    
    # Install JupyterLab extensions
    extensions = [
        "@jupyter-widgets/jupyterlab-manager",
        "@jupyter-server/resource-usage",
        "@jupyterlab/toc",
        "@jupyterlab/debugger"
    ]
    
    for extension in extensions:
        print(f"  Installing {extension}...")
        success, stdout, stderr = run_command_safely(f'{jupyter_cmd} labextension install {extension}')
        
        if success:
            print(f"  ✅ {extension}")
        else:
            print(f"  ⚠️  {extension}: {stderr}")
    
    # Create Jupyter configuration
    print_step("Creating Jupyter configuration...")
    
    jupyter_dir = Path.home() / ".jupyter"
    jupyter_dir.mkdir(exist_ok=True)
    
    config_content = '''# LSDAI-Simplified Complete Jupyter Configuration
c = get_config()

# Server settings
c.NotebookApp.ip = "127.0.0.1"
c.NotebookApp.port = 8888
c.NotebookApp.open_browser = False
c.NotebookApp.token = ""
c.NotebookApp.password_required = False
c.NotebookApp.allow_root = True

# Extensions
c.NotebookApp.nbserver_extensions = {
    "jupyterlab": True,
    "notebook": True,
    "jupyter_server_proxy": True,
}

# Security for local development
c.NotebookApp.allow_origin = "*"
c.NotebookApp.disable_check_xsrf = True

# Auto-reload
c.InteractiveShellApp.extensions = ["autoreload"]
c.InteractiveShellApp.exec_lines = ["%autoreload 2"]

# Resource monitoring
c.ResourceUseDisplay.track_cpu_percent = True
c.ResourceUseDisplay.track_memory_percent = True

# Performance
c.MappingKernelManager.cull_idle_timeout = 3600
c.MappingKernelManager.cull_idle_timeout_min = 300
'''
    
    config_file = jupyter_dir / "jupyter_notebook_config.py"
    with open(config_file, 'w') as f:
        f.write(config_content)
    
    print_success("JupyterLab configuration created")
    return True

def create_comprehensive_structure():
    """Create comprehensive project structure"""
    print_step("Creating comprehensive project structure...")
    
    directories = [
        # Core directories
        "scripts",
        "modules",
        "data",
        "logs",
        
        # Model storage
        "shared_models/Stable-diffusion",
        "shared_models/VAE", 
        "shared_models/Lora",
        "shared_models/ControlNet",
        "shared_models/embeddings",
        "shared_models/hypernetworks",
        
        # WebUI installations
        "webui_installations/forge",
        "webui_installations/a1111",
        "webui_installations/comfyui",
        "webui_installations/fooocus",
        
        # Downloads and cache
        "downloads",
        "cache",
        
        # Configurations
        "configs/forge",
        "configs/a1111", 
        "configs/comfyui",
        "configs/fooocus",
        
        # Notebooks and docs
        "notebooks",
        "docs"
    ]
    
    for directory in directories:
        dir_path = Path(directory)
        dir_path.mkdir(parents=True, exist_ok=True)
        print_success(f"Created {directory}")
    
    return True

def create_comprehensive_config():
    """Create comprehensive configuration files"""
    print_step("Creating comprehensive configuration...")
    
    # Main configuration
    config = {
        "environment": {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "python_version": platform.python_version(),
            "base_path": str(Path.cwd()),
            "console_mode": False,
            "debug_mode": False
        },
        "webui": {
            "selected": "forge",
            "launch_args": "--xformers --cuda-stream",
            "managed": True,
            "auto_restart": True,
            "max_restarts": 3
        },
        "models": {
            "selected_sd15": [],
            "selected_sdxl": [],
            "text_input": "",
            "managed_downloads": True,
            "auto_categorize": True,
            "download_parallel": 3
        },
        "performance": {
            "optimization_profile": "auto",
            "optimized": True,
            "memory_limit_gb": 8,
            "gpu_memory_limit_gb": 4,
            "cpu_cores": 4
        },
        "interface": {
            "theme": "dark",
            "verbosity": "normal",
            "show_progress": True,
            "auto_save": True
        },
        "advanced": {
            "experimental_features": False,
            "developer_mode": False,
            "log_level": "INFO"
        }
    }
    
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print_success("Main configuration created")
    
    # Create development configuration
    dev_config = {
        "development": {
            "testing_enabled": True,
            "debug_mode": False,
            "log_to_file": True,
            "performance_monitoring": True
        },
        "paths": {
            "test_data": "tests/data",
            "test_output": "tests/output",
            "temp_files": "temp"
        }
    }
    
    with open("dev_config.json", "w") as f:
        json.dump(dev_config, f, indent=2)
    
    print_success("Development configuration created")
    return True

def create_enhanced_scripts():
    """Create enhanced utility scripts"""
    print_step("Creating enhanced utility scripts...")
    
    # Create enhanced auto-execute script
    auto_execute_content = '''#!/usr/bin/env python3
"""
Enhanced Auto-execution Script for LSDAI-Simplified
Features automatic notebook execution with comprehensive error handling.
"""

import os
import sys
import json
import subprocess
import time
import signal
import threading
import logging
import psutil
from pathlib import Path
from datetime import datetime

class EnhancedAutoExecutor:
    """Enhanced automatic notebook executor with monitoring"""
    
    def __init__(self):
        self.project_dir = Path.cwd()
        self.notebooks = [
            "LSDAI-Simplified.ipynb",
            "LSDAI-Simplified-Windows.ipynb"
        ]
        self.server_process = None
        self.execution_status = {}
        self.start_time = None
        self.logger = self.setup_logger()
        
    def setup_logger(self):
        """Setup comprehensive logging"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / f"auto_execute_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
                logging.StreamHandler(sys.stdout)
            ]
        )
        return logging.getLogger(__name__)
    
    def get_python_executable(self):
        """Get Python executable from virtual environment"""
        if os.name == 'nt':
            return str(self.project_dir / "venv" / "Scripts" / "python.exe")
        else:
            return str(self.project_dir / "venv" / "bin" / "python")
    
    def start_jupyter_server(self):
        """Start Jupyter server with monitoring"""
        self.logger.info("Starting Jupyter server...")
        
        python_exe = self.get_python_executable()
        cmd = [
            python_exe, "-m", "jupyter", "notebook",
            "--no-browser",
            "--port=8888",
            "--ip=127.0.0.1",
            "--allow-root",
            f"--notebook-dir={self.project_dir}"
        ]
        
        try:
            self.server_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Wait for server to start
            time.sleep(15)
            
            if self.server_process.poll() is None:
                self.logger.info("Jupyter server started successfully")
                return True
            else:
                self.logger.error("Jupyter server failed to start")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to start Jupyter server: {e}")
            return False
    
    def execute_notebook_enhanced(self, notebook_path):
        """Execute notebook with enhanced error handling"""
        self.logger.info(f"Executing notebook: {notebook_path}")
        
        python_exe = self.get_python_executable()
        output_path = notebook_path.replace('.ipynb', f'_executed_{int(time.time())}.ipynb')
        
        cmd = [
            python_exe, "-m", "papermill",
            notebook_path,
            output_path,
            "--kernel", "python3",
            "--log-output",
            "--progress-bar",
            "--timeout", "3600",  # 1 hour timeout
            "--request-save-on-cell-execute"
        ]
        
        try:
            start_time = time.time()
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=3600
            )
            end_time = time.time()
            
            execution_time = end_time - start_time
            
            if result.returncode == 0:
                self.logger.info(f"Successfully executed {notebook_path} in {execution_time:.2f}s")
                return True
            else:
                self.logger.error(f"Failed to execute {notebook_path}: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error(f"Timeout executing {notebook_path}")
            return False
        except Exception as e:
            self.logger.error(f"Error executing {notebook_path}: {e}")
            return False
    
    def monitor_resources(self):
        """Monitor system resources during execution"""
        def monitor():
            while self.server_process and self.server_process.poll() is None:
                try:
                    cpu_percent = psutil.cpu_percent(interval=5)
                    memory = psutil.virtual_memory()
                    disk = psutil.disk_usage('/')
                    
                    self.logger.info(f"Resources - CPU: {cpu_percent}%, "
                                   f"Memory: {memory.percent}%, "
                                   f"Disk: {disk.percent}%")
                    
                    time.sleep(30)
                except:
                    pass
        
        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()
    
    def run_all_notebooks(self):
        """Execute all notebooks with enhanced monitoring"""
        self.logger.info("Starting enhanced notebook execution...")
        self.start_time = time.time()
        
        if not self.start_jupyter_server():
            return False
        
        # Start resource monitoring
        self.monitor_resources()
        
        try:
            for notebook in self.notebooks:
                if Path(notebook).exists():
                    success = self.execute_notebook_enhanced(notebook)
                    self.execution_status[notebook] = success
                    
                    if not success:
                        self.logger.warning(f"Failed to execute {notebook}")
                else:
                    self.logger.warning(f"Notebook not found: {notebook}")
            
            total_time = time.time() - self.start_time
            successful = all(self.execution_status.values())
            
            self.logger.info(f"Execution completed in {total_time:.2f}s")
            
            if successful:
                self.logger.info("All notebooks executed successfully")
            else:
                self.logger.warning("Some notebooks failed to execute")
            
            return successful
            
        finally:
            self.stop_jupyter_server()
    
    def stop_jupyter_server(self):
        """Stop Jupyter server gracefully"""
        if self.server_process:
            self.logger.info("Stopping Jupyter server...")
            
            try:
                self.server_process.terminate()
                try:
                    self.server_process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    self.server_process.kill()
                
                self.logger.info("Jupyter server stopped")
            except Exception as e:
                self.logger.error(f"Error stopping Jupyter server: {e}")

def main():
    """Main execution function"""
    executor = EnhancedAutoExecutor()
    success = executor.run_all_notebooks()
    
    if success:
        print("✅ Enhanced auto-execution completed successfully")
        sys.exit(0)
    else:
        print("❌ Enhanced auto-execution failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
    
    with open("auto_execute.py", "w") as f:
        f.write(auto_execute_content)
    
    # Make executable on Unix
    if platform.system() != "Windows":
        os.chmod("auto_execute.py", 0o755)
    
    print_success("Enhanced auto-execute script created")
    
    # Create system info script
    system_info_content = '''#!/usr/bin/env python3
"""
System Information Script for LSDAI-Simplified
Displays system information and compatibility status.
"""

import platform
import sys
import psutil
from pathlib import Path

def print_system_info():
    """Print comprehensive system information"""
    print("🔍 LSDAI-Simplified System Information")
    print("=" * 50)
    
    # System info
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Python Version: {platform.python_version()}")
    print(f"Python Executable: {sys.executable}")
    
    # Memory info
    memory = psutil.virtual_memory()
    print(f"Total Memory: {memory.total // (1024**3):.1f} GB")
    print(f"Available Memory: {memory.available // (1024**3):.1f} GB")
    
    # Disk info
    disk = psutil.disk_usage(".")
    print(f"Total Disk Space: {disk.total // (1024**3):.1f} GB")
    print(f"Free Disk Space: {disk.free // (1024**3):.1f} GB")
    
    # GPU info (if available)
    try:
        import torch
        if torch.cuda.is_available():
            print(f"GPU: {torch.cuda.get_device_name()}")
            print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory // (1024**3):.1f} GB")
        else:
            print("GPU: Not available or CUDA not installed")
    except ImportError:
        print("GPU: PyTorch not installed")
    
    # Project structure
    print("\\n📁 Project Structure:")
    required_dirs = ["scripts", "modules", "data", "shared_models", "logs"]
    for directory in required_dirs:
        if Path(directory).exists():
            print(f"  ✅ {directory}")
        else:
            print(f"  ❌ {directory} (missing)")
    
    # Configuration files
    print("\\n📄 Configuration Files:")
    config_files = ["config.json", "requirements.txt", "auto_execute.py"]
    for file in config_files:
        if Path(file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (missing)")

if __name__ == "__main__":
    print_system_info()
'''
    
    with open("system_info.py", "w") as f:
        f.write(system_info_content)
    
    if platform.system() != "Windows":
        os.chmod("system_info.py", 0o755)
    
    print_success("System info script created")
    
    return True

def create_comprehensive_requirements():
    """Create comprehensive requirements file"""
    print_step("Creating comprehensive requirements file...")
    
    requirements_content = '''# LSDAI-Simplified Comprehensive Requirements

# Core Dependencies
requests>=2.25.0
tqdm>=4.60.0
pathlib2>=2.3.0
pyyaml>=6.0
click>=8.0.0
colorama>=0.4.0
rich>=10.0.0

# Jupyter Ecosystem
jupyterlab>=3.0.0
notebook>=6.0.0
ipywidgets>=7.0.0
jupyter-server>=1.0.0
jupyter-server-proxy>=3.0.0
jupyter-resource-usage>=0.6.0

# Notebook Execution
nbconvert>=6.0.0
papermill>=2.3.0
nbformat>=5.0.0
nbclient>=0.5.0

# Development & Testing
pytest>=6.0.0
pytest-cov>=2.0.0
black>=21.0.0
flake8>=3.8.0
mypy>=0.910

# Git Integration
gitpython>=3.0.0
GitPython>=3.1.0

# System Monitoring
psutil>=5.8.0

# Optional: AI/ML (uncomment if needed)
# torch>=1.9.0
# torchvision>=0.10.0
# transformers>=4.0.0

# Optional: Enhanced Features (uncomment if needed)
# matplotlib>=3.3.0
# seaborn>=0.11.0
# plotly>=5.0.0
'''
    
    with open("requirements.txt", "w") as f:
        f.write(requirements_content)
    
    print_success("Comprehensive requirements file created")
    return True

def show_completion_summary():
    """Show comprehensive completion summary"""
    print()
    print("🎉 LSDAI-Simplified Complete Setup Finished!")
    print("=" * 55)
    print()
    print("📋 Setup Summary:")
    print("✅ Enhanced virtual environment")
    print("✅ Comprehensive Python packages")
    print("✅ JupyterLab with extensions")
    print("✅ Complete project structure")
    print("✅ Enhanced configuration files")
    print("✅ Utility scripts")
    print("✅ Comprehensive requirements")
    print()
    print("🚀 Quick Start:")
    if platform.system() == "Windows":
        print("1. Activate: venv\\Scripts\\activate")
    else:
        print("1. Activate: source venv/bin/activate")
    print("2. Start: jupyter lab")
    print("3. Open: LSDAI-Simplified.ipynb")
    print()
    print("🛠️  Available Scripts:")
    print("- auto_execute.py: Enhanced notebook execution")
    print("- system_info.py: System information display")
    print("- requirements.txt: All dependencies")
    print()
    print("📁 Project Structure:")
    print("   📂 scripts/ - Core execution scripts")
    print("   📂 modules/ - Python modules")
    print("   📂 data/ - Model data files")
    print("   📂 shared_models/ - Shared model storage")
    print("   📂 webui_installations/ - WebUI installations")
    print("   📂 configs/ - Configuration templates")
    print("   📂 logs/ - Execution and setup logs")
    print()
    print("📖 Documentation:")
    print("   📄 config.json - Main configuration")
    print("   📄 dev_config.json - Development settings")
    print("   📄 logs/setup.log - Setup log file")
    print()
    print("For issues, check the logs directory or run:")
    print("python system_info.py")

def main():
    """Main setup function"""
    logger = setup_logging()
    
    print("🚀 LSDAI-Simplified Complete Setup")
    print("=" * 45)
    
    # Check system requirements
    if not check_system_requirements():
        return False
    
    # Create enhanced virtual environment
    if not create_enhanced_venv():
        return False
    
    # Install comprehensive packages
    if not install_comprehensive_packages():
        return False
    
    # Setup JupyterLab
    if not setup_jupyter_lab():
        return False
    
    # Create comprehensive structure
    if not create_comprehensive_structure():
        return False
    
    # Create comprehensive configuration
    if not create_comprehensive_config():
        return False
    
    # Create enhanced scripts
    if not create_enhanced_scripts():
        return False
    
    # Create comprehensive requirements
    if not create_comprehensive_requirements():
        return False
    
    # Show completion summary
    show_completion_summary()
    
    logger.info("Complete setup finished successfully")
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("✅ Complete setup finished successfully!")
            sys.exit(0)
        else:
            print("❌ Complete setup failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\\n❌ Setup failed with error: {e}")
        sys.exit(1)