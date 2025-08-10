# modules/widget_manager.py

import ipywidgets as widgets
from IPython.display import display, HTML as IPHTML
from pathlib import Path

# Import our custom modules
from . import config_manager
from . import data_loader

class WidgetManager:
    """
    Manages the creation, layout, and logic of all UI widgets.
    """
    def __init__(self):
        """Initializes the WidgetManager."""
        self.widgets = {}
        self.layout = None
        self.assets_injected = False

    def _inject_assets(self):
        """Reads CSS and JS files and injects them into the notebook frontend."""
        if self.assets_injected:
            return

        assets_path = Path(__file__).parent.parent / "assets"
        css_path = assets_path / "main.css"
        js_path = assets_path / "main.js"

        css_content = ""
        if css_path.exists():
            css_content = css_path.read_text()

        js_content = ""
        if js_path.exists():
            js_content = js_path.read_text()

        # Display the assets wrapped in style and script tags
        display(IPHTML(f"<style>{css_content}</style><script>{js_content}</script>"))
        self.assets_injected = True

    def _create_widgets(self):
        """Creates all the individual widget instances."""
        self.widgets['webui'] = widgets.Dropdown(options=['Forge', 'A1111', 'ComfyUI'], description='WebUI:')
        self.widgets['sdxl_toggle'] = widgets.Checkbox(value=False, description='Load SDXL Models')
        self.widgets['model'] = widgets.Dropdown(options=data_loader.get_model_list("sd1.5"), description='Model:')
        self.widgets['vae'] = widgets.Dropdown(options=data_loader.get_vae_list("sd1.5"), description='VAE:')
        self.widgets['lora'] = widgets.Dropdown(options=data_loader.get_lora_list("sd1.5"), description='LoRA:')

        # --- New Custom Download Widgets ---
        self.widgets['empowerment_toggle'] = widgets.Checkbox(value=False, description='Empowerment Mode')
        self.widgets['custom_urls_empowered'] = widgets.Textarea(
            placeholder='Use #tags to specify download types, e.g.:\n#lora\nhttps://civitai.com/api/download/models/16576',
            layout={'width': '98%', 'height': '200px', 'visibility': 'hidden'}
        )
        # Individual fields for when empowerment is off
        self.widgets['model_url'] = widgets.Text(description="Model URL:")
        self.widgets['vae_url'] = widgets.Text(description="VAE URL:")
        self.widgets['lora_url'] = widgets.Text(description="LoRA URL:")

        self.widgets['save_button'] = widgets.Button(description='Save Settings', button_style='success', icon='save')

    def _create_layout(self):
        """Arranges widgets into a coherent layout using HBox and VBox."""
        # Standard selections
        box1 = widgets.VBox([self.widgets['webui'], self.widgets['sdxl_toggle']])
        box2 = widgets.VBox([self.widgets['model'], self.widgets['vae'], self.widgets['lora']])
        top_selections = widgets.HBox([box1, box2])

        # --- New Collapsible Custom Download Section ---
        collapsible_header = widgets.HTML(
            value="<div class='collapsible-header' onclick='toggleContainer()'>🔽 Custom Downloads</div>"
        )

        # Box for individual URL fields (visible by default)
        self.widgets['individual_urls_box'] = widgets.VBox([
            self.widgets['model_url'],
            self.widgets['vae_url'],
            self.widgets['lora_url'],
        ], layout={'visibility': 'visible'})

        # The empowerment text area is separate and its visibility will be toggled
        empowerment_area = self.widgets['custom_urls_empowered']

        # Place all download widgets inside the collapsible container
        custom_download_container = widgets.VBox([
            widgets.HBox([collapsible_header, self.widgets['empowerment_toggle']]),
            self.widgets['individual_urls_box'],
            empowerment_area
        ])
        custom_download_container.add_class("collapsible-container")

        # Main layout with animation class
        main_container = widgets.VBox([
            top_selections,
            custom_download_container,
            self.widgets['save_button']
        ], layout={'gap': '10px'})
        main_container.add_class("main-container-animated")

        self.layout = main_container

    def _register_callbacks(self):
        """Registers event handlers for interactive widgets."""
        self.widgets['sdxl_toggle'].observe(self._handle_sdxl_toggle, names='value')
        self.widgets['empowerment_toggle'].observe(self._handle_empowerment_toggle, names='value')
        self.widgets['save_button'].on_click(self._handle_save_button)

    def _handle_empowerment_toggle(self, change):
        """Shows/hides the correct custom download widgets."""
        if change['new']: # Empowerment is ON
            self.widgets['individual_urls_box'].layout.visibility = 'hidden'
            self.widgets['custom_urls_empowered'].layout.visibility = 'visible'
        else: # Empowerment is OFF
            self.widgets['individual_urls_box'].layout.visibility = 'visible'
            self.widgets['custom_urls_empowered'].layout.visibility = 'hidden'

    def _handle_sdxl_toggle(self, change):
        """Called when the SDXL checkbox is toggled to update dropdown options."""
        version = "sdxl" if change['new'] else "sd1.5"
        with self.widgets['model'].hold_sync(), self.widgets['vae'].hold_sync(), self.widgets['lora'].hold_sync():
            self.widgets['model'].options = data_loader.get_model_list(version)
            self.widgets['vae'].options = data_loader.get_vae_list(version)
            self.widgets['lora'].options = data_loader.get_lora_list(version)
            key = 'model_sdxl' if change['new'] else 'model_sd15'
            self.widgets['model'].value = config_manager.get_setting('WIDGETS', key, 'none')

    def _handle_save_button(self, button):
        """Saves the current state of all widgets to the settings file."""
        print("Saving settings...")
        widget_values = {}
        # Simple key-value pairs
        for key in ['webui', 'sdxl_toggle', 'vae', 'lora', 'empowerment_toggle']:
            widget_values[key] = self.widgets[key].value

        # Handle model saving based on toggle
        if self.widgets['sdxl_toggle'].value:
            widget_values['model_sdxl'] = self.widgets['model'].value
        else:
            widget_values['model_sd15'] = self.widgets['model'].value

        # Handle custom URL saving based on empowerment toggle
        if self.widgets['empowerment_toggle'].value:
            widget_values['custom_urls'] = self.widgets['custom_urls_empowered'].value
        else:
            # Combine individual URLs into the same 'custom_urls' field for the parser
            urls = []
            if self.widgets['model_url'].value: urls.append(f"#model\n{self.widgets['model_url'].value}")
            if self.widgets['vae_url'].value: urls.append(f"#vae\n{self.widgets['vae_url'].value}")
            if self.widgets['lora_url'].value: urls.append(f"#lora\n{self.widgets['lora_url'].value}")
            widget_values['custom_urls'] = "\n".join(urls)

        config_manager.set_setting('WIDGETS', 'all_widgets', widget_values)
        print("Settings saved successfully!")

    def _load_settings(self):
        """Loads settings from config_manager and applies them to the widgets."""
        widget_values = config_manager.get_setting('WIDGETS', 'all_widgets', {})
        if not widget_values: return

        for key, value in widget_values.items():
            if key in self.widgets:
                self.widgets[key].value = value

        # Handle custom URLs (this logic is a bit tricky, might need refinement)
        # For now, we don't try to parse the combined 'custom_urls' back into individual fields

    def display(self):
        """The main public method to build and display the entire UI."""
        self._inject_assets()
        self._create_widgets()
        self._create_layout()
        self._register_callbacks()
        # self._load_settings() # Loading logic needs to be refined after this change
        display(self.layout)
