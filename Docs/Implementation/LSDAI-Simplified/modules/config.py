#!/usr/bin/env python3
"""
LSDAI Simplified Configuration Management
Simple JSON-based configuration (no complex ODM)
"""

import json
import os
from pathlib import Path

class ConfigManager:
    """Simple configuration manager using JSON"""
    
    def __init__(self, config_file=None):
        if config_file is None:
            # Default config file location
            self.project_root = Path.cwd() / 'LSDAI-Simplified'
            self.config_file = self.project_root / 'config.json'
        else:
            self.config_file = Path(config_file)
        
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from JSON file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            else:
                return self.get_default_config()
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"⚠️  Could not load config: {e}")
            return self.get_default_config()
    
    def get_default_config(self):
        """Get default configuration structure"""
        return {
            "environment": {
                "platform": "local",
                "base_path": str(Path.cwd() / 'LSDAI-Simplified')
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
            "verbosity": "pretty",
            "hardware": {
                "optimization_profile": "auto"
            }
        }
    
    def save_config(self):
        """Save configuration to JSON file"""
        try:
            # Ensure directory exists
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"❌ Could not save config: {e}")
            return False
    
    def get(self, key, default=None):
        """Get configuration value using dot notation"""
        keys = key.split('.')
        current = self.config
        
        try:
            for k in keys:
                current = current[k]
            return current
        except (KeyError, TypeError):
            return default
    
    def set(self, key, value):
        """Set configuration value using dot notation"""
        keys = key.split('.')
        current = self.config
        
        # Navigate to parent of the target key
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        # Set the value
        current[keys[-1]] = value
        
        # Save the configuration
        return self.save_config()
    
    def update(self, updates):
        """Update multiple configuration values"""
        for key, value in updates.items():
            self.set(key, value)
        return True
    
    def get_webui_config(self):
        """Get WebUI configuration"""
        return self.get('webui', {})
    
    def get_models_config(self):
        """Get models configuration"""
        return self.get('models', {})
    
    def get_hardware_config(self):
        """Get hardware configuration"""
        return self.get('hardware', {})
    
    def get_verbosity(self):
        """Get verbosity setting"""
        return self.get('verbosity', 'pretty')
    
    def set_webui_selection(self, webui_type):
        """Set selected WebUI"""
        return self.set('webui.selected', webui_type)
    
    def set_webui_args(self, args):
        """Set WebUI launch arguments"""
        return self.set('webui.launch_args', args)
    
    def set_model_selections(self, sd15_models=None, sdxl_models=None, text_input=None):
        """Set model selections"""
        updates = {}
        if sd15_models is not None:
            updates['models.selected_sd15'] = sd15_models
        if sdxl_models is not None:
            updates['models.selected_sdxl'] = sdxl_models
        if text_input is not None:
            updates['models.text_input'] = text_input
        
        return self.update(updates)
    
    def set_verbosity(self, verbosity):
        """Set verbosity level"""
        if verbosity in ['pretty', 'raw']:
            return self.set('verbosity', verbosity)
        return False
    
    def set_hardware_profile(self, profile):
        """Set hardware optimization profile"""
        return self.set('hardware.optimization_profile', profile)

# Global configuration instance
_config_manager = None

def get_config_manager():
    """Get global configuration manager instance"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager

def load_config():
    """Load configuration (convenience function)"""
    return get_config_manager().load_config()

def save_config(config):
    """Save configuration (convenience function)"""
    get_config_manager().config = config
    return get_config_manager().save_config()

def get_config(key, default=None):
    """Get configuration value (convenience function)"""
    return get_config_manager().get(key, default)

def set_config(key, value):
    """Set configuration value (convenience function)"""
    return get_config_manager().set(key, value)

def update_config(updates):
    """Update multiple configuration values (convenience function)"""
    return get_config_manager().update(updates)