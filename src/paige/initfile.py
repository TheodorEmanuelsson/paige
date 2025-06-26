import os
import subprocess
from paige.const import (
    PAIGE_FILE_NAME,
    UV_CONTENT,
    GITIGNORE_CONTENT,
    PAIGE_FILE_CONTENT,
    GITHUB_URL,
    GITHUB_URL_SHORT,
)
from paige.path import from_paige_dir, from_tools_dir, from_work_dir, from_git_root
from paige.generate import generate_makefiles
from paige.makefile import Makefile


def _init_dot_paige() -> None:
    """Initializes the .paige directory."""
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
    return


def _init_uv(python_version: str) -> None:
    """Initializes a uv pyproject.toml file and creates the environment."""
    paige_path = from_paige_dir()
    pyproject_path = from_paige_dir("pyproject.toml")
    if os.path.exists(pyproject_path):
        print(f"Error: uv pyproject.toml file already exists at: {pyproject_path}")
        return

    try:
        # Create pyproject.toml
        with open(pyproject_path, "w") as f:
            f.write(
                UV_CONTENT.format(
                    python_version=python_version, github_url=GITHUB_URL_SHORT
                )
            )
    except Exception as e:
        print(f"Error generating uv pyproject.toml: {pyproject_path}: {e}")
        return

    try:
        # Change to .paige directory for uv to create venv in the right place
        original_dir = from_work_dir()
        os.chdir(paige_path)
        try:
            # Create the virtual environment
            subprocess.check_call(
                ["uv", "venv", ".venv"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            print(f"Created uv environment in: {os.path.join(paige_path, '.venv')}")

            # Set VIRTUAL_ENV to the new environment and run sync
            venv_path = os.path.join(paige_path, ".venv")
            env = os.environ.copy()
            env["VIRTUAL_ENV"] = venv_path

            # Install paige from GitHub URL
            # _install_paige(venv_path)

            # Sync other dependencies with verbose output
            try:
                result = subprocess.run(
                    ["uv", "sync", "--active"], env=env, capture_output=True, text=True
                )
                if result.returncode != 0:
                    print(f"Error syncing dependencies: {result.stderr}")
                else:
                    print("Synced dependencies in the new environment")
            except Exception as e:
                print(f"Error during sync: {e}")
        finally:
            os.chdir(original_dir)
    except Exception as e:
        print(f"Error setting up uv venv environment: {e}")
        return

    return


def _install_paige(venv_path: str) -> None:
    """Installs paige from GitHub."""
    env = os.environ.copy()
    env["VIRTUAL_ENV"] = venv_path
    try:
        subprocess.check_call(["uv", "pip", "install", f"git+{GITHUB_URL}"], env=env)
        print("Installed paige from GitHub")
    except subprocess.CalledProcessError as e:
        print(f"Error installing paige: {e}")
        # Try to get more detailed error output
        try:
            result = subprocess.run(
                ["uv", "pip", "install", f"git+{GITHUB_URL}"],
                env=env,
                capture_output=True,
                text=True,
            )
            print(f"Error output: {result.stderr}")
        except Exception as e2:
            print(f"Could not get detailed error: {e2}")
    return


def _init_gitignore() -> None:
    """Initializes the .gitignore file."""

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
    """Initial a paigefile.py"""

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


def _init_makefile(tool_folder: str) -> None:
    """Initializes the Makefile."""
    makefile_path = from_git_root("Makefile")
    if os.path.exists(makefile_path):
        print(f"Error: Makefile already exists at: {makefile_path}")
        return

    try:
        # Generate the initial Makefile with the default configuration
        generate_makefiles([Makefile(path=makefile_path, default_target="default")])
        print(f"Generated initial Makefile at: {makefile_path}")
    except Exception as e:
        print(f"Error generating Makefile: {makefile_path}: {e}")
        return

    return


def init_paige(python_version: str) -> None:
    """Initializes a new paige project."""
    _init_dot_paige()
    _init_uv(python_version)
    _init_gitignore()
    _init_paigefile()
    _init_makefile(from_tools_dir())
    return
