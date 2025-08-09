#!/usr/bin/env python3
"""
LSDAI Simplified Download System
Simple download management with aria2c and progress tracking
"""

import os
import sys
import subprocess
import threading
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable
from urllib.parse import urlparse

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'modules'))

try:
    import ipywidgets as widgets
    from IPython.display import display, HTML
    HAS_IPYWIDGETS = True
except ImportError:
    HAS_IPYWIDGETS = False

from config import get_config_manager
from model_parser import get_model_parser

class SimpleDownloader:
    """Simple download manager with aria2c"""
    
    def __init__(self):
        self.config_manager = get_config_manager()
        self.model_parser = get_model_parser()
        self.project_root = Path.cwd() / 'LSDAI-Simplified'
        self.downloads_path = self.project_root / 'downloads'
        
        self.active_downloads = {}
        self.download_threads = {}
        self.progress_widgets = {}
        
        # Ensure downloads directory exists
        self.downloads_path.mkdir(parents=True, exist_ok=True)
        
        # Check if aria2c is available
        self.aria2c_available = self._check_aria2c()
    
    def _check_aria2c(self) -> bool:
        """Check if aria2c is available"""
        try:
            subprocess.run(['aria2c', '--version'], check=True, capture_output=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def download_model(self, model_info: Dict[str, Any], progress_callback: Optional[Callable] = None) -> bool:
        """Download a single model"""
        url = model_info['url']
        filename = model_info['filename']
        target_path = model_info.get('target_path', self.downloads_path / filename)
        
        # Ensure target directory exists
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"📥 Downloading: {filename}")
        
        # Try different download methods
        methods = []
        
        if self.aria2c_available:
            methods.append(self._download_with_aria2c)
        
        methods.extend([
            self._download_with_wget,
            self._download_with_curl,
            self._download_with_python
        ])
        
        for method in methods:
            try:
                success = method(url, target_path, progress_callback)
                if success:
                    print(f"✅ Downloaded: {filename}")
                    return True
                else:
                    print(f"⚠️  {method.__name__} failed for {filename}")
            except Exception as e:
                print(f"❌ {method.__name__} error for {filename}: {e}")
        
        print(f"❌ Failed to download: {filename}")
        return False
    
    def _download_with_aria2c(self, url: str, target_path: Path, progress_callback: Optional[Callable] = None) -> bool:
        """Download using aria2c"""
        try:
            cmd = [
                'aria2c',
                '--continue=true',
                '--max-tries=3',
                '--split=4',
                '--max-connection-per-server=4',
                '--min-split-size=1M',
                '--user-agent=Mozilla/5.0',
                '--file-allocation=none',
                '--summary-interval=1',
                '--stop-with-process=exit',
                '--dir', str(target_path.parent),
                '--out', target_path.name,
                url
            ]
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Monitor progress
            total_size = 0
            downloaded = 0
            
            for line in iter(process.stdout.readline, ''):
                line = line.strip()
                if line and progress_callback:
                    # Parse aria2c progress output
                    if '(' in line and ')' in line:
                        try:
                            progress_part = line.split('(')[1].split(')')[0]
                            if '%' in progress_part:
                                progress = float(progress_part.split('%')[0])
                                progress_callback(progress)
                        except:
                            pass
            
            process.wait()
            return process.returncode == 0 and target_path.exists()
            
        except Exception:
            return False
    
    def _download_with_wget(self, url: str, target_path: Path, progress_callback: Optional[Callable] = None) -> bool:
        """Download using wget"""
        try:
            cmd = [
                'wget',
                '--continue',
                '--tries=3',
                '--user-agent=Mozilla/5.0',
                '--output-document', str(target_path),
                url
            ]
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Monitor progress
            for line in iter(process.stdout.readline, ''):
                line = line.strip()
                if line and progress_callback and '%' in line:
                    try:
                        progress = float(line.split('%')[0].split()[-1])
                        progress_callback(progress)
                    except:
                        pass
            
            process.wait()
            return process.returncode == 0 and target_path.exists()
            
        except Exception:
            return False
    
    def _download_with_curl(self, url: str, target_path: Path, progress_callback: Optional[Callable] = None) -> bool:
        """Download using curl"""
        try:
            cmd = [
                'curl',
                '--continue-at', '-',
                '--retry', '3',
                '--user-agent', 'Mozilla/5.0',
                '--output', str(target_path),
                '--location',  # Follow redirects
                url
            ]
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Monitor progress
            for line in iter(process.stdout.readline, ''):
                line = line.strip()
                if line and progress_callback:
                    # Parse curl progress
                    if '%' in line and 'DL' in line:
                        try:
                            progress = float(line.split('%')[0].split()[-1])
                            progress_callback(progress)
                        except:
                            pass
            
            process.wait()
            return process.returncode == 0 and target_path.exists()
            
        except Exception:
            return False
    
    def _download_with_python(self, url: str, target_path: Path, progress_callback: Optional[Callable] = None) -> bool:
        """Download using Python requests"""
        try:
            import requests
            
            # Handle large file downloads with streaming
            with requests.get(url, stream=True, headers={'User-Agent': 'Mozilla/5.0'}) as r:
                r.raise_for_status()
                
                total_size = int(r.headers.get('content-length', 0))
                downloaded = 0
                
                with open(target_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            if progress_callback and total_size > 0:
                                progress = (downloaded / total_size) * 100
                                progress_callback(progress)
                
                return True
                
        except Exception:
            return False
    
    def download_models_from_text(self, text_input: str) -> Dict[str, Any]:
        """Download models parsed from text input"""
        if not text_input.strip():
            return {'success': False, 'message': 'No text input provided'}
        
        try:
            # Parse models
            models = self.model_parser.parse_text_input(text_input)
            validation = self.model_parser.validate_models(models)
            
            if not validation['valid']:
                return {
                    'success': False,
                    'message': f'Validation errors: {", ".join(validation["errors"])}'
                }
            
            # Get download list
            download_list = self.model_parser.get_download_list(models)
            
            if not download_list:
                return {'success': False, 'message': 'No valid models found'}
            
            print(f"📋 Found {len(download_list)} models to download")
            
            # Download each model
            results = {
                'success': True,
                'downloaded': [],
                'failed': [],
                'total': len(download_list)
            }
            
            for model in download_list:
                if HAS_IPYWIDGETS:
                    # Create progress widget
                    progress_bar = widgets.FloatProgress(
                        value=0.0,
                        min=0.0,
                        max=100.0,
                        description=f"Downloading {model['name']}:",
                        bar_style='info',
                        layout=widgets.Layout(width='500px')
                    )
                    status_label = widgets.Label(value="Starting...")
                    
                    display(widgets.VBox([progress_bar, status_label]))
                    
                    def progress_callback(progress):
                        progress_bar.value = progress
                        status_label.value = f"{progress:.1f}%"
                    
                    success = self.download_model(model, progress_callback)
                    
                    if success:
                        progress_bar.bar_style = 'success'
                        status_label.value = "✅ Completed"
                        results['downloaded'].append(model['name'])
                    else:
                        progress_bar.bar_style = 'danger'
                        status_label.value = "❌ Failed"
                        results['failed'].append(model['name'])
                else:
                    # Simple text-based progress
                    def progress_callback(progress):
                        print(f"  {model['name']}: {progress:.1f}%")
                    
                    success = self.download_model(model, progress_callback)
                    
                    if success:
                        results['downloaded'].append(model['name'])
                    else:
                        results['failed'].append(model['name'])
            
            # Summary
            summary = f"Download completed: {len(results['downloaded'])} successful, {len(results['failed'])} failed"
            print(f"\n📊 {summary}")
            
            results['message'] = summary
            return results
            
        except Exception as e:
            return {'success': False, 'message': f'Error during download: {e}'}
    
    def get_download_status(self) -> Dict[str, Any]:
        """Get current download status"""
        return {
            'active_downloads': len(self.active_downloads),
            'aria2c_available': self.aria2c_available,
            'downloads_path': str(self.downloads_path)
        }
    
    def print_download_status(self):
        """Print download status information"""
        status = self.get_download_status()
        
        print("📥 Download System Status")
        print("=" * 30)
        print(f"Active downloads: {status['active_downloads']}")
        print(f"aria2c available: {'✅ Yes' if status['aria2c_available'] else '❌ No'}")
        print(f"Downloads path: {status['downloads_path']}")

# Global downloader instance
_downloader = None

def get_downloader():
    """Get global downloader instance"""
    global _downloader
    if _downloader is None:
        _downloader = SimpleDownloader()
    return _downloader

if __name__ == "__main__":
    # Test the downloader
    downloader = get_downloader()
    downloader.print_download_status()