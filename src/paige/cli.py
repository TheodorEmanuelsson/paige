import os
import click
import subprocess
import sys

from paige.path import from_paige_dir
from paige.initfile import generate_init_file

@click.group()
def cli():
    pass

@cli.command()
@click.argument('package_name')
def install(package_name):
    """Installs a package into the .paige virtual environment."""
    tool_path = from_paige_dir()

    target_pip_executable = os.path.join(tool_path, "bin", "pip")
    click.echo(f"Installing package '{package_name}' into the paige virtual environment...")

    try:
        subprocess.check_call([target_pip_executable, "install", package_name])
        click.echo(f"Package '{package_name}' successfully installed in the paige virtual environment.")
    except subprocess.CalledProcessError as e:
        click.secho(f"Error installing package '{package_name}' into virtual environment: {e}", fg='red')
    except FileNotFoundError:
        click.secho(f"Error: pip executable not found in paige virtual environment.", fg='red')


@cli.command()
def init():
    """Initializes paige tool in the project."""
    tool_path = from_paige_dir()

    click.echo(f"Initializing paige environment at {tool_path}...")

    generate_init_file()

    click.echo(f"Paige initialized in '{tool_path}'.")

if __name__ == '__main__':
    cli()
