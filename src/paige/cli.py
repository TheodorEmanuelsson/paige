import os
import click
import subprocess
import sys

TOOL_FOLDER_NAME = ".paige"
TOOL_FILE_NAME = "paigefile.py"
MAKEFILE_NAME = "Makefile"

@click.group()
def cli():
    pass

@cli.command()
def init():
    """Initializes paige"""
    tool_folder = TOOL_FOLDER_NAME
    tool_path = os.path.abspath(tool_folder)

    click.echo(f"Initializing '{TOOL_FOLDER_NAME}' tool environment in the current project directory...")
    click.echo(f"Folder will be created at: {tool_path}")

    # Create .paige folder in project root
    os.makedirs(tool_folder, exist_ok=True)
    click.echo(f"Created folder: {tool_folder}")

    # Create virtual environment inside .paige folder in project root
    venv_path = os.path.join(tool_folder) # venv in .paige in project root
    click.echo(f"Creating virtual environment in: {venv_path}")
    try:
        subprocess.check_call([sys.executable, "-m", "venv", venv_path])
        click.echo("Virtual environment created.")
    except subprocess.CalledProcessError as e:
        click.secho(f"Error creating virtual environment: {e}", fg='red')
        return

    # Install 'paige' package into the .paige virtual environment
    target_pip_executable = os.path.join(tool_folder, "bin", "pip")
    package_name_to_install = "paige"
    click.echo(f"Installing package '{package_name_to_install}' into the virtual environment...")
    try:
        subprocess.check_call([target_pip_executable, "install", package_name_to_install])
        click.echo(f"Package '{package_name_to_install}' installed in the virtual environment.")
    except subprocess.CalledProcessError as e:
        click.secho(f"Error installing package '{package_name_to_install}' into virtual environment: {e}", fg='red')
        return

    # Create .gitignore file inside .paige folder
    gitignore_path = os.path.join(tool_path, ".gitignore")
    ignores = "\n".join([
        ".gitignore",
        "bin/",
        "include/",
        "lib/",
        "pyvenv.cfg",
    ])
    try:
        with open(gitignore_path, "w") as f:
            f.write(ignores)
    except Exception as e:
        click.secho(f"Error creating .gitignore inside '{TOOL_FOLDER_NAME}': {e}", fg='yellow')

    # Create a paigefile.py
    paigefile_path = os.path.join(tool_path, TOOL_FILE_NAME)
    try:
        with open(paigefile_path, "w") as f:
            f.write("import paige")
        click.echo(f"Created empty paigefile.py in '{TOOL_FOLDER_NAME}' folder.")
        click.echo(f"File created at: {paigefile_path}")
    except Exception as e:
        click.secho(f"Error creating paigefile.py in '{TOOL_FOLDER_NAME}': {e}", fg='yellow')

    # Create initial Makefile in the project root
    makefile_path = os.path.join(tool_path, MAKEFILE_NAME)
    makefile_content = f"""\
.PHONY: all run

all: help

help:
\t@echo "Usage: make <target>"
\t@echo "Targets:"
\t@echo "  run: Execute tasks defined in {TOOL_FILE_NAME}"
\t@echo "  help: Show this help message"

run:
\t@echo "Executing tasks from {TOOL_FILE_NAME}..."
\t@source {TOOL_FOLDER_NAME}/bin/activate && python {TOOL_FOLDER_NAME}/{TOOL_FILE_NAME}  # Activate venv and run paigefile.py
"""
    try:
        with open(makefile_path, "w") as f:
            f.write(makefile_content)
        click.echo(f"Created initial {MAKEFILE_NAME} in the project root.")
        click.echo(f"File created at: {os.path.abspath(makefile_path)}")
    except Exception as e:
        click.secho(f"Error creating {MAKEFILE_NAME}: {e}", fg='yellow')

if __name__ == '__main__':
    cli()
