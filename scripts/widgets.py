#!/usr/bin/env python3
"""
LSDAI Simplified - Widget Interface Module
Provides clean accordion-style widget interface for WebUI configuration
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'modules'))

try:
    import ipywidgets as widgets
    from IPython.display import display
    IPYTHON_AVAILABLE = True
except ImportError:
    IPYTHON_AVAILABLE = False
    print("Warning: ipywidgets not available. Using simulation mode.")

from config import load_config, save_config, update_config
from model_parser import ModelTextParser
from hardware_optimizer import SimpleHardwareOptimizer

# Supported WebUIs
SUPPORTED_WEBUIS = {
    'forge': {
        'name': 'Stable Diffusion WebUI Forge',
        'repo': 'https://github.com/lllyasviel/stable-diffusion-webui-forge.git',
        'install_script': 'install_forge.py',
        'launch_args': '--xformers --cuda-stream'
    },
    'a1111': {
        'name': 'AUTOMATIC1111 WebUI',
        'repo': 'https://github.com/AUTOMATIC1111/stable-diffusion-webui.git',
        'install_script': 'install_a1111.py',
        'launch_args': '--xformers --no-half-vae'
    },
    'comfyui': {
        'name': 'ComfyUI',
        'repo': 'https://github.com/comfyanonymous/ComfyUI.git',
        'install_script': 'install_comfyui.py',
        'launch_args': '--dont-print-server'
    },
    'fooocus': {
        'name': 'Fooocus',
        'repo': 'https://github.com/lllyasviel/Fooocus.git',
        'install_script': 'install_fooocus.py',
        'launch_args': '--preset anime'
    }
}

class SimpleWidgetInterface:
    """Simple accordion-style widget interface for LSDAI"""
    
    def __init__(self):
        self.config = load_config()
        self.model_parser = ModelTextParser()
        self.hardware_optimizer = SimpleHardwareOptimizer()
        self.widgets = {}
        
    def create_interface(self):
        """Create the main accordion interface"""
        if not IPYTHON_AVAILABLE:
            print("Creating simulated widget interface...")
            return self.create_simulated_interface()
        
        # Create sections
        sections = [
            self.create_webui_section(),
            self.create_model_section(),
            self.create_text_section(),
            self.create_config_section()
        ]
        
        # Create accordion
        accordion = widgets.Accordion(sections)
        accordion.set_title(0, '🚀 WebUI Selection')
        accordion.set_title(1, '🎨 Model Selection')
        accordion.set_title(2, '📝 Text Input')
        accordion.set_title(3, '⚙️ Configuration')
        
        return accordion
    
    def create_simulated_interface(self):
        """Create a text-based simulation of the interface"""
        print("\n" + "="*50)
        print("LSDAI Simplified Widget Interface (Simulation)")
        print("="*50)
        
        print("\n1. 🚀 WebUI Selection")
        print("Available WebUIs:")
        for key, info in SUPPORTED_WEBUIS.items():
            selected = "✓" if self.config.get('webui', {}).get('selected') == key else " "
            print(f"  {selected} {key}: {info['name']}")
        
        print("\n2. 🎨 Model Selection")
        print("Model categories: SD1.5, SDXL")
        print("Types: Checkpoints, LoRAs, VAEs, ControlNet")
        
        print("\n3. 📝 Text Input")
        print("Text-based model shopping cart")
        print("Use format: $ckpt, $lora, $vae, $controlnet")
        
        print("\n4. ⚙️ Configuration")
        print(f"Verbosity: {self.config.get('verbosity', 'pretty')}")
        print(f"Hardware profile: {self.config.get('hardware', {}).get('optimization_profile', 'auto')}")
        
        print("\n" + "="*50)
        return "Simulated interface created"
    
    def create_webui_section(self):
        """Create WebUI selection section"""
        webui_options = [f"{key}: {info['name']}" for key, info in SUPPORTED_WEBUIS.items()]
        selected_webui = self.config.get('webui', {}).get('selected', 'forge')
        
        # Find index of selected WebUI
        selected_index = 0
        for i, option in enumerate(webui_options):
            if option.startswith(selected_webui):
                selected_index = i
                break
        
        dropdown = widgets.Dropdown(
            options=webui_options,
            value=webui_options[selected_index],
            description='WebUI:',
            style={'description_width': 'initial'}
        )
        
        dropdown.observe(self.on_webui_change, names='value')
        self.widgets['webui'] = dropdown
        
        # WebUI info
        info_html = widgets.HTML(value=self.get_webui_info(selected_webui))
        
        return widgets.VBox([dropdown, info_html])
    
    def create_model_section(self):
        """Create model selection section"""
        # SD1.5/SDXL toggle
        sdxl_toggle = widgets.ToggleButton(
            value=False,
            description='Show SDXL Models',
            button_style='info',
            style={'description_width': 'initial'}
        )
        
        # Model selection grid
        model_grid = self.create_model_grid(sdxl_toggle.value)
        
        sdxl_toggle.observe(self.on_sdxl_toggle, names='value')
        self.widgets['sdxl_toggle'] = sdxl_toggle
        
        return widgets.VBox([sdxl_toggle, model_grid])
    
    def create_text_section(self):
        """Create text input section"""
        # Text area for model shopping cart
        text_area = widgets.Textarea(
            value=self.config.get('models', {}).get('text_input', ''),
            placeholder='Enter model URLs with categories:\n$ckpt\nhttps://example.com/model1.safetensors\nhttps://example.com/model2.safetensors\n\n$lora\nhttps://example.com/lora1.safetensors',
            description='Models:',
            layout={'width': '100%', 'height': '200px'},
            style={'description_width': 'initial'}
        )
        
        text_area.observe(self.on_text_change, names='value')
        self.widgets['text_input'] = text_area
        
        # Parse button
        parse_btn = widgets.Button(
            description='Parse Models',
            button_style='success',
            style={'description_width': 'initial'}
        )
        
        parse_btn.on_click(self.on_parse_click)
        self.widgets['parse_btn'] = parse_btn
        
        # Results area
        results_area = widgets.HTML(value="Ready to parse models...")
        self.widgets['parse_results'] = results_area
        
        return widgets.VBox([text_area, parse_btn, results_area])
    
    def create_config_section(self):
        """Create configuration section"""
        # Verbosity selection
        verbosity_options = ['pretty', 'raw']
        selected_verbosity = self.config.get('verbosity', 'pretty')
        
        verbosity_dropdown = widgets.Dropdown(
            options=verbosity_options,
            value=selected_verbosity,
            description='Verbosity:',
            style={'description_width': 'initial'}
        )
        
        verbosity_dropdown.observe(self.on_verbosity_change, names='value')
        self.widgets['verbosity'] = verbosity_dropdown
        
        # Hardware optimization
        hardware_profile = self.config.get('hardware', {}).get('optimization_profile', 'auto')
        
        hardware_dropdown = widgets.Dropdown(
            options=['auto', 'low_vram', 'medium_vram', 'high_vram', 'cpu_only'],
            value=hardware_profile,
            description='Hardware Profile:',
            style={'description_width': 'initial'}
        )
        
        hardware_dropdown.observe(self.on_hardware_change, names='value')
        self.widgets['hardware'] = hardware_dropdown
        
        # Save config button
        save_btn = widgets.Button(
            description='Save Configuration',
            button_style='warning',
            style={'description_width': 'initial'}
        )
        
        save_btn.on_click(self.on_save_click)
        self.widgets['save_btn'] = save_btn
        
        return widgets.VBox([verbosity_dropdown, hardware_dropdown, save_btn])
    
    def create_model_grid(self, sdxl_mode=False):
        """Create model selection grid"""
        # This is a simplified version - in a real implementation,
        # you would load actual model data from the data files
        
        model_type = 'sdxl' if sdxl_mode else 'sd15'
        
        # Create checkboxes for different model categories
        categories = ['Checkpoint', 'LoRA', 'VAE', 'ControlNet']
        
        category_widgets = []
        for category in categories:
            # Sample models for demonstration
            if model_type == 'sd15':
                models = [f'SD1.5 {category} 1', f'SD1.5 {category} 2']
            else:
                models = [f'SDXL {category} 1', f'SDXL {category} 2']
            
            checkboxes = []
            for model in models:
                checkbox = widgets.Checkbox(
                    value=False,
                    description=model,
                    style={'description_width': 'initial'}
                )
                checkboxes.append(checkbox)
            
            category_box = widgets.VBox([
                widgets.HTML(value=f"<b>{category}</b>"),
                widgets.HBox(checkboxes)
            ])
            
            category_widgets.append(category_box)
        
        return widgets.VBox(category_widgets)
    
    def get_webui_info(self, webui_key):
        """Get HTML info for selected WebUI"""
        if webui_key in SUPPORTED_WEBUIS:
            info = SUPPORTED_WEBUIS[webui_key]
            return f"""
            <div style="padding: 10px; background-color: #f0f0f0; border-radius: 5px;">
                <b>{info['name']}</b><br>
                Repository: {info['repo']}<br>
                Default Args: {info['launch_args']}
            </div>
            """
        return "<div>Select a WebUI</div>"
    
    # Event handlers
    def on_webui_change(self, change):
        """Handle WebUI selection change"""
        selected = change['new'].split(':')[0]
        update_config('webui.selected', selected)
        
        # Update info display
        if 'webui' in self.widgets:
            # This would update the info HTML in a real implementation
            pass
    
    def on_sdxl_toggle(self, change):
        """Handle SDXL toggle change"""
        sdxl_mode = change['new']
        # Update model grid
        if 'model_grid' in self.widgets:
            # This would update the model grid in a real implementation
            pass
    
    def on_text_change(self, change):
        """Handle text input change"""
        text = change['new']
        update_config('models.text_input', text)
    
    def on_parse_click(self, b):
        """Handle parse button click"""
        text = self.widgets['text_input'].value
        if not text.strip():
            self.widgets['parse_results'].value = "Please enter some model URLs."
            return
        
        try:
            parsed_models = self.model_parser.parse_text_input(text)
            
            # Display results
            result_html = "<b>Parsed Models:</b><br>"
            for category in ['sd15', 'sdxl']:
                models = parsed_models[category]
                if any(models.values()):
                    result_html += f"<br><b>{category.upper()}:</b><br>"
                    for model_type, model_list in models.items():
                        if model_list:
                            result_html += f"  {model_type}: {len(model_list)} models<br>"
            
            self.widgets['parse_results'].value = result_html
            
            # Save parsed models to config
            update_config('models.parsed', parsed_models)
            
        except Exception as e:
            self.widgets['parse_results'].value = f"Error parsing models: {str(e)}"
    
    def on_verbosity_change(self, change):
        """Handle verbosity change"""
        verbosity = change['new']
        update_config('verbosity', verbosity)
    
    def on_hardware_change(self, change):
        """Handle hardware profile change"""
        profile = change['new']
        update_config('hardware.optimization_profile', profile)
    
    def on_save_click(self, b):
        """Handle save configuration button click"""
        try:
            save_config(self.config)
            self.widgets['save_btn'].description = 'Configuration Saved!'
            self.widgets['save_btn'].button_style = 'success'
            
            # Reset button after 2 seconds
            import time
            time.sleep(2)
            self.widgets['save_btn'].description = 'Save Configuration'
            self.widgets['save_btn'].button_style = 'warning'
            
        except Exception as e:
            self.widgets['save_btn'].description = f'Save Failed: {str(e)}'
            self.widgets['save_btn'].button_style = 'danger'

def main():
    """Main function to create and display the widget interface"""
    print("Creating LSDAI Simplified Widget Interface...")
    
    interface = SimpleWidgetInterface()
    widget_interface = interface.create_interface()
    
    if IPYTHON_AVAILABLE:
        display(widget_interface)
    else:
        print("Widget interface created (simulation mode)")
        print("In a real Jupyter environment, this would display interactive widgets.")

if __name__ == "__main__":
    main()