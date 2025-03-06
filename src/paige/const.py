import os
import subprocess

PACKAGE_NAME = "paige"
TOOL_DIR_NAME = ".paige"
TOOL_FILE_NAME = "paigefile.py"
MAKEFILE_NAME = "Makefile"

GIT_ROOT = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], text=True, stderr=subprocess.DEVNULL).strip()
TOOL_DIR_PATH = os.path.join(GIT_ROOT, TOOL_DIR_NAME)
TOOL_FILE_PATH = os.path.join(TOOL_DIR_PATH, TOOL_FILE_NAME)
MAKEFILE_PATH = os.path.join(GIT_ROOT, MAKEFILE_NAME)
