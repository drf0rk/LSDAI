# scripts/setup_env.py

import sys
from pathlib import Path

def check_dependencies():
    """
    In the future, this function will install dependencies from requirements.txt.
    For now, it just confirms that the requirements file exists.
    """
    print("🔧 Checking for dependencies file...")
    project_root = Path(__file__).parent.parent
    requirements_path = project_root / "requirements.txt"

    if requirements_path.exists():
        print(f"   ✅ Found requirements.txt.")
        # In a future step, we would add:
        # import subprocess
        # print("   Installing dependencies...")
        # subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(requirements_path)])
    else:
        print(f"   ❌ Warning: requirements.txt not found at {requirements_path}.")
    print("   Dependency check complete.")

def verify_project_structure():
    """
    Verifies that the essential directories created in the previous step exist.
    """
    print("\n🔍 Verifying project structure...")
    project_root = Path(__file__).parent.parent
    required_dirs = ["modules", "configs", "shared_models", "webui_installations", "assets", "scripts"]
    all_ok = True

    for directory in required_dirs:
        dir_path = project_root / directory
        if dir_path.is_dir():
            print(f"   ✅ Found directory: {directory}/")
        else:
            print(f"   ❌ Missing required directory: {directory}/")
            all_ok = False

    if not all_ok:
        print("\n❌ Project structure verification failed. Some directories are missing.")
        sys.exit(1) # Exit with an error code if the structure is broken

    print("   ✅ Project structure is valid.")

def main():
    """Main setup function for Cell 1."""
    print("==============================================")
    print("🚀 Running LSDAI Environment Setup & Verification")
    print("==============================================")

    check_dependencies()
    verify_project_structure()

    print("\n🎉 Environment is verified and ready for the next steps.")
    print("==============================================")

if __name__ == "__main__":
    main()
