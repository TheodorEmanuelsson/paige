import os
import click
import subprocess
import sys

PACKAGE_NAME = "paige"
TOOL_FOLDER_NAME = ".paige"
TOOL_FILE_NAME = "paigefile.py"
MAKEFILE_NAME = "Makefile"

@click.group()
def cli():
    pass

@cli.command()
@click.option('--dev', is_flag=True, default=False, help='Install paige in development mode (local install).')
def init(dev:bool):
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

    # 3. Install 'paige' package into the .paige virtual environment (conditional install based on --dev flag)
    target_pip_executable = os.path.join(tool_folder, "bin", "pip")
    package_name_to_install = PACKAGE_NAME # Use PACKAGE_NAME constant
    click.echo(f"Installing package '{package_name_to_install}' into the virtual environment...")
    try:
        if dev: # Check if --dev flag is True
            click.echo("Installing in development mode (local install)...")
            subprocess.check_call([target_pip_executable, "install", "."]) # Local install
            click.echo(f"Package '{package_name_to_install}' installed in the virtual environment from local project (dev mode).")
        else:
            click.echo("Installing from PyPI (or package index)...")
            subprocess.check_call([target_pip_executable, "install", package_name_to_install]) # Install from PyPI
            click.echo(f"Package '{package_name_to_install}' installed in the virtual environment from package index.")
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
    makefile_content = f"""\
.PHONY:
paige:
\t@source {TOOL_FOLDER_NAME}/bin/activate && python {TOOL_FOLDER_NAME}/{TOOL_FILE_NAME} --paige-run
"""
    try:
        with open(MAKEFILE_NAME, "w") as f:
            f.write(makefile_content)
        click.echo(f"Created initial {MAKEFILE_NAME} in the project root (separated default and 'paige' targets).")
        click.echo(f"File created at: {os.path.abspath(MAKEFILE_NAME)}")
    except Exception as e:
        click.secho(f"Error creating {MAKEFILE_NAME}: {e}", fg='yellow')

if __name__ == '__main__':
    cli()
