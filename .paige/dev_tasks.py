# .paige/dev_tasks.py

from paige.core import task, task_manager

@task(description="Run unit tests for the project.")
def run_tests():
    """Simulates running unit tests."""
    print("Simulating: Running unit tests...")

@task(description="Start the development server for local testing.")
def start_dev_server():
    """Simulates starting a development server."""
    print("Simulating: Starting development server...")

@task(description="Run code linters and formatters.")
def lint_and_format():
    """Simulates running linters and formatters."""
    print("Simulating: Running linters and formatters (e.g., flake8, black)...")
