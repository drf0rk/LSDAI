#!/usr/bin/env python3
"""
LSDAI Simplified Hardware Optimizer
Profile-based hardware optimization (no AI in notebook)
"""

import os
import subprocess
from typing import Dict, Any, List

class SimpleHardwareOptimizer:
    """Simple hardware optimization with predefined profiles"""
    
    def __init__(self):
        self.profiles = self._load_profiles()
    
    def _load_profiles(self) -> Dict[str, Dict[str, Any]]:
        """Load hardware optimization profiles"""
        return {
            'low_vram': {
                'conditions': {'vram_gb': '<=4'},
                'args': ['--medvram', '--lowvram'],
                'batch_size': 1,
                'description': 'Low VRAM (<=4GB)'
            },
            'medium_vram': {
                'conditions': {'vram_gb': '<=8'},
                'args': ['--medvram'],
                'batch_size': 2,
                'description': 'Medium VRAM (<=8GB)'
            },
            'high_vram': {
                'conditions': {'vram_gb': '>8'},
                'args': ['--xformers'],
                'batch_size': 4,
                'description': 'High VRAM (>8GB)'
            },
            'cpu_only': {
                'conditions': {'gpu': False},
                'args': ['--cpu'],
                'batch_size': 1,
                'description': 'CPU only'
            }
        }
    
    def detect_hardware(self) -> Dict[str, Any]:
        """Detect hardware capabilities"""
        hardware_info = {
            'gpu': False,
            'vram_gb': 0,
            'gpu_name': 'Unknown',
            'cpu_cores': os.cpu_count() or 1,
            'ram_gb': self._get_system_ram()
        }
        
        # Try to detect GPU using nvidia-smi
        try:
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=name,memory.total', '--format=csv,noheader,nounits'],
                capture_output=True, text=True, check=True
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if lines:
                    # Parse GPU info
                    gpu_info = lines[0].split(', ')
                    if len(gpu_info) >= 2:
                        hardware_info['gpu'] = True
                        hardware_info['gpu_name'] = gpu_info[0].strip()
                        hardware_info['vram_gb'] = float(gpu_info[1].strip())
                        
        except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
            # nvidia-smi not available or failed, try with torch
            pass
        
        # Fallback: Try with torch if available
        if not hardware_info['gpu']:
            try:
                import torch
                if torch.cuda.is_available():
                    hardware_info['gpu'] = True
                    hardware_info['vram_gb'] = torch.cuda.get_device_properties(0).total_memory / 1e9
                    hardware_info['gpu_name'] = torch.cuda.get_device_name(0)
            except ImportError:
                pass
        
        return hardware_info
    
    def _get_system_ram(self) -> float:
        """Get system RAM in GB"""
        try:
            if os.name == 'posix':  # Linux/macOS
                with open('/proc/meminfo', 'r') as f:
                    for line in f:
                        if line.startswith('MemTotal:'):
                            return int(line.split()[1]) / (1024 * 1024)  # Convert to GB
            elif os.name == 'nt':  # Windows
                import ctypes
                kernel32 = ctypes.windll.kernel32
                class MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ('dwLength', ctypes.c_ulong),
                        ('dwMemoryLoad', ctypes.c_ulong),
                        ('ullTotalPhys', ctypes.c_ulonglong),
                        ('ullAvailPhys', ctypes.c_ulonglong),
                        ('ullTotalPageFile', ctypes.c_ulonglong),
                        ('ullAvailPageFile', ctypes.c_ulonglong),
                        ('ullTotalVirtual', ctypes.c_ulonglong),
                        ('ullAvailVirtual', ctypes.c_ulonglong),
                        ('ullAvailExtendedVirtual', ctypes.c_ulonglong),
                    ]
                memory_status = MEMORYSTATUSEX()
                memory_status.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
                kernel32.GlobalMemoryStatusEx(ctypes.byref(memory_status))
                return memory_status.ullTotalPhys / (1024**3)  # Convert to GB
        except:
            pass
        
        return 8.0  # Default fallback
    
    def get_optimization_profile(self, webui_type: str = None) -> Dict[str, Any]:
        """Get optimization profile based on hardware detection"""
        hardware = self.detect_hardware()
        
        # Find matching profile
        for profile_name, profile in self.profiles.items():
            conditions = profile['conditions']
            match = True
            
            if 'vram_gb' in conditions:
                condition = conditions['vram_gb']
                if condition.startswith('<='):
                    threshold = float(condition[2:])
                    if hardware['vram_gb'] > threshold:
                        match = False
                elif condition.startswith('>'):
                    threshold = float(condition[1:])
                    if hardware['vram_gb'] <= threshold:
                        match = False
            
            if 'gpu' in conditions:
                if hardware['gpu'] != conditions['gpu']:
                    match = False
            
            if match:
                return {
                    'profile_name': profile_name,
                    'description': profile['description'],
                    'args': profile['args'],
                    'batch_size': profile['batch_size'],
                    'hardware': hardware
                }
        
        # Default fallback
        return {
            'profile_name': 'medium_vram',
            'description': self.profiles['medium_vram']['description'],
            'args': self.profiles['medium_vram']['args'],
            'batch_size': self.profiles['medium_vram']['batch_size'],
            'hardware': hardware
        }
    
    def get_optimization_args(self, webui_type: str = None) -> List[str]:
        """Get optimization arguments for WebUI launch"""
        profile = self.get_optimization_profile(webui_type)
        return profile['args']
    
    def get_hardware_info(self) -> Dict[str, Any]:
        """Get detailed hardware information"""
        hardware = self.detect_hardware()
        profile = self.get_optimization_profile()
        
        return {
            'hardware': hardware,
            'selected_profile': profile['profile_name'],
            'profile_description': profile['description'],
            'optimization_args': profile['args'],
            'recommended_batch_size': profile['batch_size']
        }
    
    def print_hardware_info(self):
        """Print hardware information in a user-friendly format"""
        info = self.get_hardware_info()
        hardware = info['hardware']
        
        print("🔧 Hardware Detection Results")
        print("=" * 40)
        print(f"💻 GPU: {'✅ Available' if hardware['gpu'] else '❌ Not available'}")
        
        if hardware['gpu']:
            print(f"🎮 GPU Name: {hardware['gpu_name']}")
            print(f"🧠 VRAM: {hardware['vram_gb']:.1f} GB")
        
        print(f"⚡ CPU Cores: {hardware['cpu_cores']}")
        print(f"🧾 System RAM: {hardware['ram_gb']:.1f} GB")
        print()
        print("🎯 Optimization Profile")
        print("-" * 20)
        print(f"Profile: {info['selected_profile']}")
        print(f"Description: {info['profile_description']}")
        print(f"Arguments: {' '.join(info['optimization_args'])}")
        print(f"Recommended Batch Size: {info['recommended_batch_size']}")

# Global hardware optimizer instance
_hardware_optimizer = None

def get_hardware_optimizer():
    """Get global hardware optimizer instance"""
    global _hardware_optimizer
    if _hardware_optimizer is None:
        _hardware_optimizer = SimpleHardwareOptimizer()
    return _hardware_optimizer