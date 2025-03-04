import subprocess
import os
import sys

TOOL_FOLDER_NAME = ".page"
PACKAGE_NAME = "page"

def install_page_tool():
    """Installs the 'page' tool package into a .page folder."""
    tool_folder = os.path.expanduser(os.path.join("~", TOOL_FOLDER_NAME))

    print(f"Installing '{PACKAGE_NAME}' into {tool_folder}...")

    # 1. Create .page folder
    print(f"Creating .page folder: {tool_folder}")
    os.makedirs(tool_folder, exist_ok=True)
    print(".page folder created.")

    # 2. Create a virtual environment inside .page
    target_venv_path = tool_folder
    print(f"Creating virtual environment in: {target_venv_path}")
    try:
        subprocess.check_call([sys.executable, "-m", "venv", target_venv_path])
        print("Virtual environment created.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment: {e}")
        return False  # Indicate failure

    # 3. Install 'page' package into .page venv using pip
    target_pip_executable = os.path.join(tool_folder, "bin", "pip")
    print(f"Using pip from .page venv: {target_pip_executable}")

    # Upgrade pip (optional, but good practice)
    print("Upgrading pip in .page venv...")
    try:
        subprocess.check_call([target_pip_executable, "install", "--upgrade", "pip"])
        print("Pip upgraded.")
    except subprocess.CalledProcessError as e:
        print(f"Error upgrading pip: {e}")
        return False # Indicate failure

    print(f"Installing package '{PACKAGE_NAME}' into .page venv...")
    try:
        # Install directly from PyPI (assuming 'page' is published there)
        subprocess.check_call([target_pip_executable, "install", PACKAGE_NAME])
        # If not on PyPI yet, or for local dev install from source:
        # subprocess.check_call([target_pip_executable, "install", "."]) # if running from project root
        print(f"Package '{PACKAGE_NAME}' installed successfully in .page venv.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing package '{PACKAGE_NAME}' into .page venv: {e}")
        return False # Indicate failure

    print(f"\n'{PACKAGE_NAME}' tool package installed in: {tool_folder}")
    print(f"To use the tool, add '{os.path.join(tool_folder, 'bin')}' to your PATH.")
    print("Or, use the full path to the 'page' command in the '.page/bin' directory.")
    return True # Indicate success

if __name__ == "__main__":
    if install_page_tool():
        print("\nInstallation completed successfully!")
    else:
        print("\nInstallation failed. Please check the error messages above.")
        sys.exit(1) # Exit with error code on failure
