import os
import subprocess

from paige.const import PAIGE_DIR_NAME

def from_work_dir(*path_elems:str|None) -> str:
    cwd = os.getcwd()
    return cwd if not path_elems else os.path.join(cwd, *path_elems)

def from_git_root(*path_elems:str|None)->str:
    try:
        git_root_bytes = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], stderr=subprocess.DEVNULL)
        git_root = git_root_bytes.decode('utf-8').strip()
        return os.path.join(git_root, *path_elems)
    except subprocess.CalledProcessError:
        raise Exception("Not in a git repository or git command failed.")

def from_paige_dir(*path_elems:str|None):
    if not path_elems:
        return from_git_root(PAIGE_DIR_NAME)
    return from_git_root(PAIGE_DIR_NAME, *path_elems)

def from_tools_dir(*path_elems:str|None)->str:
    path = from_paige_dir("tools", *path_elems)
    ensure_parent_dir(path)
    return path

def from_bin_dir(*path_elems:str|None)->str:
    path = from_paige_dir("bin", *path_elems)
    ensure_parent_dir(path)
    return path

def from_build_dir(*path_elems:str|None)->str:
    path = from_paige_dir("build", *path_elems)
    ensure_parent_dir(path)
    return path

def ensure_parent_dir(path:str)->None:
    parent_dir = os.path.dirname(path)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

if __name__ == "__main__":
    print("from_work_dir():", from_work_dir())
    print("from_git_root():", from_git_root())
    print("from_paige_dir():", from_paige_dir())
    print("from_tools_dir():", from_tools_dir())
    print("from_bin_dir():", from_bin_dir())
    print("from_build_dir():", from_build_dir())
