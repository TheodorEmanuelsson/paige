import functools
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

_GLOBAL_NAMESPACE = "_global_namespace"

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
