#!/usr/bin/env python3
"""
LSDAI Simplified WebUI Launcher
Simple WebUI launcher with sequential execution
"""

import os
import sys
import signal
import subprocess
import threading
import time
from pathlib import Path
from typing import Dict, Any, Optional, List

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'modules'))

try:
    import ipywidgets as widgets
    from IPython.display import display, HTML
    HAS_IPYWIDGETS = True
except ImportError:
    HAS_IPYWIDGETS = False

from config import get_config_manager
from webui_manager import get_webui_manager
from hardware_optimizer import get_hardware_optimizer

class SimpleLauncher:
    """Simple WebUI launcher with sequential execution"""
    
    def __init__(self):
        self.config_manager = get_config_manager()
        self.webui_manager = get_webui_manager()
        self.hardware_optimizer = get_hardware_optimizer()
        
        self.launch_process = None
        self.launch_thread = None
        self.launch_output = []
        self.is_launching = False
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\n⚠️  Received signal {signum}, stopping WebUI...")
        self.stop_webui()
        sys.exit(0)
    
    def launch_webui(self, webui_type: str, extra_args: str = "") -> bool:
        """Launch a WebUI with hardware optimization"""
        if self.is_launching:
            print("❌ Another WebUI is already being launched")
            return False
        
        if not self.webui_manager.is_webui_installed(webui_type):
            print(f"❌ {webui_type} is not installed")
            return False
        
        if self.webui_manager.is_webui_running():
            running_webui = self.webui_manager.get_running_webui()
            print(f"❌ {running_webui} is already running. Stop it first.")
            return False
        
        print(f"🚀 Preparing to launch {webui_type}...")
        
        # Get hardware optimization
        hardware_profile = self.hardware_optimizer.get_optimization_profile(webui_type)
        optimization_args = hardware_profile['args']
        
        # Combine with user arguments
        user_args = extra_args.split() if extra_args else []
        all_args = optimization_args + user_args
        
        print(f"🔧 Using profile: {hardware_profile['profile_name']}")
        print(f"🔧 Arguments: {' '.join(all_args)}")
        
        # Launch in separate thread to avoid blocking
        self.launch_thread = threading.Thread(
            target=self._launch_webui_thread,
            args=(webui_type, all_args)
        )
        self.launch_thread.start()
        
        return True
    
    def _launch_webui_thread(self, webui_type: str, args: List[str]):
        """Launch WebUI in a separate thread"""
        self.is_launching = True
        self.launch_output = []
        
        try:
            webui_info = self.webui_manager.get_webui_info(webui_type)
            webui_path = self.webui_manager.get_webui_path(webui_type)
            launch_script = webui_info['launch_script']
            
            print(f"🚀 Launching {webui_info['name']}...")
            
            # Change to WebUI directory
            original_cwd = os.getcwd()
            os.chdir(webui_path)
            
            # Build command
            cmd = ['python3', launch_script] + args
            
            # Add --share for cloud environments
            if self.webui_manager.is_cloud_environment():
                cmd.append('--share')
            
            print(f"📝 Command: {' '.join(cmd)}")
            print("-" * 50)
            
            # Start process
            self.launch_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Set running WebUI
            self.webui_manager.running_webui = webui_type
            
            # Monitor output
            self._monitor_launch_output()
            
        except Exception as e:
            print(f"❌ Launch failed: {e}")
            self.is_launching = False
            os.chdir(original_cwd)
    
    def _monitor_launch_output(self):
        """Monitor WebUI launch output"""
        if not self.launch_process:
            return
        
        try:
            for line in iter(self.launch_process.stdout.readline, ''):
                line = line.strip()
                if line:
                    self.launch_output.append(line)
                    print(line)
                    
                    # Check for URLs
                    if 'running on local url:' in line.lower():
                        print(f"🎉 Local URL: {line.split('running on local url:')[-1].strip()}")
                    elif 'running on public url:' in line.lower():
                        print(f"🌐 Public URL: {line.split('running on public url:')[-1].strip()}")
                    elif 'error' in line.lower() or 'failed' in line.lower():
                        print(f"⚠️  Error detected: {line}")
            
            # Process finished
            return_code = self.launch_process.wait()
            print(f"\n📋 WebUI process ended with return code: {return_code}")
            
        except Exception as e:
            print(f"❌ Error monitoring output: {e}")
        finally:
            self.is_launching = False
            self.webui_manager.running_webui = None
            self.launch_process = None
    
    def stop_webui(self) -> bool:
        """Stop the currently running WebUI"""
        if not self.is_launching and not self.webui_manager.is_webui_running():
            print("❌ No WebUI is currently running")
            return False
        
        print("⏹️ Stopping WebUI...")
        
        try:
            # Stop through webui_manager
            success = self.webui_manager.stop_webui()
            
            # If that fails, try to kill the process directly
            if self.launch_process:
                self.launch_process.terminate()
                try:
                    self.launch_process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    self.launch_process.kill()
                
                self.launch_process = None
            
            self.is_launching = False
            print("✅ WebUI stopped")
            return True
            
        except Exception as e:
            print(f"❌ Error stopping WebUI: {e}")
            return False
    
    def get_launch_status(self) -> Dict[str, Any]:
        """Get current launch status"""
        return {
            'is_launching': self.is_launching,
            'running_webui': self.webui_manager.get_running_webui(),
            'launch_output_lines': len(self.launch_output),
            'process_active': self.launch_process is not None
        }
    
    def create_launcher_interface(self):
        """Create launcher interface with widgets"""
        if not HAS_IPYWIDGETS:
            print("❌ ipywidgets is required for launcher interface")
            return None
        
        # WebUI selection
        webui_options = self.webui_manager.get_supported_webuis()
        selected_webui = self.config_manager.get('webui.selected', 'forge')
        
        webui_dropdown = widgets.Dropdown(
            options=webui_options,
            value=selected_webui,
            description='WebUI:',
            style={'description_width': 'initial'}
        )
        
        # Custom arguments
        args_input = widgets.Text(
            value=self.config_manager.get('webui.launch_args', ''),
            placeholder='Additional launch arguments...',
            description='Args:',
            style={'description_width': 'initial'}
        )
        
        # Launch button
        launch_btn = widgets.Button(
            description="🚀 Launch",
            button_style='success',
            layout=widgets.Layout(width='120px')
        )
        
        # Stop button
        stop_btn = widgets.Button(
            description="⏹️ Stop",
            button_style='danger',
            layout=widgets.Layout(width='120px')
        )
        
        # Status display
        status_display = widgets.HTML(value=self._get_status_html())
        
        # Output area
        output_area = widgets.Output(layout={'border': '1px solid #ccc', 'height': '300px', 'overflow_y': 'auto'})
        
        # Connect event handlers
        webui_dropdown.observe(self._on_webui_change, names='value')
        args_input.observe(self._on_args_change, names='value')
        launch_btn.on_click(self._on_launch_click)
        stop_btn.on_click(self._on_stop_click)
        
        # Store widgets
        self.launcher_widgets = {
            'webui_dropdown': webui_dropdown,
            'args_input': args_input,
            'launch_btn': launch_btn,
            'stop_btn': stop_btn,
            'status_display': status_display,
            'output_area': output_area
        }
        
        # Layout
        controls = widgets.HBox([webui_dropdown, args_input, launch_btn, stop_btn])
        return widgets.VBox([controls, status_display, output_area])
    
    def _get_status_html(self) -> str:
        """Get HTML status display"""
        status = self.get_launch_status()
        
        if status['is_launching']:
            return """
            <div style="padding: 10px; background-color: #fff3cd; border-radius: 5px; border-left: 4px solid #ffc107;">
                <strong>🟡 Launching WebUI...</strong>
            </div>
            """
        elif status['running_webui']:
            return f"""
            <div style="padding: 10px; background-color: #d4edda; border-radius: 5px; border-left: 4px solid #28a745;">
                <strong>🟢 {status['running_webui']} is running</strong>
            </div>
            """
        else:
            return """
            <div style="padding: 10px; background-color: #f8d7da; border-radius: 5px; border-left: 4px solid #dc3545;">
                <strong>🔴 No WebUI is running</strong>
            </div>
            """
    
    def _update_output_display(self):
        """Update the output display"""
        if hasattr(self, 'launcher_widgets') and 'output_area' in self.launcher_widgets:
            with self.launcher_widgets['output_area']:
                self.launcher_widgets['output_area'].clear_output()
                for line in self.launch_output[-20:]:  # Show last 20 lines
                    print(line)
    
    # Event handlers
    def _on_webui_change(self, change):
        """Handle WebUI selection change"""
        self.config_manager.set_webui_selection(change['new'])
    
    def _on_args_change(self, change):
        """Handle arguments change"""
        self.config_manager.set_webui_args(change['new'])
    
    def _on_launch_click(self, b):
        """Handle launch button click"""
        webui_type = self.launcher_widgets['webui_dropdown'].value
        extra_args = self.launcher_widgets['args_input'].value
        
        success = self.launch_webui(webui_type, extra_args)
        if success:
            self.launcher_widgets['status_display'].value = self._get_status_html()
            
            # Start output monitoring
            def monitor_output():
                while self.is_launching:
                    self._update_output_display()
                    time.sleep(1)
            
            threading.Thread(target=monitor_output, daemon=True).start()
    
    def _on_stop_click(self, b):
        """Handle stop button click"""
        success = self.stop_webui()
        if success:
            self.launcher_widgets['status_display'].value = self._get_status_html()
            self._update_output_display()

# Global launcher instance
_launcher = None

def get_launcher():
    """Get global launcher instance"""
    global _launcher
    if _launcher is None:
        _launcher = SimpleLauncher()
    return _launcher

if __name__ == "__main__":
    # Test the launcher
    launcher = get_launcher()
    status = launcher.get_launch_status()
    print(f"Launcher status: {status}")