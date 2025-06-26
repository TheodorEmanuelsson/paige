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
@click.argument("package_name")
def install(package_name: str):
    """Installs a package into the .paige virtual environment."""
    paige_dir = from_paige_dir()
    pyproject_path = os.path.join(paige_dir, "pyproject.toml")

    if not os.path.exists(pyproject_path):
        click.echo(
            f"pyproject.toml not found in {paige_dir}. Make sure the environment is initialized."
        )
        sys.exit(1)

    try:
        # Add package to pyproject.toml
        result = subprocess.run(
            ["uv", "add", package_name], cwd=paige_dir, capture_output=True, text=True
        )

        if result.returncode != 0:
            click.echo(f"Error adding package: {result.stderr}")
            sys.exit(result.returncode)

        click.echo(f"Successfully added {package_name} to pyproject.toml")
        click.echo("Package is now available in the .paige environment")

    except Exception as e:
        click.echo(f"Error installing package: {e}")
        sys.exit(1)


@cli.command()
@click.argument("python_version")
def init(python_version: str):
    """Initializes paige tool in the project."""
    init_paige(python_version)


@cli.command()
@click.argument("target")
@click.argument("args", nargs=-1)
def run(target, args):
    """Generates the temp file, runs the target, and deletes the temp file."""
    import paige as pg
    import subprocess

    ctx = {}
    executable_path = pg.create_generating_paigefile()
    try:
        cmd = [executable_path, target] + list(args)
        result = subprocess.run(cmd)
        sys.exit(result.returncode)
    finally:
        try:
            os.remove(executable_path)
        except Exception:
            pass


if __name__ == "__main__":
    cli()
