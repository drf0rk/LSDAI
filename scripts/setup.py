#!/usr/bin/env python3
"""
LSDAI Simplified Setup System - Enhanced Version
Cell 1: Environment Setup & Advanced Configuration

This enhanced setup system provides:
- Comprehensive platform detection (Colab/Kaggle/Paperspace/Local)
- Robust dependency management with multiple fallback mechanisms
- Advanced directory structure validation and creation
- System diagnostics and health checks
- Enhanced configuration management with validation
- Progress indicators and detailed user feedback
"""

import os
import sys
import json
import subprocess
import shutil
import platform
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import time

# Optional imports
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

class EnhancedSetup:
    """Enhanced setup system for LSDAI with comprehensive features"""
    
    def __init__(self):
        self.base_path = Path.cwd()
        self.project_root = self.base_path / 'LSDAI-Simplified'
        self.config_file = self.project_root / 'config.json'
        self.setup_log = []
        self.progress_callbacks = []
        
    def log_progress(self, message: str, level: str = "INFO"):
        """Log progress message with timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        self.setup_log.append(log_entry)
        print(f"📝 {log_entry}")
        
        # Call progress callbacks if any
        for callback in self.progress_callbacks:
            callback(message, level)
    
    def add_progress_callback(self, callback):
        """Add progress callback function"""
        self.progress_callbacks.append(callback)
    
    def detect_platform(self) -> Dict[str, str]:
        """Enhanced platform detection with detailed information"""
        platform_info = {
            'type': 'unknown',
            'name': 'Unknown',
            'python_version': sys.version,
            'os': platform.system(),
            'os_version': platform.version(),
            'architecture': platform.machine(),
            'processor': platform.processor()
        }
        
        # Detect specific cloud platforms
        if 'COLAB_GPU' in os.environ:
            platform_info.update({
                'type': 'colab',
                'name': 'Google Colab',
                'gpu_available': True
            })
        elif 'KAGGLE_KERNEL_RUN_TYPE' in os.environ:
            platform_info.update({
                'type': 'kaggle',
                'name': 'Kaggle',
                'gpu_available': os.environ.get('KAGGLE_KERNEL_RUN_TYPE') == 'GPU'
            })
        elif 'PAPERSPACE_NOTEBOOK_ID' in os.environ:
            platform_info.update({
                'type': 'paperspace',
                'name': 'Paperspace',
                'gpu_available': True
            })
        else:
            platform_info.update({
                'type': 'local',
                'name': 'Local Environment',
                'gpu_available': self._detect_local_gpu()
            })
        
        return platform_info
    
    def _detect_local_gpu(self) -> bool:
        """Detect if GPU is available in local environment"""
        try:
            # Try to detect CUDA
            result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
            if result.returncode == 0:
                return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # Try to detect via torch if available
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            pass
        
        return False
    
    def get_system_resources(self) -> Dict[str, any]:
        """Get detailed system resource information"""
        try:
            if PSUTIL_AVAILABLE:
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                cpu_count = psutil.cpu_count()
                cpu_percent = psutil.cpu_percent(interval=1)
                
                return {
                    'memory_total_gb': round(memory.total / (1024**3), 2),
                    'memory_available_gb': round(memory.available / (1024**3), 2),
                    'memory_percent': memory.percent,
                    'disk_total_gb': round(disk.total / (1024**3), 2),
                    'disk_free_gb': round(disk.free / (1024**3), 2),
                    'disk_percent': disk.percent,
                    'cpu_count': cpu_count,
                    'cpu_percent': cpu_percent
                }
            else:
                # Fallback method without psutil
                import os
                import statvfs
                
                # Get disk info (Unix-like systems)
                try:
                    stat = os.statvfs('/')
                    disk_total = stat.f_frsize * stat.f_blocks
                    disk_free = stat.f_frsize * stat.f_bavail
                    disk_percent = round((1 - stat.f_bavail / stat.f_blocks) * 100, 1)
                except (AttributeError, OSError):
                    disk_total = disk_free = disk_percent = 0
                
                # Get memory info (Unix-like systems)
                try:
                    with open('/proc/meminfo', 'r') as f:
                        meminfo = f.read()
                        mem_total = int([line for line in meminfo.split('\n') if 'MemTotal:' in line][0].split()[1])
                        mem_available = int([line for line in meminfo.split('\n') if 'MemAvailable:' in line][0].split()[1])
                        mem_percent = round((1 - mem_available / mem_total) * 100, 1)
                except (FileNotFoundError, IndexError, ValueError):
                    mem_total = mem_available = mem_percent = 0
                
                # Get CPU info
                try:
                    cpu_count = os.cpu_count() or 1
                    # Simple CPU load calculation (not very accurate without psutil)
                    cpu_percent = 0  # Default to 0 as we can't easily measure
                except:
                    cpu_count = 1
                    cpu_percent = 0
                
                return {
                    'memory_total_gb': round(mem_total / (1024**2), 2),  # Convert KB to GB
                    'memory_available_gb': round(mem_available / (1024**2), 2),
                    'memory_percent': mem_percent,
                    'disk_total_gb': round(disk_total / (1024**3), 2),
                    'disk_free_gb': round(disk_free / (1024**3), 2),
                    'disk_percent': disk_percent,
                    'cpu_count': cpu_count,
                    'cpu_percent': cpu_percent,
                    'note': 'Limited system info (psutil not available)'
                }
        except Exception as e:
            self.log_progress(f"Error getting system resources: {e}", "WARNING")
            return {'error': str(e), 'note': 'System resource detection failed'}
    
    def validate_directory_structure(self) -> Dict[str, bool]:
        """Validate existing directory structure"""
        required_dirs = [
            'shared_models/Stable-diffusion',
            'shared_models/VAE', 
            'shared_models/Lora',
            'shared_models/ControlNet',
            'shared_models/embeddings',
            'webui_installations',
            'downloads',
            'scripts',
            'modules',
            'data',
            'configs'
        ]
        
        validation_results = {}
        for directory in required_dirs:
            path = self.project_root / directory
            validation_results[directory] = path.exists()
        
        return validation_results
    
    def create_directory_structure(self) -> bool:
        """Create and validate directory structure with enhanced error handling"""
        self.log_progress("Creating directory structure...")
        
        directories = [
            'shared_models/Stable-diffusion',
            'shared_models/VAE', 
            'shared_models/Lora',
            'shared_models/ControlNet',
            'shared_models/embeddings',
            'webui_installations',
            'downloads',
            'scripts',
            'modules',
            'data',
            'configs',
            'configs/forge',
            'configs/a1111',
            'configs/comfyui',
            'configs/fooocus',
            'logs'
        ]
        
        success_count = 0
        for directory in directories:
            try:
                path = self.project_root / directory
                path.mkdir(parents=True, exist_ok=True)
                
                # Create .gitkeep files to preserve empty directories
                gitkeep_file = path / '.gitkeep'
                if not gitkeep_file.exists():
                    gitkeep_file.touch()
                
                success_count += 1
                self.log_progress(f"✅ Created: {directory}")
            except Exception as e:
                self.log_progress(f"❌ Failed to create {directory}: {e}", "ERROR")
        
        self.log_progress(f"Directory structure creation: {success_count}/{len(directories)} successful")
        return success_count == len(directories)
    
    def get_default_config(self) -> Dict[str, any]:
        """Get enhanced default configuration with validation"""
        platform_info = self.detect_platform()
        
        return {
            "environment": {
                "platform": platform_info['type'],
                "platform_name": platform_info['name'],
                "base_path": str(self.project_root),
                "gpu_available": platform_info.get('gpu_available', False),
                "python_version": platform_info['python_version'],
                "setup_timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            },
            "webui": {
                "selected": "forge",
                "launch_args": "--xformers --cuda-stream",
                "available_webuis": ["forge", "a1111", "comfyui", "fooocus"],
                "sequential_execution": True
            },
            "models": {
                "selected_sd15": [],
                "selected_sdxl": [],
                "text_input": "",
                "auto_categorize": True,
                "shared_storage": True
            },
            "verbosity": "pretty",
            "hardware": {
                "optimization_profile": "auto",
                "detected_hardware": {},
                "custom_args": ""
            },
            "download": {
                "prefer_aria2c": True,
                "max_concurrent_downloads": 3,
                "retry_attempts": 3,
                "timeout_seconds": 300
            },
            "ui": {
                "accordion_layout": True,
                "show_progress": True,
                "auto_save": True
            }
        }
    
    def validate_config(self, config: Dict[str, any]) -> Tuple[bool, List[str]]:
        """Validate configuration structure and values"""
        errors = []
        
        # Required sections
        required_sections = ['environment', 'webui', 'models', 'hardware']
        for section in required_sections:
            if section not in config:
                errors.append(f"Missing required section: {section}")
        
        # Validate webui selection
        if 'webui' in config:
            valid_webuis = ['forge', 'a1111', 'comfyui', 'fooocus']
            if config['webui'].get('selected') not in valid_webuis:
                errors.append(f"Invalid WebUI selection: {config['webui'].get('selected')}")
        
        # Validate verbosity
        if 'verbosity' in config:
            valid_verbosity = ['pretty', 'raw', 'debug']
            if config['verbosity'] not in valid_verbosity:
                errors.append(f"Invalid verbosity setting: {config['verbosity']}")
        
        # Validate hardware optimization
        if 'hardware' in config:
            valid_profiles = ['auto', 'low_vram', 'medium_vram', 'high_vram', 'cpu_only']
            if config['hardware'].get('optimization_profile') not in valid_profiles:
                errors.append(f"Invalid hardware profile: {config['hardware'].get('optimization_profile')}")
        
        return len(errors) == 0, errors
    
    def setup_config(self) -> bool:
        """Setup enhanced JSON configuration with validation"""
        self.log_progress("Setting up configuration...")
        
        try:
            if not self.config_file.exists():
                config = self.get_default_config()
                
                # Validate default config
                is_valid, errors = self.validate_config(config)
                if not is_valid:
                    self.log_progress(f"Default configuration validation failed: {errors}", "ERROR")
                    return False
                
                with open(self.config_file, 'w') as f:
                    json.dump(config, f, indent=2)
                
                self.log_progress("✅ Created default configuration")
                return True
            else:
                # Validate existing config
                try:
                    with open(self.config_file, 'r') as f:
                        existing_config = json.load(f)
                    
                    is_valid, errors = self.validate_config(existing_config)
                    if not is_valid:
                        self.log_progress(f"Existing configuration has issues: {errors}", "WARNING")
                        # Create backup and recreate
                        backup_file = self.config_file.with_suffix('.json.backup')
                        shutil.copy2(self.config_file, backup_file)
                        self.log_progress(f"Created backup: {backup_file}")
                        
                        # Recreate with default
                        config = self.get_default_config()
                        with open(self.config_file, 'w') as f:
                            json.dump(config, f, indent=2)
                        self.log_progress("✅ Recreated configuration with defaults")
                    else:
                        self.log_progress("✅ Configuration file exists and is valid")
                    
                    return True
                except json.JSONDecodeError as e:
                    self.log_progress(f"Invalid JSON in config file: {e}", "ERROR")
                    # Recreate with default
                    config = self.get_default_config()
                    with open(self.config_file, 'w') as f:
                        json.dump(config, f, indent=2)
                    self.log_progress("✅ Recreated configuration due to JSON error")
                    return True
        except Exception as e:
            self.log_progress(f"Configuration setup failed: {e}", "ERROR")
            return False
    
    def install_dependencies(self) -> Dict[str, bool]:
        """Enhanced dependency installation with multiple fallback mechanisms"""
        self.log_progress("Installing dependencies...")
        
        platform_info = self.detect_platform()
        platform_type = platform_info['type']
        
        results = {}
        
        # System dependencies
        if platform_type in ['colab', 'kaggle']:
            self.log_progress("Installing system dependencies...")
            system_packages = ['git', 'aria2', 'wget', 'curl']
            
            for package in system_packages:
                try:
                    subprocess.run(['apt-get', 'update', '-qq'], check=True, capture_output=True)
                    subprocess.run(['apt-get', 'install', '-y', '-qq', package], check=True, capture_output=True)
                    results[f'system_{package}'] = True
                    self.log_progress(f"✅ System package: {package}")
                except subprocess.CalledProcessError:
                    results[f'system_{package}'] = False
                    self.log_progress(f"⚠️ System package failed: {package}", "WARNING")
        
        # Python packages with fallback mechanisms
        python_packages = {
            'ipywidgets': {'essential': True, 'alternatives': []},
            'requests': {'essential': True, 'alternatives': []},
            'psutil': {'essential': False, 'alternatives': []},
            'tqdm': {'essential': False, 'alternatives': []},
            'torch': {'essential': False, 'alternatives': ['torch-cpu']},
            'Pillow': {'essential': False, 'alternatives': []}
        }
        
        for package, info in python_packages.items():
            installed = False
            
            # Try primary installation
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', package], 
                             check=True, capture_output=True, timeout=60)
                installed = True
                self.log_progress(f"✅ Python package: {package}")
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                self.log_progress(f"⚠️ Primary install failed: {package}", "WARNING")
                
                # Try alternatives
                for alt_package in info['alternatives']:
                    try:
                        subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', alt_package], 
                                     check=True, capture_output=True, timeout=60)
                        installed = True
                        self.log_progress(f"✅ Alternative package: {alt_package} (for {package})")
                        break
                    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                        continue
            
            results[f'python_{package}'] = installed
            
            if not installed and info['essential']:
                self.log_progress(f"❌ Essential package failed: {package}", "ERROR")
        
        # Check specific tools
        tools_to_check = ['git', 'aria2c', 'wget', 'curl']
        for tool in tools_to_check:
            try:
                subprocess.run([tool, '--version'], check=True, capture_output=True, timeout=10)
                results[f'tool_{tool}'] = True
                self.log_progress(f"✅ Tool available: {tool}")
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
                results[f'tool_{tool}'] = False
                self.log_progress(f"❌ Tool not available: {tool}", "WARNING")
        
        return results
    
    def check_aria2c(self) -> bool:
        """Check if aria2c is available and working"""
        try:
            result = subprocess.run(['aria2c', '--version'], check=True, capture_output=True, text=True)
            self.log_progress(f"✅ aria2c available: {result.stdout.strip().split()[0]}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.log_progress("❌ aria2c not available", "WARNING")
            return False
    
    def run_system_diagnostics(self) -> Dict[str, any]:
        """Run comprehensive system diagnostics"""
        self.log_progress("Running system diagnostics...")
        
        diagnostics = {
            'platform': self.detect_platform(),
            'system_resources': self.get_system_resources(),
            'directory_validation': self.validate_directory_structure(),
            'tools_available': {},
            'python_modules': {},
            'recommendations': []
        }
        
        # Check tool availability
        tools = ['git', 'aria2c', 'wget', 'curl', 'python', 'pip']
        for tool in tools:
            try:
                result = subprocess.run([tool, '--version'], check=True, capture_output=True, text=True, timeout=5)
                diagnostics['tools_available'][tool] = {
                    'available': True,
                    'version': result.stdout.strip().split()[0] if result.stdout else 'Unknown'
                }
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
                diagnostics['tools_available'][tool] = {'available': False, 'version': None}
        
        # Check Python modules
        modules = ['torch', 'tensorflow', 'ipywidgets', 'requests', 'psutil', 'tqdm', 'PIL']
        for module in modules:
            try:
                if module == 'PIL':
                    import PIL
                    version = getattr(PIL, '__version__', 'Unknown')
                else:
                    mod = __import__(module)
                    version = getattr(mod, '__version__', 'Unknown')
                diagnostics['python_modules'][module] = {'available': True, 'version': version}
            except ImportError:
                diagnostics['python_modules'][module] = {'available': False, 'version': None}
        
        # Generate recommendations
        if not diagnostics['tools_available']['git']['available']:
            diagnostics['recommendations'].append("Install git for WebUI cloning")
        
        if not diagnostics['tools_available']['aria2c']['available']:
            diagnostics['recommendations'].append("Install aria2c for faster downloads")
        
        if diagnostics['system_resources'].get('memory_total_gb', 0) < 4:
            diagnostics['recommendations'].append("Low memory detected - consider using low VRAM profile")
        
        if diagnostics['system_resources'].get('disk_free_gb', 0) < 10:
            diagnostics['recommendations'].append("Low disk space - ensure sufficient storage for models")
        
        if not diagnostics['python_modules']['torch']['available']:
            diagnostics['recommendations'].append("Install PyTorch for GPU acceleration")
        
        self.log_progress(f"Diagnostics completed with {len(diagnostics['recommendations'])} recommendations")
        return diagnostics
    
    def print_diagnostics_summary(self, diagnostics: Dict[str, any]):
        """Print a user-friendly diagnostics summary"""
        print("\n🔍 System Diagnostics Summary")
        print("=" * 50)
        
        # Platform info
        platform = diagnostics['platform']
        print(f"\n📍 Platform: {platform['name']} ({platform['type']})")
        print(f"   OS: {platform['os']} {platform['architecture']}")
        print(f"   GPU Available: {'✅ Yes' if platform.get('gpu_available') else '❌ No'}")
        
        # System resources
        resources = diagnostics['system_resources']
        if resources:
            print(f"\n💾 System Resources:")
            print(f"   Memory: {resources.get('memory_total_gb', 0):.1f}GB total, {resources.get('memory_available_gb', 0):.1f}GB available")
            print(f"   Disk: {resources.get('disk_total_gb', 0):.1f}GB total, {resources.get('disk_free_gb', 0):.1f}GB free")
            print(f"   CPU: {resources.get('cpu_count', 0)} cores, {resources.get('cpu_percent', 0)}% usage")
        
        # Tools status
        print(f"\n🔧 Tools Status:")
        for tool, info in diagnostics['tools_available'].items():
            status = "✅" if info['available'] else "❌"
            version = f" ({info['version']})" if info['version'] else ""
            print(f"   {status} {tool}{version}")
        
        # Python modules
        print(f"\n📦 Python Modules:")
        for module, info in diagnostics['python_modules'].items():
            status = "✅" if info['available'] else "❌"
            version = f" ({info['version']})" if info['version'] else ""
            print(f"   {status} {module}{version}")
        
        # Directory structure
        print(f"\n📁 Directory Structure:")
        validation = diagnostics['directory_validation']
        valid_count = sum(1 for status in validation.values() if status)
        total_count = len(validation)
        print(f"   {valid_count}/{total_count} directories valid")
        
        # Recommendations
        if diagnostics['recommendations']:
            print(f"\n💡 Recommendations:")
            for i, rec in enumerate(diagnostics['recommendations'], 1):
                print(f"   {i}. {rec}")
        
        print("\n" + "=" * 50)
    
    def setup_environment(self) -> Dict[str, any]:
        """Setup the complete enhanced environment"""
        print("🚀 LSDAI Simplified Enhanced Setup")
        print("=" * 50)
        
        start_time = time.time()
        
        # Phase 1: Platform Detection
        self.log_progress("Phase 1: Platform Detection")
        platform_info = self.detect_platform()
        self.log_progress(f"Platform detected: {platform_info['name']}")
        
        # Phase 2: System Diagnostics
        self.log_progress("Phase 2: System Diagnostics")
        diagnostics = self.run_system_diagnostics()
        
        # Phase 3: Directory Structure
        self.log_progress("Phase 3: Directory Structure Creation")
        dir_success = self.create_directory_structure()
        
        # Phase 4: Configuration Setup
        self.log_progress("Phase 4: Configuration Setup")
        config_success = self.setup_config()
        
        # Phase 5: Dependency Installation
        self.log_progress("Phase 5: Dependency Installation")
        dep_results = self.install_dependencies()
        
        # Phase 6: Final Validation
        self.log_progress("Phase 6: Final Validation")
        aria2c_available = self.check_aria2c()
        
        # Calculate setup time
        setup_time = time.time() - start_time
        
        # Print summary
        print(f"\n🎉 Setup completed in {setup_time:.1f} seconds!")
        print("\n📋 Setup Summary:")
        print(f"  Platform: {platform_info['name']}")
        print(f"  Directory Structure: {'✅ Complete' if dir_success else '❌ Incomplete'}")
        print(f"  Configuration: {'✅ Valid' if config_success else '❌ Invalid'}")
        print(f"  Dependencies: {sum(1 for v in dep_results.values() if v)}/{len(dep_results)} successful")
        print(f"  aria2c: {'✅ Available' if aria2c_available else '❌ Not available'}")
        
        # Print diagnostics if there are issues
        if not dir_success or not config_success or sum(1 for v in dep_results.values() if v) < len(dep_results) * 0.8:
            print("\n⚠️ Setup encountered some issues. See diagnostics below:")
            self.print_diagnostics_summary(diagnostics)
        
        # Save setup log
        log_file = self.project_root / 'logs' / 'setup.log'
        try:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            with open(log_file, 'w') as f:
                f.write(f"LSDAI Setup Log - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n")
                for entry in self.setup_log:
                    f.write(entry + "\n")
            self.log_progress(f"Setup log saved to: {log_file}")
        except Exception as e:
            self.log_progress(f"Failed to save setup log: {e}", "WARNING")
        
        return {
            'platform': platform_info,
            'diagnostics': diagnostics,
            'directory_success': dir_success,
            'config_success': config_success,
            'dependency_results': dep_results,
            'aria2c_available': aria2c_available,
            'setup_time': setup_time,
            'config_file': str(self.config_file),
            'setup_log': self.setup_log
        }

def setup_environment():
    """Main setup function"""
    setup = EnhancedSetup()
    return setup.setup_environment()

def setup_environment_with_progress():
    """Setup function with progress callback example"""
    def progress_callback(message, level):
        # Example progress callback - could be used with ipywidgets
        if level == "ERROR":
            print(f"❌ {message}")
        elif level == "WARNING":
            print(f"⚠️ {message}")
        else:
            print(f"✅ {message}")
    
    setup = EnhancedSetup()
    setup.add_progress_callback(progress_callback)
    return setup.setup_environment()

def quick_setup():
    """Quick setup for advanced users"""
    print("🚀 LSDAI Quick Setup")
    print("=" * 30)
    
    setup = EnhancedSetup()
    
    # Minimal setup - just essentials
    platform_info = setup.detect_platform()
    setup.create_directory_structure()
    setup.setup_config()
    
    # Only install essential dependencies
    essential_packages = ['ipywidgets', 'requests']
    for package in essential_packages:
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', package], 
                         check=True, capture_output=True)
            print(f"✅ {package}")
        except subprocess.CalledProcessError:
            print(f"❌ {package}")
    
    print(f"\n✅ Quick setup complete for {platform_info['name']}")
    return {
        'platform': platform_info,
        'config_file': str(setup.config_file)
    }

if __name__ == "__main__":
    # Run full setup
    result = setup_environment()
    
    # Print final status
    if result['directory_success'] and result['config_success']:
        print("\n🎉 Setup completed successfully!")
        print("You can now run Cell 2 (Widget Configuration)")
    else:
        print("\n⚠️ Setup completed with some issues.")
        print("Check the diagnostics above for details.")
    
    # For debugging, save result to file
    try:
        with open(setup.project_root / 'setup_result.json', 'w') as f:
            # Convert non-serializable objects
            serializable_result = {
                'platform': result['platform'],
                'directory_success': result['directory_success'],
                'config_success': result['config_success'],
                'dependency_results': result['dependency_results'],
                'aria2c_available': result['aria2c_available'],
                'setup_time': result['setup_time'],
                'config_file': result['config_file']
            }
            json.dump(serializable_result, f, indent=2)
        print(f"Setup results saved to: {setup.project_root / 'setup_result.json'}")
    except Exception as e:
        print(f"Could not save setup results: {e}")