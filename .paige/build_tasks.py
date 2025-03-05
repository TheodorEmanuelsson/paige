# .paige/build_tasks.py

from paige.core import task, task_manager

@task(description="Compile the main application code.")
def compile_code():
    """Simulates compiling code."""
    print("Simulating: Compiling application code...")

@task(dependencies=["compile_code"], description="Package the application for distribution.")
def package_app():
    """Simulates packaging the application."""
    print("Simulating: Packaging application...")

@task(dependencies=["package_app", "compile_code"], description="Build the entire application (compile and package).", public=False) # Example of a non-public task
def build_all():
    """Builds the entire application by running compile_code and package_app."""
    print("Simulating: Building all components...")
