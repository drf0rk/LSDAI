# LSDAI-Simplified

A simplified, focused multi-WebUI launcher that combines the best features of LSDAI with sdAIgen's simplicity and maintainability.

## 🎯 Project Vision

Create a streamlined multi-WebUI launcher that:

- **Focus**: Launch Stable Diffusion WebUIs effectively
- **Simplicity**: Appropriate complexity for the task
- **Maintainability**: Clean, understandable code
- **User Experience**: Intuitive interface with essential features

## 🚀 Quick Start

### Method 1: Automated Installation (Recommended)

```bash
# Clone or download the project
cd LSDAI-Simplified

# Run the universal installer
chmod +x universal_installer.sh
./universal_installer.sh
```

### Method 2: Simple Setup

```bash
# Simple Python setup
python3 simple_setup.py
```

### Method 3: Comprehensive Setup

```bash
# Full-featured setup with JupyterLab integration
python3 complete_setup.py
```

### Method 4: Manual Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or venv\\Scripts\\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Start Jupyter
jupyter lab
```

## 📁 Project Structure

```
LSDAI-Simplified/
├── LSDAI-Simplified.ipynb              # Main notebook (Linux/macOS)
├── LSDAI-Simplified-Windows.ipynb      # Windows-compatible notebook
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── setup.sh                            # Bash installation script
├── installer.py                        # Comprehensive Python installer
├── simple_setup.py                     # Simple Python setup
├── complete_setup.py                   # Complete Python setup
├── universal_installer.sh              # Cross-platform installer
├── auto_execute.py                     # Auto-execution script
├── config.json                         # Project configuration
├── scripts/                           # Core scripts
│   ├── setup.py                       # Environment setup
│   ├── widgets.py                     # Widget interface
│   ├── downloader.py                  # Download management
│   └── launcher.py                    # WebUI launcher
├── modules/                           # Core modules
│   ├── config.py                      # Configuration management
│   ├── webui_manager.py               # WebUI management
│   ├── model_parser.py                # Text shopping cart parser
│   └── hardware_optimizer.py          # Hardware optimization
├── data/                              # Model data
│   ├── models_sd15.py                 # SD1.5 model definitions
│   └── models_sdxl.py                 # SDXL model definitions
├── shared_models/                      # Shared model storage
│   ├── Stable-diffusion/
│   ├── VAE/
│   ├── Lora/
│   ├── ControlNet/
│   └── embeddings/
├── configs/                           # WebUI configuration templates
│   ├── forge/
│   ├── a1111/
│   ├── comfyui/
│   └── fooocus/
└── logs/                              # Execution and installation logs
```

## 🎯 Supported WebUIs

| WebUI | Description | Status |
|-------|-------------|--------|
| **Forge** | Performance-optimized A1111 fork | ✅ Supported |
| **A1111** | Original AUTOMATIC1111 WebUI | ✅ Supported |
| **ComfyUI** | Node-based workflow interface | ✅ Supported |
| **Fooocus** | Simplified, user-friendly interface | ✅ Supported |

## 🔧 Key Features

### Multi-WebUI Support
- Launch multiple Stable Diffusion WebUIs
- Sequential execution (one at a time)
- Shared model storage with symlinks
- Individual WebUI configuration

### Model Management
- Text-based model shopping cart system
- Traditional model selection interface
- SD1.5/SDXL categorization
- Automatic model organization

### Cross-Platform Compatibility
- **Linux**: Full widget functionality
- **macOS**: Full widget functionality  
- **Windows**: Console-based interface

### Installation Methods
- **Universal Installer**: Cross-platform shell script
- **Python Installers**: Multiple complexity levels
- **Manual Setup**: For advanced users

## 📖 Usage

### Basic Workflow

1. **Setup**: Run one of the installation scripts
2. **Configure**: Edit `config.json` if needed
3. **Launch**: Start Jupyter and open the notebook
4. **Execute**: Run cells in sequence (Setup → Configure → Download → Launch)

### Configuration

Edit `config.json` to customize:

```json
{
  "webui": {
    "selected": "forge",
    "launch_args": "--xformers --cuda-stream"
  },
  "models": {
    "selected_sd15": [],
    "selected_sdxl": [],
    "text_input": ""
  },
  "verbosity": "normal"
}
```

### Text-Based Model Shopping Cart

Use the text input to add models:

```
$ckpt
https://huggingface.co/ runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.ckpt

$lora
https://civitai.com/api/download/models/12345 [style_lora.safetensors]
```

## 🛠️ Installation Scripts

### `universal_installer.sh`
- **Platform**: Linux, macOS, Windows (WSL)
- **Features**: Complete automated installation
- **Dependencies**: Installs system and Python packages

### `installer.py`
- **Platform**: Cross-platform Python
- **Features**: Comprehensive installation with logging
- **Best for**: Production environments

### `simple_setup.py`
- **Platform**: Cross-platform Python
- **Features**: Basic installation only
- **Best for**: Quick setup and testing

### `complete_setup.py`
- **Platform**: Cross-platform Python
- **Features**: Full setup with JupyterLab integration
- **Best for**: Development environments

### `setup.sh`
- **Platform**: Linux/macOS only
- **Features**: Bash-based installation
- **Best for**: Server environments

## 📊 System Requirements

### Minimum Requirements
- **Python**: 3.8+
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **GPU**: CUDA-compatible GPU recommended

### Recommended Requirements
- **Python**: 3.9+
- **RAM**: 16GB+
- **Storage**: 10GB+ free space
- **GPU**: 8GB+ VRAM

## 🔍 Troubleshooting

### Common Issues

#### Installation Fails
```bash
# Check Python version
python3 --version

# Ensure pip is available
python3 -m pip --version

# Try manual virtual environment creation
python3 -m venv venv
```

#### Module Import Errors
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or venv\\Scripts\\activate  # Windows

# Reinstall packages
pip install -r requirements.txt
```

#### WebUI Won't Start
- Check GPU drivers
- Verify CUDA installation
- Ensure sufficient VRAM
- Check launch arguments in config.json

### Log Files

Check installation and execution logs:
- `logs/install.log` - Installation logs
- `logs/execution.log` - Notebook execution logs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **LSDAI**: For the comprehensive feature set and architecture ideas
- **sdAIgen**: For the simplicity and maintainability approach
- **Stable Diffusion Community**: For the amazing WebUI implementations

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review log files in the `logs/` directory
3. Open an issue on the project repository

---

**LSDAI-Simplified** - Making Stable Diffusion accessible to everyone.