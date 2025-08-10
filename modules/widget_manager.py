# modules/widget_manager.py

import ipywidgets as widgets
from IPython.display import display

# Import our custom modules
from . import config_manager
from . import data_loader

class WidgetManager:
    """
    Manages the creation, layout, and logic of all UI widgets.
    """
    def __init__(self):
        """Initializes the WidgetManager."""
        self.widgets = {}  # A dictionary to hold all widget instances for easy access.
        self.layout = None # The final UI layout container.

    def _create_widgets(self):
        """Creates all the individual widget instances."""
        # --- WebUI & Model Version ---
        self.widgets['webui'] = widgets.Dropdown(options=['Forge', 'A1111', 'ComfyUI'], description='WebUI:')
        self.widgets['sdxl_toggle'] = widgets.Checkbox(value=False, description='Load SDXL Models')

        # --- Model, VAE, LoRA Selection (defaults to SD1.5) ---
        self.widgets['model'] = widgets.Dropdown(options=data_loader.get_model_list("sd1.5"), description='Model:')
        self.widgets['vae'] = widgets.Dropdown(options=data_loader.get_vae_list("sd1.5"), description='VAE:')
        self.widgets['lora'] = widgets.Dropdown(options=data_loader.get_lora_list("sd1.5"), description='LoRA:')

        # --- Custom Downloads ---
        self.widgets['custom_urls'] = widgets.Textarea(
            placeholder='Enter one URL per line for custom models, VAEs, LoRAs...',
            layout={'width': '98%', 'height': '100px'}
        )

        # --- Save Button ---
        self.widgets['save_button'] = widgets.Button(description='Save Settings', button_style='success', icon='save')

    def _create_layout(self):
        """Arranges widgets into a coherent layout using HBox and VBox."""
        # Combine WebUI and SDXL toggle
        box1 = widgets.VBox([self.widgets['webui'], self.widgets['sdxl_toggle']])
        # Combine Model, VAE, LoRA dropdowns
        box2 = widgets.VBox([self.widgets['model'], self.widgets['vae'], self.widgets['lora']])
        # Place major selection areas side-by-side
        top_selections = widgets.HBox([box1, box2])

        # Create a title for the custom URL section
        custom_url_title = widgets.HTML("<b>Custom Downloads (one URL per line)</b>")

        # Assemble the final layout
        self.layout = widgets.VBox([
            top_selections,
            widgets.HTML("<hr>"),
            custom_url_title,
            self.widgets['custom_urls'],
            widgets.HTML("<hr>"),
            self.widgets['save_button']
        ])

    def _register_callbacks(self):
        """Registers event handlers for interactive widgets."""
        self.widgets['sdxl_toggle'].observe(self._handle_sdxl_toggle, names='value')
        self.widgets['save_button'].on_click(self._handle_save_button)

    def _handle_sdxl_toggle(self, change):
        """Called when the SDXL checkbox is toggled to update dropdown options."""
        version = "sdxl" if change['new'] else "sd1.5"

        with self.widgets['model'].hold_sync(), self.widgets['vae'].hold_sync(), self.widgets['lora'].hold_sync():
            self.widgets['model'].options = data_loader.get_model_list(version)
            self.widgets['vae'].options = data_loader.get_vae_list(version)
            self.widgets['lora'].options = data_loader.get_lora_list(version)

            # Load the saved setting for the new model type
            key = 'model_sdxl' if change['new'] else 'model_sd15'
            self.widgets['model'].value = config_manager.get_setting('WIDGETS', key, 'none')

    def _handle_save_button(self, button):
        """Saves the current state of all widgets to the settings file."""
        print("Saving settings...")
        config_manager.set_setting('WEBUI', 'current', self.widgets['webui'].value)

        # Save the correct model based on the toggle state
        if self.widgets['sdxl_toggle'].value:
            config_manager.set_setting('WIDGETS', 'model_sdxl', self.widgets['model'].value)
        else:
            config_manager.set_setting('WIDGETS', 'model_sd15', self.widgets['model'].value)

        config_manager.set_setting('WIDGETS', 'vae', self.widgets['vae'].value)
        config_manager.set_setting('WIDGETS', 'lora', self.widgets['lora'].value)
        config_manager.set_setting('WIDGETS', 'custom_urls', self.widgets['custom_urls'].value)
        print("Settings saved successfully!")

    def _load_settings(self):
        """Loads settings from config_manager and applies them to the widgets."""
        self.widgets['webui'].value = config_manager.get_setting('WEBUI', 'current', 'Forge')

        # Note: We do not load the SDXL toggle state, it always defaults to False.
        # We load the model for the default view (SD1.5).
        self.widgets['model'].value = config_manager.get_setting('WIDGETS', 'model_sd15', 'none')
        self.widgets['vae'].value = config_manager.get_setting('WIDGETS', 'vae', 'none')
        self.widgets['lora'].value = config_manager.get_setting('WIDGETS', 'lora', 'none')
        self.widgets['custom_urls'].value = config_manager.get_setting('WIDGETS', 'custom_urls', '')

    def display(self):
        """The main public method to build and display the entire UI."""
        self._create_widgets()
        self._create_layout()
        self._register_callbacks()
        self._load_settings()
        display(self.layout)
