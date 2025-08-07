# 🚀 LSDAI Simplified - Multi-WebUI Launcher

A simplified, focused multi-WebUI launcher for Stable Diffusion that combines the best features of LSDAI with sdAIgen's simplicity and maintainability.

## 🎯 Features

- ✅ **Multi-WebUI Support**: Forge, A1111, ComfyUI, Fooocus
- ✅ **Sequential Execution**: Only one WebUI runs at a time
- ✅ **Text-Based Model Shopping Cart**: Easy model management
- ✅ **Profile-Based Hardware Optimization**: No AI in notebook
- ✅ **Simple JSON Configuration**: No complex ODM
- ✅ **Cross-Platform Compatibility**: Works on Linux, Windows, and macOS

## 🏗️ Architecture

```
Cell 1: Setup → Cell 2: Configuration → Cell 3: Download → Cell 4: Launch
```

## 📁 Project Structure

```
LSDAI-Simplified/
├── LSDAI-Simplified.ipynb              # Main notebook (Linux/macOS)
├── LSDAI-Simplified-Windows.ipynb      # Windows-compatible notebook
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
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
└── data/                              # Model data
    ├── models_sd15.py                 # SD1.5 model definitions
    └── models_sdxl.py                 # SDXL model definitions
```

## 🚀 Quick Start

### For Linux/macOS:
1. Open `LSDAI-Simplified.ipynb` in Jupyter
2. Run Cell 1 (Setup)
3. Run Cell 2 (Configuration)
4. Run Cell 3 (Download)
5. Run Cell 4 (Launch)

### For Windows:
1. Open `LSDAI-Simplified-Windows.ipynb` in Jupyter
2. Run Cell 1 (Setup)
3. Run Cell 2 (Configuration)
4. Run Cell 3 (Download)
5. Run Cell 4 (Launch)

## 📋 Usage Instructions

### Step 1: Setup
- Creates directory structure
- Installs dependencies
- Sets up configuration

### Step 2: Configuration
- Select your preferred WebUI
- Add models using text input or selection
- Configure hardware optimization
- Save your preferences

### Step 3: Download
- Downloads models from your saved list
- Uses aria2c (Linux/macOS) or requests (Windows)
- Shows progress with widgets or console output

### Step 4: Launch
- Launch your selected WebUI
- Automatically optimized for your hardware
- Monitor real-time output
- Stop gracefully when done

## 🎯 Key Features

### Text-Based Model Shopping Cart
```
$ckpt
https://civitai.com/api/download/models/12345[My Model]
$lora
https://civitai.com/api/download/models/67890[My LoRA]
$vae
https://civitai.com/api/download/models/54321[My VAE]
```

### Hardware Optimization Profiles
- **Low VRAM (≤4GB)**: `--medvram --lowvram`
- **Medium VRAM (≤8GB)**: `--medvram`
- **High VRAM (>8GB)**: `--xformers`
- **CPU Only**: `--cpu`

### Supported WebUIs
- **Forge**: Stable Diffusion WebUI Forge
- **A1111**: AUTOMATIC1111 WebUI
- **ComfyUI**: ComfyUI
- **Fooocus**: Fooocus

## 🔧 Requirements

### Python Dependencies
```bash
pip install -r requirements.txt
```

### System Dependencies
- **Git**: For WebUI installation
- **Python 3.8+**: Required runtime
- **aria2c** (Linux/macOS): For fast downloads (optional)
- **Requests**: For Windows downloads (included in requirements.txt)

### Optional Dependencies
- **ipywidgets**: For interactive widgets (Linux/macOS)
- **gitpython**: For Git operations (optional)

## 🔧 Troubleshooting

### Common Issues

1. **ipywidgets not available** (Linux/macOS)
   ```bash
   pip install ipywidgets
   ```

2. **aria2c not found** (Linux/macOS)
   - The system will fallback to other download methods
   - Install aria2c for best performance: `apt-get install aria2`

3. **Git not found** (Windows)
   - Install Git for Windows from https://git-scm.com/
   - Add Git to system PATH

4. **Permission errors** (Windows)
   - Run Command Prompt as Administrator
   - Check file/folder permissions

5. **WebUI installation failed**
   - Check internet connection
   - Ensure git is available
   - Try running the setup cell again

6. **Model download failed**
   - Check URL validity
   - Ensure sufficient disk space
   - Try different download method (automatic fallback)

## 🎉 Enjoy!

This simplified LSDAI provides all the essential features you need without the complexity of the original version. Focus on what matters: creating amazing AI art!

## 📄 License

This project is open source and available under the MIT License.