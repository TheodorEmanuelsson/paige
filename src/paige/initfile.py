import os
import sys
import subprocess
from paige.const import PAIGE_FILE_NAME, UV_CONTENT, GITIGNORE_CONTENT, PAIGE_FILE_CONTENT
from paige.path import from_paige_dir, from_tools_dir, from_work_dir

def _init_dot_paige() -> None:
    '''Initializes the .paige directory.'''
    paige_path = from_paige_dir()
    if os.path.exists(paige_path):
        print(f"Error: .paige directory already exists at: {paige_path}")
        return

    try:
        os.makedirs(paige_path, exist_ok=True)
        print(f"Initialized .paige directory at: {paige_path}")
    except Exception as e:
        print(f"Error creating .paige directory: {e}")
        return

def _init_uv(python_version:str) -> None:
    '''Initializes a uv pyproject.toml file and creates the environment.'''
    paige_path = from_paige_dir()
    pyproject_path = from_paige_dir("pyproject.toml")
    if os.path.exists(pyproject_path):
        print(f"Error: uv pyproject.toml file already exists at: {pyproject_path}")
        return

    try:
        # Create pyproject.toml
        with open(pyproject_path, "w") as f:
            f.write(UV_CONTENT.format(python_version=python_version))
    except Exception as e:
        print(f"Error generating uv pyproject.toml: {pyproject_path}: {e}")
        return

    try:
        # Change to .paige directory for uv to create venv in the right place
        original_dir = from_work_dir()
        os.chdir(paige_path)
        try:
            subprocess.check_call(['uv', 'venv', '.venv'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"Created uv environment in: {os.path.join(paige_path, '.venv')}")
        finally:
            os.chdir(original_dir)
    except Exception as e:
        print(f"Error setting up uv venv environment: {e}")
        return

    return

def _init_gitignore() -> None:
    '''Initializes the .gitignore file.'''

    gitignore_path = from_paige_dir(".gitignore")
    if os.path.exists(gitignore_path):
        print(f"Error: .gitignore file already exists at: {gitignore_path}")
        return

    try:
        with open(gitignore_path, "w") as f:
            f.write(GITIGNORE_CONTENT)
    except Exception as e:
        print(f"Error generating .gitignore: {gitignore_path}: {e}")
        return

    return

def _init_paigefile():
    '''Initial a paigefile.py'''

    paigefile_path = from_paige_dir(PAIGE_FILE_NAME)
    if os.path.exists(paigefile_path):
        print(f"Error: paigefile.py already exists at: {paigefile_path}")
        return

    try:
        with open(paigefile_path, "w") as f:
            f.write(PAIGE_FILE_CONTENT)
    except Exception as e:
        print(f"Error generating paigefile: {paigefile_path}: {e}")
        return

    return

def _init_makefile(tool_folder:str) -> None:
    '''Initializes the Makefile.'''
    pass

def init_paige(python_version:str) -> None:
    '''Initializes a new paige project.'''

    _init_dot_paige()
    _init_uv(python_version)
    _init_gitignore()
    _init_paigefile()
    _init_makefile(from_tools_dir())
    return
