import os
import click
import subprocess
import sys

from paige.path import from_paige_dir
from paige.initfile import init_paige

@click.group()
def cli():
    pass

@cli.command()
@click.argument('package_name')
def install(package_name:str):
    """Installs a package into the .paige virtual environment."""
    pass


@cli.command()
@click.argument('python_version')
def init(python_version:str):
    """Initializes paige tool in the project."""
    init_paige(python_version)

if __name__ == '__main__':
    cli()
