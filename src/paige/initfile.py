import os
import sys
import subprocess
from paige.const import PAIGE_FILE_NAME
from paige.path import from_paige_dir

def _init_dot_paige() -> None:
    '''Initializes the .paige directory.'''
    paige_path = from_paige_dir()
    if not os.path.exists(paige_path):
        print(f"Error: Tool folder not found at: {paige_path}. Run 'paige init' first.")
        return

    paige_folder = os.path.join(paige_path, ".paige")
    if os.path.exists(paige_folder):
        print(f"Error: .paige directory already exists at: {paige_folder}")
        return

    os.makedirs(paige_folder, exist_ok=True)
    return

def _init_virtualenv() -> None:
    '''Initializes the virtual environment.'''
    paige_path = from_paige_dir()
    if os.path.exists(paige_path):
        print(f"Error: Virtual environment already exists at: {paige_path}")
        return

    try:
        subprocess.check_call([sys.executable, "-m", "venv", paige_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Created virtual environment in: {paige_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment: {e}")
        return
    except FileNotFoundError:
        print("Error: Python 'venv' module not found. Ensure Python 3 and 'venv' are installed.")
        return

    return

def _init_gitignore() -> None:
    '''Initializes the .gitignore file.'''

    gitignore_content = f"""\
/.gitignore
/bin
/include
/lib
pyvenv.cfg
"""
    gitignore_path = from_paige_dir(".gitignore")
    if os.path.exists(gitignore_path):
        print(f"Error: .gitignore file already exists at: {gitignore_path}")
        return
    
    try:
        with open(gitignore_path, "w") as f:
            f.write(gitignore_content)
    except Exception as e:
        print(f"Error generating .gitignore: {gitignore_path}: {e}")
        return
    
    return

def _init_paigefile()
    '''Initial a paigefile.py'''

    paigefile_content = """\
import paige as pg


if __name__ == "__main__":
    pass
""" 
    paigefile_path = from_paige_dir(PAIGE_FILE_NAME)
    if os.path.exists(paigefile_path):
        print(f"Error: paigefile.py already exists at: {paigefile_path}")
        return
    
    try:
        with open(paigefile_path, "w") as f:
            f.write(paigefile_content)
    except Exception as e:
        print(f"Error generating paigefile: {paigefile_path}: {e}")
        return
    
    return

def _init_makefile(tool_folder:str) -> None:
    '''Initializes the Makefile.'''
    pass

def init_paige() -> None:
    '''Initializes a new paige project.'''
    _init_dot_paige()
    _init_virtualenv()
    _init_gitignore()
    _init_paigefile()
    _init_makefile()
    return