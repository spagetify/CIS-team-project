import subprocess
import sys
import os

def install_dependencies():
    """Installs Python dependencies listed in requirements.txt."""
    requirements_file = "requirements.txt"

    if not os.path.exists(requirements_file):
        print(f"Error: '{requirements_file}' not found. Please create it with your project's dependencies.")
        sys.exit(1)

    print(f"Installing dependencies from '{requirements_file}'...")
    try:
        # Use sys.executable to ensure the correct Python interpreter's pip is used
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: 'pip' command not found. Ensure pip is installed and in your PATH.")
        sys.exit(1)

if __name__ == "__main__":
    install_dependencies()