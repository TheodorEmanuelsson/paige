import os
import inspect
import importlib.util
from paige.const import TOOL_DIR_PATH

def scan_py_files(folder):
    """Scans .py files in a folder and returns a list of file paths."""
    py_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".py") and file != "paigefile.py":
                py_files.append(os.path.join(root, file))
    return py_files


def _discover_all_task_functions():
    """Scans .py files in .paige folder and returns a dictionary of task functions."""
    task_functions = {}
    paige_folder = TOOL_DIR_PATH
    py_files_found = scan_py_files(paige_folder)

    if not py_files_found:
        return task_functions

    for py_file_path in py_files_found:
        module_name = os.path.splitext(os.path.basename(py_file_path))[0] # Filename w/o .py
        spec = importlib.util.spec_from_file_location(module_name, py_file_path) # Create module spec
        module = importlib.util.module_from_spec(spec) # Create module object
        spec.loader.exec_module(module) # Load module from file

        for name, obj in inspect.getmembers(module): # Inspect members of the module
            if inspect.isfunction(obj) and name != "main" and not name.startswith("_"): # Check function criteria
                task_functions[name] = obj # Add function to task_functions dict

    return task_functions


def _discover_task_function(task_name):
    """Dynamically discovers a task function by name."""
    task_functions = _discover_all_task_functions()
    return task_functions.get(task_name) # Return function or None if not found
