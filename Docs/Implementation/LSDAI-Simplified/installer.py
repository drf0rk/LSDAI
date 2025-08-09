#!/usr/bin/env python3
"""
LSDAI-Simplified Installer
Comprehensive installation and setup script for LSDAI-Simplified project.
"""

import os
import sys
import subprocess
import json
import platform
import shutil
import venv
import tempfile
import urllib.request
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import logging
import time

class LSDAIInstaller:
    """Comprehensive installer for LSDAI-Simplified"""
    
    def __init__(self):
        self.project_dir = Path.cwd()
        self.venv_dir = self.project_dir / "venv"
        self.logs_dir = self.project_dir / "logs"
        self.setup_log = []
        self.system_info = self._get_system_info()
        
        # Setup logging
        self._setup_logging()
        
    def _setup_logging(self):
        """Setup logging configuration"""
        self.logs_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.logs_dir / "install.log"),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def _get_system_info(self) -> Dict[str, Any]:
        """Get detailed system information"""
        return {
            'platform': platform.system(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'python_version': platform.python_version(),
            'python_executable': sys.executable,
            'is_windows': platform.system() == 'Windows',
            'is_linux': platform.system() == 'Linux',
            'is_macos': platform.system() == 'Darwin',
            'home_dir': Path.home(),
            'current_dir': Path.cwd()
        }
    
    def log(self, message: str, level: str = "INFO"):
        """Log message with timestamp"""
        log_entry = f"[{level}] {message}"
        self.setup_log.append(log_entry)
        
        if level == "ERROR":
            self.logger.error(message)
        elif level == "WARNING":
            self.logger.warning(message)
        elif level == "SUCCESS":
            self.logger.info(f"✓ {message}")
        else:
            self.logger.info(message)
    
    def run_command(self, command: List[str], cwd: Optional[Path] = None,
                   timeout: int = 300, capture_output: bool = True) -> Dict[str, Any]:
        """Run a command and return result"""
        try:
            self.log(f"Running: {' '.join(command)}")
            
            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=capture_output,
                text=True,
                timeout=timeout
            )
            
            return {
                'success': result.returncode == 0,
                'returncode': result.returncode,
                'stdout': result.stdout if capture_output else '',
                'stderr': result.stderr if capture_output else ''
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'returncode': -1,
                'stdout': '',
                'stderr': f'Command timed out after {timeout} seconds'
            }
        except Exception as e:
            return {
                'success': False,
                'returncode': -1,
                'stdout': '',
                'stderr': str(e)
            }
    
    def check_python_version(self) -> bool:
        """Check if Python version is compatible"""
        self.log("Checking Python version...")
        
        version = self.system_info['python_version']
        major, minor = map(int, version.split('.')[:2])
        
        if major < 3 or (major == 3 and minor < 8):
            self.log(f"Python {major}.{minor} not supported. Need 3.8+", "ERROR")
            return False
        
        self.log(f"Python {major}.{minor} is compatible", "SUCCESS")
        return True
    
    def create_virtual_environment(self) -> bool:
        """Create Python virtual environment"""
        self.log("Creating virtual environment...")
        
        try:
            # Create virtual environment
            venv.create(self.venv_dir, with_pip=True)
            self.log("Virtual environment created", "SUCCESS")
            
            # Get paths for the virtual environment
            if self.system_info['is_windows']:
                python_exe = self.venv_dir / "Scripts" / "python.exe"
                pip_exe = self.venv_dir / "Scripts" / "pip.exe"
            else:
                python_exe = self.venv_dir / "bin" / "python"
                pip_exe = self.venv_dir / "bin" / "pip"
            
            # Upgrade pip
            result = self.run_command([
                str(python_exe), "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"
            ])
            
            if result['success']:
                self.log("pip upgraded successfully", "SUCCESS")
            else:
                self.log(f"pip upgrade failed: {result['stderr']}", "WARNING")
            
            return True
            
        except Exception as e:
            self.log(f"Failed to create virtual environment: {e}", "ERROR")
            return False
    
    def install_system_dependencies(self) -> bool:
        """Install system-level dependencies"""
        self.log("Installing system dependencies...")
        
        if self.system_info['is_linux']:
            # Install Linux dependencies
            packages = ['git', 'python3-pip', 'python3-venv', 'wget', 'curl', 'aria2', 'build-essential']
            
            for package in packages:
                result = self.run_command(['sudo', 'apt-get', 'install', '-y', package])
                if not result['success']:
                    self.log(f"Failed to install {package}: {result['stderr']}", "WARNING")
                else:
                    self.log(f"Installed {package}", "SUCCESS")
        
        elif self.system_info['is_macos']:
            # Check for Homebrew and install dependencies
            result = self.run_command(['brew', '--version'])
            if result['success']:
                packages = ['git', 'wget', 'curl', 'aria2']
                for package in packages:
                    self.run_command(['brew', 'install', package])
            else:
                self.log("Homebrew not found. Please install system dependencies manually.", "WARNING")
        
        elif self.system_info['is_windows']:
            # Check for Git
            result = self.run_command(['git', '--version'])
            if not result['success']:
                self.log("Git not found. Please install Git for Windows.", "WARNING")
        
        return True
    
    def install_python_packages(self) -> bool:
        """Install required Python packages"""
        self.log("Installing Python packages...")
        
        # Get Python executable from virtual environment
        if self.system_info['is_windows']:
            python_exe = self.venv_dir / "Scripts" / "python.exe"
        else:
            python_exe = self.venv_dir / "bin" / "python"
        
        # Core packages
        core_packages = [
            'requests>=2.25.0',
            'tqdm>=4.60.0',
            'jupyterlab>=3.0.0',
            'notebook>=6.0.0',
            'ipywidgets>=7.0.0',
            'gitpython>=3.0.0'
        ]
        
        # Jupyter execution packages
        jupyter_packages = [
            'jupyter-server',
            'jupyter-server-proxy',
            'jupyter-resource-usage',
            'nbconvert',
            'papermill',
            'nbformat'
        ]
        
        all_packages = core_packages + jupyter_packages
        
        # Install packages
        for package in all_packages:
            self.log(f"Installing {package}...")
            
            result = self.run_command([
                str(python_exe), "-m", "pip", "install", package, "--upgrade"
            ])
            
            if result['success']:
                self.log(f"Successfully installed {package}", "SUCCESS")
            else:
                self.log(f"Failed to install {package}: {result['stderr']}", "WARNING")
        
        return True
    
    def setup_jupyter_configuration(self) -> bool:
        """Setup JupyterLab configuration"""
        self.log("Setting up JupyterLab configuration...")
        
        # Get Python executable from virtual environment
        if self.system_info['is_windows']:
            python_exe = self.venv_dir / "Scripts" / "python.exe"
            jupyter_cmd = [str(python_exe), "-m", "jupyter"]
        else:
            python_exe = self.venv_dir / "bin" / "python"
            jupyter_cmd = [str(python_exe), "-m", "jupyter"]
        
        # Install JupyterLab extensions
        extensions = [
            '@jupyter-widgets/jupyterlab-manager',
            '@jupyter-server/resource-usage'
        ]
        
        for extension in extensions:
            result = self.run_command(jupyter_cmd + ['labextension', 'install', extension])
            if not result['success']:
                self.log(f"Failed to install extension {extension}: {result['stderr']}", "WARNING")
        
        # Create Jupyter configuration directory
        jupyter_config_dir = Path.home() / '.jupyter'
        jupyter_config_dir.mkdir(exist_ok=True)
        
        # Create Jupyter configuration
        config_content = '''# LSDAI-Simplified Jupyter Configuration
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
    'jupyter_server_proxy': True,
}

# Security settings for local development
c.NotebookApp.allow_origin = '*'
c.NotebookApp.disable_check_xsrf = True

# Auto-reload
c.InteractiveShellApp.extensions = ['autoreload']
c.InteractiveShellApp.exec_lines = ['%autoreload 2']

# Resource usage monitoring
c.ResourceUseDisplay.track_cpu_percent = True
c.ResourceUseDisplay.track_memory_percent = True
'''
        
        config_file = jupyter_config_dir / 'jupyter_notebook_config.py'
        with open(config_file, 'w') as f:
            f.write(config_content)
        
        self.log("JupyterLab configuration created", "SUCCESS")
        return True
    
    def create_project_structure(self) -> bool:
        """Create project directory structure"""
        self.log("Creating project structure...")
        
        directories = [
            'scripts',
            'modules',
            'data',
            'shared_models/Stable-diffusion',
            'shared_models/VAE',
            'shared_models/Lora',
            'shared_models/ControlNet',
            'shared_models/embeddings',
            'webui_installations',
            'downloads',
            'configs',
            'logs'
        ]
        
        for directory in directories:
            dir_path = self.project_dir / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            self.log(f"Created directory: {directory}", "SUCCESS")
        
        return True
    
    def create_configuration_files(self) -> bool:
        """Create configuration files"""
        self.log("Creating configuration files...")
        
        # Create main configuration
        config_content = {
            "environment": {
                "platform": self.system_info['platform'],
                "base_path": str(self.project_dir),
                "console_mode": False
            },
            "webui": {
                "selected": "forge",
                "launch_args": "--xformers --cuda-stream",
                "managed": True
            },
            "models": {
                "selected_sd15": [],
                "selected_sdxl": [],
                "text_input": "",
                "managed_downloads": True
            },
            "verbosity": "normal",
            "hardware": {
                "optimization_profile": "auto",
                "optimized": True
            }
        }
        
        config_file = self.project_dir / "config.json"
        with open(config_file, 'w') as f:
            json.dump(config_content, f, indent=2)
        
        self.log("Configuration file created", "SUCCESS")
        return True
    
    def create_auto_execution_script(self) -> bool:
        """Create automatic notebook execution script"""
        self.log("Creating auto-execution script...")
        
        # Get Python executable path
        if self.system_info['is_windows']:
            python_exe = "venv\\Scripts\\python.exe"
        else:
            python_exe = "venv/bin/python"
        
        script_content = f'''#!/usr/bin/env python3
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
        self.execution_status = {{}}
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
            f"--notebook-dir={{self.notebook_dir}}"
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
            logger.error(f"Failed to start Jupyter server: {{e}}")
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
                logger.error(f"Error stopping Jupyter server: {{e}}")
    
    def execute_notebook(self, notebook_path: str) -> bool:
        """Execute notebook using papermill"""
        logger.info(f"Executing notebook: {{notebook_path}}")
        
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
                logger.info(f"Successfully executed {{notebook_path}}")
                return True
            else:
                logger.error(f"Failed to execute {{notebook_path}}: {{result.stderr}}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error(f"Timeout executing {{notebook_path}}")
            return False
        except Exception as e:
            logger.error(f"Error executing {{notebook_path}}: {{e}}")
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
                        logger.warning(f"Failed to execute {{notebook}}")
                else:
                    logger.warning(f"Notebook not found: {{notebook}}")
            
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
'''
        
        script_file = self.project_dir / "auto_execute.py"
        with open(script_file, 'w') as f:
            f.write(script_content)
        
        # Make script executable on Unix systems
        if not self.system_info['is_windows']:
            script_file.chmod(0o755)
        
        self.log("Auto-execution script created", "SUCCESS")
        return True
    
    def create_requirements_file(self) -> bool:
        """Create requirements.txt file"""
        self.log("Creating requirements.txt file...")
        
        requirements_content = '''# Core dependencies
requests>=2.25.0
tqdm>=4.60.0
jupyterlab>=3.0.0
notebook>=6.0.0
ipywidgets>=7.0.0
gitpython>=3.0.0

# Jupyter execution
jupyter-server
jupyter-server-proxy
jupyter-resource-usage
nbconvert
papermill
nbformat

# Development and testing
pytest>=6.0.0
pytest-cov>=2.0.0
black>=21.0.0
flake8>=3.8.0
'''
        
        requirements_file = self.project_dir / "requirements.txt"
        with open(requirements_file, 'w') as f:
            f.write(requirements_content)
        
        self.log("Requirements file created", "SUCCESS")
        return True
    
    def show_completion_message(self):
        """Show completion message"""
        self.log("Installation completed successfully!", "SUCCESS")
        print()
        print("🎉 LSDAI-Simplified Installation Complete!")
        print("=" * 50)
        print()
        print("Next steps:")
        print("1. Activate virtual environment:")
        if self.system_info['is_windows']:
            print("   venv\\Scripts\\activate")
        else:
            print("   source venv/bin/activate")
        print()
        print("2. Start JupyterLab:")
        print("   jupyter lab")
        print()
        print("3. Open and run the notebook:")
        print("   LSDAI-Simplified.ipynb (Linux/macOS)")
        print("   LSDAI-Simplified-Windows.ipynb (Windows)")
        print()
        print("4. Configuration files created:")
        print("   - config.json: Project configuration")
        print("   - auto_execute.py: Auto-execution script")
        print("   - requirements.txt: Python dependencies")
        print()
        print("Project structure:")
        print("   📁 scripts/ - Core scripts")
        print("   📁 modules/ - Core modules")
        print("   📁 data/ - Model data")
        print("   📁 shared_models/ - Shared model storage")
        print("   📁 logs/ - Execution logs")
        print()
        print("For troubleshooting, check:")
        print(f"   📄 {self.logs_dir}/install.log")
    
    def install(self) -> bool:
        """Run complete installation process"""
        self.log("Starting LSDAI-Simplified installation...")
        self.log(f"System: {self.system_info['platform']} {self.system_info['architecture']}")
        self.log(f"Python: {self.system_info['python_version']}")
        
        # Check Python version
        if not self.check_python_version():
            return False
        
        # Install system dependencies
        if not self.install_system_dependencies():
            return False
        
        # Create virtual environment
        if not self.create_virtual_environment():
            return False
        
        # Install Python packages
        if not self.install_python_packages():
            return False
        
        # Setup Jupyter configuration
        if not self.setup_jupyter_configuration():
            return False
        
        # Create project structure
        if not self.create_project_structure():
            return False
        
        # Create configuration files
        if not self.create_configuration_files():
            return False
        
        # Create auto-execution script
        if not self.create_auto_execution_script():
            return False
        
        # Create requirements file
        if not self.create_requirements_file():
            return False
        
        # Show completion message
        self.show_completion_message()
        
        return True

def main():
    """Main entry point"""
    installer = LSDAIInstaller()
    
    try:
        success = installer.install()
        if success:
            print("\n✅ Installation completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Installation failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Installation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Installation failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()