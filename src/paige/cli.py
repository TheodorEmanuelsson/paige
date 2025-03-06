import os
import click
import subprocess
import sys

from paige.const import (
    TOOL_DIR_NAME,
    TOOL_DIR_PATH,
)
from paige.initfile import generate_init_file

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
def init():
    """Initializes paige tool in the project."""
    tool_name = TOOL_DIR_NAME
    tool_path = TOOL_DIR_PATH

    click.echo(f"Initializing '{tool_name}' tool environment at {tool_path}...")

    generate_init_file()

    click.echo(f"Paige tool initialized in '{tool_path}'.")
    click.echo(f"Edit '.paige/paigefile.py' to define your tasks and Makefiles.")


if __name__ == '__main__':
    cli()
