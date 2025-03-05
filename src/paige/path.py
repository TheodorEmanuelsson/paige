import os
import subprocess
from paige.core import (
    GIT_ROOT,
    TOOL_DIR_PATH,
)

def from_work_dir(*path_elems):
    cwd = os.getcwd()
    return os.path.join(cwd, *path_elems)

def from_git_root(*path_elems):
    try:
        git_root = GIT_ROOT
        return os.path.join(git_root, *path_elems)
    except subprocess.CalledProcessError:
        raise Exception("Not in a git repository or git command failed.")

def from_tools_dir(*path_elems):
    tools_dir = from_git_root(TOOL_DIR_PATH, "tools")
    path = os.path.join(tools_dir, *path_elems)
    ensure_parent_dir(path)
    return path

def from_bin_dir(*path_elems):
    bin_dir = from_git_root(TOOL_DIR_PATH, "bin")
    path = os.path.join(bin_dir, *path_elems)
    ensure_parent_dir(path)
    return path

def from_build_dir(*path_elems):
    build_dir = from_git_root(TOOL_DIR_PATH, "build")
    path = os.path.join(build_dir, *path_elems)
    ensure_parent_dir(path)
    return path

def ensure_parent_dir(path):
    parent_dir = os.path.dirname(path)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)
