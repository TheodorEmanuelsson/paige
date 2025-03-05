import os

def scan_py_files(page_folder:str):
    """Scans for .py files in the specified page folder and returns their names."""
    py_files = []
    for filename in os.listdir(page_folder):
        if filename.endswith(".py") and filename != "pagefile.py":
            filepath = os.path.join(page_folder, filename)
            if os.path.isfile(filepath):
                py_files.append(filename)
    return py_files

def generate_makefiles(*makefiles):
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
