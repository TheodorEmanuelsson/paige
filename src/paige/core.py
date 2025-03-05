import os
import functools
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

PACKAGE_NAME = "paige"
TOOL_DIR_NAME = ".paige"
TOOL_FILE_NAME = "paigefile.py"
MAKEFILE_NAME = "Makefile"

GIT_ROOT = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], text=True, stderr=subprocess.DEVNULL).strip()
TOOL_DIR_PATH = os.path.join(GIT_ROOT, TOOL_DIR_NAME)
TOOL_FILE_PATH = os.path.join(TOOL_DIR_PATH, TOOL_FILE_NAME)
MAKEFILE_PATH = os.path.join(GIT_ROOT, MAKEFILE_NAME)

_GLOBAL_NAMESPACE = "_global_namespace"

class Makefile:
    """
    Represents the configuration for generating a Makefile.
    """
    def __init__(self, path, default_target, namespace="_global_namespace"):
        """
        Initializes a Makefile configuration.

        Args:
            path (str): The path where the Makefile should be created (e.g., "Makefile", "terraform/Makefile").
            default_target (str): The default target to be executed when 'make' is run (e.g., "all").
            namespace (str, optional): The namespace for tasks in this Makefile.
                                         Defaults to "_global_namespace".
        """
        self.path = path
        self.default_target = default_target
        self.namespace = namespace

class TaskManager:
    def __init__(self):
        """Initializes the TaskManager with an empty task registry."""
        self._tasks = {}

    def task(self, dependencies=None, description="", namespace=_GLOBAL_NAMESPACE, public=True):
        """Decorator to register a task."""
        if dependencies is None:
            dependencies = []

        def decorator(func):
            if namespace not in self._tasks:
                self._tasks[namespace] = {}
            self._tasks[namespace][func.__name__] = {
                "func": func,
                "dependencies": dependencies,
                "description": description,
                "public": public,
            }
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                logging.info("Executing task: %s:%s", namespace, func.__name__)
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def execute_task(self, task_name, namespace=_GLOBAL_NAMESPACE):
        """Executes a task and its dependencies."""
        if namespace not in self._tasks or task_name not in self._tasks[namespace]:
            raise ValueError(f"Task '{task_name}' not found in namespace '{namespace}'.")

        task_data = self._tasks[namespace][task_name]
        for dependency in task_data["dependencies"]:
            dep_namespace, dep_task_name = dependency.split(":") if ":" in dependency else (
                _GLOBAL_NAMESPACE, dependency
            )
            self.execute_task(dep_task_name, dep_namespace)

        task_data["func"]()

    def get_all_tasks(self):
        """Returns the dictionary of all registered tasks."""
        return self._tasks

task_manager = TaskManager()

task = task_manager.task
execute_task = task_manager.execute_task
get_all_tasks = task_manager.get_all_tasks
