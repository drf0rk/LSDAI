#!/usr/bin/env python3
"""
LSDAI Simplified WebUI Manager
Multi-WebUI support with simplified management
"""

import os
import subprocess
import signal
from pathlib import Path
from typing import Dict, Optional, List

class WebUIManager:
    """Simple WebUI manager for multiple Stable Diffusion WebUIs"""
    
    def __init__(self):
        self.supported_webuis = {
            'forge': {
                'name': 'Stable Diffusion WebUI Forge',
                'repo': 'https://github.com/lllyasviel/stable-diffusion-webui-forge.git',
                'install_script': 'install_forge.py',
                'launch_args': '--xformers --cuda-stream',
                'launch_script': 'launch.py'
            },
            'a1111': {
                'name': 'AUTOMATIC1111 WebUI',
                'repo': 'https://github.com/AUTOMATIC1111/stable-diffusion-webui.git',
                'install_script': 'install_a1111.py',
                'launch_args': '--xformers --no-half-vae',
                'launch_script': 'launch.py'
            },
            'comfyui': {
                'name': 'ComfyUI',
                'repo': 'https://github.com/comfyanonymous/ComfyUI.git',
                'install_script': 'install_comfyui.py',
                'launch_args': '--dont-print-server',
                'launch_script': 'main.py'
            },
            'fooocus': {
                'name': 'Fooocus',
                'repo': 'https://github.com/lllyasviel/Fooocus.git',
                'install_script': 'install_fooocus.py',
                'launch_args': '--preset anime',
                'launch_script': 'entry_with_update.py'
            }
        }
        
        self.running_webui = None
        self.webui_process = None
        self.project_root = Path.cwd() / 'LSDAI-Simplified'
        self.installations_path = self.project_root / 'webui_installations'
    
    def get_supported_webuis(self) -> List[str]:
        """Get list of supported WebUI types"""
        return list(self.supported_webuis.keys())
    
    def get_webui_info(self, webui_type: str) -> Dict:
        """Get information about a specific WebUI"""
        return self.supported_webuis.get(webui_type, {})
    
    def get_webui_path(self, webui_type: str) -> Path:
        """Get installation path for a WebUI"""
        return self.installations_path / webui_type
    
    def is_webui_installed(self, webui_type: str) -> bool:
        """Check if a WebUI is installed"""
        webui_path = self.get_webui_path(webui_type)
        launch_script = webui_path / self.supported_webuis[webui_type]['launch_script']
        return webui_path.exists() and launch_script.exists()
    
    def install_webui(self, webui_type: str) -> bool:
        """Install a WebUI"""
        if webui_type not in self.supported_webuis:
            print(f"❌ Unsupported WebUI: {webui_type}")
            return False
        
        webui_info = self.supported_webuis[webui_type]
        webui_path = self.get_webui_path(webui_type)
        
        print(f"📥 Installing {webui_info['name']}...")
        
        try:
            # Create installations directory
            self.installations_path.mkdir(parents=True, exist_ok=True)
            
            # Clone repository
            if not webui_path.exists():
                subprocess.run([
                    'git', 'clone', webui_info['repo'], str(webui_path)
                ], check=True, capture_output=True)
                print(f"  ✅ Cloned repository")
            else:
                print(f"  ✅ Repository already exists")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Installation failed: {e}")
            return False
    
    def get_launch_command(self, webui_type: str, extra_args: str = "") -> List[str]:
        """Get launch command for a WebUI"""
        if webui_type not in self.supported_webuis:
            return []
        
        webui_info = self.supported_webuis[webui_type]
        webui_path = self.get_webui_path(webui_type)
        launch_script = webui_info['launch_script']
        
        # Use system Python
        python_exe = 'python3'
        
        # Build command
        cmd = [python_exe, launch_script]
        
        # Add default arguments
        if webui_info['launch_args']:
            cmd.extend(webui_info['launch_args'].split())
        
        # Add extra arguments
        if extra_args:
            cmd.extend(extra_args.split())
        
        # Add --share for cloud environments
        if self.is_cloud_environment():
            cmd.append('--share')
        
        return cmd
    
    def is_cloud_environment(self) -> bool:
        """Check if running in cloud environment"""
        return 'COLAB_GPU' in os.environ or 'KAGGLE_KERNEL_RUN_TYPE' in os.environ
    
    def launch_webui(self, webui_type: str, extra_args: str = "") -> bool:
        """Launch a WebUI"""
        if self.running_webui:
            print(f"❌ Another WebUI ({self.running_webui}) is already running")
            return False
        
        if not self.is_webui_installed(webui_type):
            print(f"❌ {webui_type} is not installed")
            return False
        
        webui_info = self.supported_webuis[webui_type]
        webui_path = self.get_webui_path(webui_type)
        
        print(f"🚀 Launching {webui_info['name']}...")
        
        try:
            # Change to WebUI directory
            original_cwd = os.getcwd()
            os.chdir(webui_path)
            
            # Get launch command
            cmd = self.get_launch_command(webui_type, extra_args)
            
            if not cmd:
                print(f"❌ Could not create launch command for {webui_type}")
                return False
            
            # Start process
            self.webui_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            self.running_webui = webui_type
            print(f"✅ {webui_info['name']} launched successfully!")
            
            # Start monitoring output
            self._monitor_webui_output()
            
            return True
            
        except Exception as e:
            print(f"❌ Launch failed: {e}")
            os.chdir(original_cwd)
            return False
    
    def _monitor_webui_output(self):
        """Monitor WebUI output for URLs and errors"""
        if not self.webui_process:
            return
        
        print("📝 Monitoring output for URLs...")
        print("-" * 40)
        
        try:
            for line in iter(self.webui_process.stdout.readline, ''):
                line = line.strip()
                if line:
                    print(line)
                    
                    # Check for URLs
                    if 'running on local url:' in line.lower():
                        print(f"🎉 Local URL found: {line}")
                    elif 'running on public url:' in line.lower():
                        print(f"🌐 Public URL found: {line}")
                    
        except KeyboardInterrupt:
            print("\n⏹️ Monitoring stopped")
        except Exception as e:
            print(f"❌ Monitoring error: {e}")
    
    def stop_webui(self) -> bool:
        """Stop the currently running WebUI"""
        if not self.running_webui:
            print("❌ No WebUI is currently running")
            return False
        
        webui_type = self.running_webui
        webui_info = self.supported_webuis[webui_type]
        
        print(f"⏹️ Stopping {webui_info['name']}...")
        
        try:
            if self.webui_process:
                self.webui_process.terminate()
                try:
                    self.webui_process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    self.webui_process.kill()
                
                self.webui_process = None
            
            self.running_webui = None
            print(f"✅ {webui_info['name']} stopped")
            return True
            
        except Exception as e:
            print(f"❌ Error stopping WebUI: {e}")
            return False
    
    def get_running_webui(self) -> Optional[str]:
        """Get the currently running WebUI type"""
        return self.running_webui
    
    def is_webui_running(self) -> bool:
        """Check if any WebUI is currently running"""
        return self.running_webui is not None
    
    def get_installation_status(self) -> Dict[str, bool]:
        """Get installation status for all WebUIs"""
        status = {}
        for webui_type in self.supported_webuis:
            status[webui_type] = self.is_webui_installed(webui_type)
        return status
    
    def setup_shared_model_storage(self) -> bool:
        """Setup shared model storage with symlinks"""
        print("🔗 Setting up shared model storage...")
        
        shared_paths = {
            'models': 'shared_models/Stable-diffusion',
            'vae': 'shared_models/VAE',
            'lora': 'shared_models/Lora',
            'controlnet': 'shared_models/ControlNet',
            'embeddings': 'shared_models/embeddings'
        }
        
        success = True
        
        for webui_type in self.supported_webuis:
            webui_path = self.get_webui_path(webui_type)
            
            if not webui_path.exists():
                continue
            
            print(f"  🔗 Setting up symlinks for {webui_type}...")
            
            for model_type, shared_path in shared_paths.items():
                source = self.project_root / shared_path
                target = webui_path / 'models' / model_type
                
                try:
                    # Create target directory if it doesn't exist
                    target.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Remove existing directory/file if it exists
                    if target.exists():
                        if target.is_dir():
                            shutil.rmtree(target)
                        else:
                            target.unlink()
                    
                    # Create symlink
                    target.symlink_to(source)
                    print(f"    ✅ {model_type} -> {shared_path}")
                    
                except Exception as e:
                    print(f"    ❌ Failed to create symlink for {model_type}: {e}")
                    success = False
        
        return success

# Global WebUI manager instance
_webui_manager = None

def get_webui_manager():
    """Get global WebUI manager instance"""
    global _webui_manager
    if _webui_manager is None:
        _webui_manager = WebUIManager()
    return _webui_manager