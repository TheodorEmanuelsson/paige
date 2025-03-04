import os
import click
import subprocess
import sys

TOOL_FOLDER_NAME = ".page"
PAGEFILE_NAME = "pagefile.py"

@click.group()
def cli():
    pass

@cli.command()
def init():
    """Initializes page"""
    tool_folder = TOOL_FOLDER_NAME
    tool_path = os.path.abspath(tool_folder)

    click.echo(f"Initializing '{TOOL_FOLDER_NAME}' tool environment in the current project directory...")
    click.echo(f"Folder will be created at: {tool_path}")

    # Create .page folder in project root
    os.makedirs(tool_folder, exist_ok=True)
    click.echo(f"Created folder: {tool_folder}")

    # Create virtual environment inside .page folder in project root
    venv_path = os.path.join(tool_folder) # venv in .page in project root
    click.echo(f"Creating virtual environment in: {venv_path}")
    try:
        subprocess.check_call([sys.executable, "-m", "venv", venv_path])
        click.echo("Virtual environment created.")
    except subprocess.CalledProcessError as e:
        click.secho(f"Error creating virtual environment: {e}", fg='red')
        return

    # Install 'page' package into the .page virtual environment
    target_pip_executable = os.path.join(tool_folder, "bin", "pip")
    package_name_to_install = "page"
    click.echo(f"Installing package '{package_name_to_install}' into the virtual environment...")
    try:
        subprocess.check_call([target_pip_executable, "install", package_name_to_install])
        click.echo(f"Package '{package_name_to_install}' installed in the virtual environment.")
    except subprocess.CalledProcessError as e:
        click.secho(f"Error installing package '{package_name_to_install}' into virtual environment: {e}", fg='red')
        return

    # Create .gitignore file inside .page folder
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

    # Create a pagefile.py
    pagefile_path = os.path.join(tool_path, PAGEFILE_NAME)
    try:
        with open(pagefile_path, "w") as f:
            f.write("import page")
        click.echo(f"Created empty pagefile.py in '{TOOL_FOLDER_NAME}' folder.")
        click.echo(f"File created at: {pagefile_path}")
    except Exception as e:
        click.secho(f"Error creating pagefile.py in '{TOOL_FOLDER_NAME}': {e}", fg='yellow')

if __name__ == '__main__':
    cli()
