import os

from paige.core import (
    TOOL_DIR_PATH,
    Makefile
)

def scan_py_files():
    """Scans for .py files in the tool dir."""
    py_files = []
    for filename in os.listdir(TOOL_DIR_PATH):
        if filename.endswith(".py") and filename != "pagefile.py":
            filepath = os.path.join(TOOL_DIR_PATH, filename)
            if os.path.isfile(filepath):
                py_files.append(filename)
    return py_files

def generate_makefiles(*makefiles: Makefile):
    for makefile_config in makefiles:
        makefile_content = f"""\
.PHONY: all {makefile_config.default_target}

all: {makefile_config.default_target}

{makefile_config.default_target}:
\t@echo "Running tasks for Makefile: {makefile_config.path} (Namespace: {makefile_config.namespace})"
\t@# Placeholder:  Command to execute tasks for this Makefile/Namespace will go here
\t@echo "To implement: Execute tasks from namespace '{makefile_config.namespace}' and generate rules..."
"""
        makefile_path = makefile_config.path
        try:
            with open(makefile_path, "w") as f:
                f.write(makefile_content)
            print(f"Generated Makefile: {makefile_path}")
        except Exception as e:
            print(f"Error generating Makefile: {makefile_path}: {e}")
