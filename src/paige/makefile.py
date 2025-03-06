# src/paige/makefile.py
import os
import inspect
import re
from paige.const import TOOL_DIR_NAME, TOOL_DIR_PATH
from paige.path import from_git_root
from paige import discover


DEFAULT_GO_VERSION = "1.23.4"
TOOL_FOLDER_NAME = ".paige"

class MakefileConfig:
    def __init__(self, path, default_target, namespace=None):
        self.path = path
        self.default_target = default_target
        self.namespace = namespace

    def get_namespace_name(self):
        if self.namespace is None:
            return ""
        return str(self.namespace).split('.')[-1]

    def get_default_target_name(self):
        if self.default_target is None:
            return ""
        target_name = self.default_target.__name__
        target_name = re.sub(r'^main\.', '', target_name)
        target_name = re.sub(r'^' + re.escape(self.get_namespace_name()) + r'\.', '', target_name)
        target_name = target_name.split('-')[0]
        if not re.match(r'^[a-zA-Z]+$', target_name):
            raise ValueError(f"Invalid default target name: {target_name}")
        return target_name


def generate_makefile(makefile_config, additional_makefile_configs=None):
    if additional_makefile_configs is None:
        additional_makefile_configs = []

    makefile_path = makefile_config.path
    include_path_rel = os.path.relpath(from_git_root(".paige"), os.path.dirname(makefile_path))

    makefile_content = f"""\
TOOL_FOLDER_NAME := {TOOL_FOLDER_NAME}

# To learn more, see {include_path_rel}/paigefile.py and [paige documentation - TODO: add link].
"""

    if makefile_config.get_default_target_name():
        makefile_content += f"""
.DEFAULT_GOAL := {to_make_target(makefile_config.get_default_target_name())}
"""

    makefile_content += f"""
cwd := $(dir $(realpath $(firstword $(MAKEFILE_LIST))))
paigefile := $(abspath $(cwd)/{os.path.join(include_path_rel, "bin", "paige")})

# Setup Python virtual environment
VENV_NAME := {TOOL_FOLDER_NAME}
VENV_BIN_DIR := $$(pwd)/$(VENV_NAME)/bin
PYTHON := $$(VENV_BIN_DIR)/python

.PHONY: $(paigefile)
$(paigefile):
\t@echo "Building paige tool..."
\t@$(PYTHON) -m venv $(VENV_NAME) --prompt {TOOL_DIR_NAME}
\t@$(VENV_BIN_DIR)/pip install --upgrade pip
\t@$(VENV_BIN_DIR)/pip install -e {os.path.relpath(from_git_root('.'), os.path.dirname(makefile_path))}

.PHONY: paige
paige: $(paigefile)
\t@$(MAKE) $(paigefile) -- --paige-run

.PHONY: update-paige
update-paige: $(paigefile)
\t@echo "Updating paige tool..."
\t@cd {include_path_rel} && $(PYTHON) -m pip install --upgrade -e .
\t@$(MAKE) paige


.PHONY: clean-paige
clean-paige:
\t@echo "Cleaning paige build output..."
\t@rm -rf {os.path.join(include_path_rel, "tools")} {os.path.join(include_path_rel, "bin")} {os.path.join(include_path_rel, "build")}


# Task targets will be generated below this line ### TASK_TARGETS_START ###
### TASK_TARGETS_START ###
""" # Task targets marker

    task_targets_content = ""
    all_task_functions = discover._discover_all_task_functions() # Get tasks using discover module

    for task_name, task_function in all_task_functions.items():
        target_name = to_make_target(task_name)

        # Construct command to execute the Python function directly using paigefile.py
        task_command = f"""\
\t@echo "Executing task: {task_name}"
\t@source {TOOL_FOLDER_NAME}/bin/activate && python -c "from .paige import paigefile; paigefile.{task_name}(__import__('contextvars').Context())"
""" # Call function from paigefile.py

        task_targets_content += f"""
.PHONY: {target_name}
{target_name}: paige
{task_command}
"""

    # Insert task targets into Makefile content at the marker
    makefile_content = makefile_content.replace("### TASK_TARGETS_START ###", task_targets_content)


    if not makefile_config.get_namespace_name():
        for sub_makefile_config in additional_makefile_configs:
            if not sub_makefile_config.get_namespace_name():
                continue

            makefile_dir_rel = os.path.relpath(from_git_root('.'), os.path.dirname(makefile_config.path))
            sub_makefile_rel_path = os.path.relpath(sub_makefile_config.path, makefile_config.path)
            makefile_content += f"""

.PHONY: {to_make_target(sub_makefile_config.get_namespace_name())}
{to_make_target(sub_makefile_config.get_namespace_name())}:
\t@$(MAKE) -C {makefile_dir_rel} -f {sub_makefile_rel_path}
"""


    makefile_content += """
.PHONY: help
help:
\t@echo "Targets:"
\t@grep -oE '^[a-z-]+:.*?## .*$$' Makefile | sed 's/\\s+##\\s+/ /'
"""

    try:
        os.makedirs(os.path.dirname(makefile_path), exist_ok=True)
        with open(makefile_path, "w") as f:
            f.write(makefile_content)
        print(f"Generated Makefile: {makefile_path}")
    except Exception as e:
        print(f"Error generating Makefile: {makefile_path}: {e}")



def to_make_vars(args):
    return []

def to_paige_function(target, args):
    return target

def to_make_target(name):
    output = name
    if ":" in name:
        output = name.split(":")[1]
    output = output.replace("_", "-")
    return output.lower()
