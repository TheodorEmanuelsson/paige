import os
import click
import subprocess
import sys

from paige.core import (
    PACKAGE_NAME,
    TOOL_DIR_NAME,
    TOOL_DIR_PATH,
    MAKEFILE_PATH,
)

@click.group()
def cli():
    pass

@cli.command()
@click.argument('package_name')
def install(package_name):
    """Installs a package into the .paige virtual environment."""
    tool_name = TOOL_DIR_NAME
    tool_path = TOOL_DIR_PATH

    target_pip_executable = os.path.join(tool_path, "bin", "pip")
    click.echo(f"Installing package '{package_name}' into the '{tool_name}' virtual environment...")

    try:
        subprocess.check_call([target_pip_executable, "install", package_name])
        click.echo(f"Package '{package_name}' successfully installed in the '{tool_name}' virtual environment.")
    except subprocess.CalledProcessError as e:
        click.secho(f"Error installing package '{package_name}' into virtual environment: {e}", fg='red')
    except FileNotFoundError:
        click.secho(f"Error: pip executable not found in '{tool_name}' virtual environment.", fg='red')


@cli.command()
@click.option('--dev', is_flag=True, default=False, help='Install paige in development mode (local install).')
def init(dev:bool):
    """Initializes paige"""
    package = PACKAGE_NAME
    tool_name = TOOL_DIR_NAME
    tool_path = TOOL_DIR_PATH

    click.echo(f"Initializing '{tool_name}' tool environment at {tool_path}...")

    # Create .paige folder in project root
    os.makedirs(tool_path, exist_ok=True)

    # Create virtual environment inside .paige folder in project root
    venv_path = tool_path
    click.echo(f"Creating virtual environment in: {venv_path}")
    try:
        subprocess.check_call([sys.executable, "-m", "venv", venv_path])
        click.echo("Virtual environment created.")
    except subprocess.CalledProcessError as e:
        click.secho(f"Error creating virtual environment: {e}", fg='red')
        return

    # Install 'paige' package into the .paige virtual environment (conditional install based on --dev flag)
    target_pip_executable = os.path.join(tool_path, "bin", "pip")
    package_name_to_install = package
    click.echo(f"Installing package '{package_name_to_install}' into the virtual environment...")
    try:
        if dev:
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
        click.secho(f"Error creating .gitignore inside '{tool_name}': {e}", fg='yellow')

    # Create a paigefile.py
    paigefile_contents = """
import paige as pg

def main():
    pg.generate_makefiles(
        pg.Makefile(
            path = pg.from_git_root("Makefile),
            default_target = all()
    ),
)

pg.task()
def all():
    pass
"""
    try:
        with open(tool_path, "w") as f:
            f.write(paigefile_contents)
        click.echo(f"Created empty paigefile.py in '{tool_name}' folder.")
        click.echo(f"File created at: {tool_path}")
    except Exception as e:
        click.secho(f"Error creating paigefile.py in '{tool_name}': {e}", fg='yellow')

    # Create initial Makefile in the project root
    makefile_content = f"""\
.PHONY:
paige:
\t@echo testing
"""
    try:
        with open(MAKEFILE_PATH, "w") as f:
            f.write(makefile_content)
        click.echo(f"Created initial {MAKEFILE_PATH} at git root.")
    except Exception as e:
        click.secho(f"Error creating {MAKEFILE_PATH}: {e}", fg='yellow')

if __name__ == '__main__':
    cli()
