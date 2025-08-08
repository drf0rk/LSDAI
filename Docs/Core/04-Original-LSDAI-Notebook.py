# -*- coding: utf-8 -*-
"""
04-Original-LSDAI-Notebook.py - Original LSDAI Implementation

EXECUTION PROMPT: You are continuing the LSDAI project with a focus on creating a simplified, user-friendly multi-WebUI launcher. Your immediate task is to develop and execute a comprehensive testing strategy for all installation scripts, then refine them based on testing results to ensure reliable deployment across different platforms. Start by thoroughly reading all 4 core documentation files to understand the complete project context, then examine all installation scripts to understand their functionality, create a detailed testing plan, execute validation tests, analyze results, and refine the scripts and documentation based on your findings. Focus on ensuring that all installation methods work reliably across different platforms, maintain cross-platform compatibility, and provide a seamless user experience with comprehensive error handling and progress monitoring. Begin your response with a summary of your understanding of the project context and testing requirements, then proceed with developing and executing the testing strategy, referencing this handover document as your authoritative context throughout our interaction.

Original file is located at:
    https://colab.research.google.com/drive/13eT-kfOSdQWJANb18uHpxfdmQjms1xAp
"""

# ============================================================================
# LSDAI Enhanced WebUI System - Complete Notebook Cells (Fixed)
# ============================================================================

# ===========================================
# CELL 1: Environment Setup & Enhancement Installation
# ===========================================

#@title **LSDAI Enhanced Setup - Git Clone Method** { display-mode: "form" }

import os
import sys
import subprocess
import shutil
import json
from pathlib import Path

print("⤵️ Ensuring safe working directory...")
# %cd /content

print("📦 Installing system dependencies...")
try:
    subprocess.run(['apt-get', 'update', '-qq'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    subprocess.run(['apt-get', 'install', '-y', '-qq', 'python3-venv', 'git', 'aria2', 'wget'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    print("✅ System dependencies installed.")
except (subprocess.CalledProcessError, FileNotFoundError) as e:
    print(f"⚠️  Could not install system dependencies. Assuming they are present.")

project_dir = Path('/content/LSDAI')

if project_dir.exists():
    print("🧹 Cleaning up existing installation...")
    shutil.rmtree(project_dir, ignore_errors=True)

print("📥 Cloning LSDAI repository...")
try:
    subprocess.run(['git', 'clone', '-q', 'https://github.com/remphanstar/LSDAI.git', str(project_dir)], check=True, stderr=subprocess.PIPE)
except subprocess.CalledProcessError as e:
    print(f"❌ FATAL: Git clone failed. Error: {e.stderr.decode()}")
    raise e

# %cd {project_dir}
print(f"⤵️ Changed directory to {os.getcwd()}")

modules_path = project_dir / 'modules'
if str(modules_path) not in sys.path:
    sys.path.insert(0, str(modules_path))
    print(f"✅ Added {modules_path} to Python path")

settings_file = project_dir / 'settings.json'
env_settings = {
    "home_path": "/content",
    "scr_path": str(project_dir),
    "venv_path": "/content/venv",
    "settings_path": str(settings_file)
}

print("🔧 Setting up environment variables...")
os.environ.update(env_settings)
print("✅ Environment variables set.")

if not settings_file.exists():
    initial_settings = {
        "ENVIRONMENT": env_settings,
        "WIDGETS": {},
        "WEBUI": {"current": "automatic1111"}
    }
    settings_file.write_text(json.dumps(initial_settings, indent=4))
    print("✅ Created initial settings file")

enhancement_script = project_dir / 'setup_enhancements.py'
if enhancement_script.exists():
    print("🔧 Running enhancement setup...")
#     %run {enhancement_script}
else:
    print("✅ Repository cloned successfully!")

print("🎉 Setup completed! You can now run Cell 2 (Widgets).")

# Commented out IPython magic to ensure Python compatibility.
# ===========================================
# CELL 2: Enhanced Widgets with Verbosity Control
# ===========================================

#@title **1. Enhanced Widgets** 🔽 { display-mode: "form" }

import os
import json
from pathlib import Path

project_dir = Path('/content/LSDAI')
settings_path = project_dir / 'settings.json'

print("🔧 Verifying environment for widgets...")
if settings_path.exists():
    try:
        with open(settings_path, 'r') as f:
            settings = json.load(f)

        env_paths = settings.get("ENVIRONMENT", {})
        required_paths = ['home_path', 'scr_path', 'venv_path', 'settings_path']

        for path_key in required_paths:
            if path_key not in os.environ and path_key in env_paths:
                os.environ[path_key] = str(env_paths[path_key])

        print("✅ Environment variables verified.")
    except Exception as e:
        print(f"❌ Error loading settings.json: {e}")
else:
    print("⚠️ Warning: settings.json not found.")

print("🚀 Running enhanced widgets with verbosity control...")
main_widget_script_path = project_dir / 'scripts/enhanced_widgets_integration.py'
if main_widget_script_path.exists():
#     %run {main_widget_script_path}
else:
    print("❌ Enhanced widgets script not found.")

# Commented out IPython magic to ensure Python compatibility.
# ===========================================
# CELL 3: Enhanced Downloading with Restored Functionality
# ===========================================

#@title **2. Enhanced Downloading** 🔽 { display-mode: "form" }

from pathlib import Path

# Verify project setup
project_dir = Path('/content/LSDAI')
downloading_script = project_dir / 'scripts/enhanced_downloading_integration.py'

print("🚀 LSDAI Enhanced Downloading System")
print("=" * 40)

if not downloading_script.exists():
    print("❌ Enhanced downloading script not found.")
    print("   Please ensure Cell 1 (Setup) completed successfully.")
else:
    print("✅ Starting enhanced downloading with restored functionality...")
#     %run {downloading_script}

# Commented out IPython magic to ensure Python compatibility.
# ===========================================
# CELL 4: Enhanced Launch
# ===========================================

#@title **3. Enhanced Launch** 🔽 { display-mode: "form" }

import os
from pathlib import Path

project_dir = Path('/content/LSDAI')
launch_script = project_dir / 'scripts/enhanced_launch_integration.py'

print("🚀 LSDAI Enhanced Launch System")
print("=" * 40)

if not launch_script.exists():
    print(f"❌ Launch script not found at {launch_script}")
    print("Please ensure Cell 1 (Setup) completed successfully.")
else:
    print("✅ Starting Enhanced Launch System...")
#     %run {launch_script}

# ===========================================
# ALTERNATIVE CELL 4: Manual Launch (Fallback)
# ===========================================

#@title **3. Manual WebUI Launch (Fallback)** 🔽 { display-mode: "form" }

import os
import sys
import subprocess
from pathlib import Path

project_dir = Path('/content/LSDAI')

print("🔧 Manual WebUI Launch - Fallback System")
print("=" * 40)

# Add modules to path
modules_path = project_dir / 'modules'
if str(modules_path) not in sys.path:
    sys.path.insert(0, str(modules_path))

# Try to use verbosity system
try:
    from modules.verbose_output_manager import get_verbose_manager, VerbosityLevel, vprint
    verbose_manager = get_verbose_manager()

    def print_msg(msg, level=VerbosityLevel.NORMAL):
        vprint(msg, level)
except ImportError:
    def print_msg(msg, level=None):
        print(msg)

# Find WebUI installation
base_path = Path('/content')
webui_paths = [
    base_path / 'stable-diffusion-webui',
    base_path / 'ComfyUI',
    base_path / 'automatic1111'
]

webui_path = None
for path in webui_paths:
    if path.exists() and (path / 'launch.py').exists():
        webui_path = path
        break

if not webui_path:
    print_msg("❌ No WebUI installation found. Please run Cell 3 (Downloading) first.")
else:
    print_msg(f"✅ Found WebUI: {webui_path}")

    # Use venv python if available
    venv_path = base_path / 'venv'
    if venv_path.exists():
        python_exe = venv_path / 'bin' / 'python'
        if not python_exe.exists():
            python_exe = venv_path / 'Scripts' / 'python.exe'
    else:
        python_exe = sys.executable

    # Build launch command
    cmd = [str(python_exe), 'launch.py', '--share', '--xformers', '--no-half-vae']

    print_msg(f"🚀 Launching WebUI...")
    print_msg(f"Command: {' '.join(cmd)}")
    print_msg(f"Working directory: {webui_path}")

    try:
        # Change to WebUI directory
        original_cwd = os.getcwd()
        os.chdir(webui_path)

        # Start WebUI process
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )

        print_msg("✅ WebUI process started!")
        print_msg("📝 Monitoring output for URLs...")
        print("-" * 40)

        # Monitor output
        try:
            for line in iter(process.stdout.readline, ''):
                line = line.strip()
                if line:
                    print(line)
                    if 'running on local url:' in line.lower():
                        print(f"🎉 Local URL found: {line}")
                    elif 'running on public url:' in line.lower():
                        print(f"🌐 Public URL found: {line}")
        except KeyboardInterrupt:
            print_msg("\n⏹️ Stopping WebUI...")
            process.terminate()
            process.wait()
            print_msg("✅ WebUI stopped.")

        os.chdir(original_cwd)

    except Exception as e:
        print_msg(f"❌ Launch failed: {e}")
        os.chdir(original_cwd)

# ===========================================
# DIAGNOSTIC CELL: Troubleshooting
# ===========================================

#@title **🔍 System Diagnostics** 🔽 { display-mode: "form" }

import os
import sys
from pathlib import Path

print("🔍 LSDAI System Diagnostics")
print("=" * 40)

project_dir = Path('/content/LSDAI')

# Check project structure
print("\n📁 Project Structure:")
if project_dir.exists():
    print(f"✅ Project directory: {project_dir}")

    key_files = [
        'settings.json',
        'modules/__init__.py',
        'modules/json_utils.py',
        'modules/widget_factory.py',
        'modules/verbose_output_manager.py',
        'scripts/enhanced_widgets_integration.py',
        'scripts/enhanced_downloading_integration.py',
        'scripts/enhanced_launch_integration.py'
    ]

    for file_path in key_files:
        full_path = project_dir / file_path
        status = "✅" if full_path.exists() else "❌"
        print(f"  {status} {file_path}")
else:
    print(f"❌ Project directory not found: {project_dir}")

# Check Python path
print(f"\n🐍 Python Path Configuration:")
modules_path = project_dir / 'modules'
if str(modules_path) in sys.path:
    print(f"✅ Modules path in sys.path: {modules_path}")
else:
    print(f"❌ Modules path missing: {modules_path}")

# Check environment variables
print(f"\n🔧 Environment Variables:")
env_vars = ['home_path', 'scr_path', 'venv_path', 'settings_path']
for var in env_vars:
    value = os.environ.get(var, 'NOT SET')
    status = "✅" if value != 'NOT SET' else "❌"
    print(f"  {status} {var}: {value}")

# Check WebUI installations
print(f"\n🚀 WebUI Installations:")
base_path = Path('/content')
webui_checks = [
    ('Automatic1111', base_path / 'stable-diffusion-webui'),
    ('ComfyUI', base_path / 'ComfyUI'),
    ('Forge', base_path / 'stable-diffusion-webui-forge')
]

found_webui = False
for name, path in webui_checks:
    if path.exists():
        launch_script = path / 'launch.py'
        if launch_script.exists():
            print(f"✅ {name}: {path} (launch.py found)")
            found_webui = True
        else:
            print(f"⚠️ {name}: {path} (no launch.py)")
    else:
        print(f"❌ {name}: Not found")

if not found_webui:
    print("💡 Tip: Run Cell 3 (Enhanced Downloading) to install a WebUI")

# Check venv
print(f"\n🐍 Virtual Environment:")
venv_path = base_path / 'venv'
if venv_path.exists():
    python_venv = venv_path / 'bin' / 'python'
    if not python_venv.exists():
        python_venv = venv_path / 'Scripts' / 'python.exe'

    if python_venv.exists():
        print(f"✅ Virtual environment: {venv_path}")
        print(f"✅ Python executable: {python_venv}")
    else:
        print(f"⚠️ Virtual environment found but no python executable")
else:
    print(f"❌ No virtual environment found")

# Test imports
print(f"\n📦 Module Import Tests:")
test_imports = [
    ('json_utils', 'modules.json_utils'),
    ('widget_factory', 'modules.widget_factory'),
    ('verbose_output_manager', 'modules.verbose_output_manager')
]

for name, module in test_imports:
    try:
        __import__(module)
        print(f"✅ {name}: Import successful")
    except ImportError as e:
        print(f"❌ {name}: Import failed - {e}")

print(f"\n🎯 Diagnosis Complete!")
print("If you see any ❌ errors above, those need to be fixed before launching.")