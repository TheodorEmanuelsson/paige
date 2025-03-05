import subprocess
import os
import logging

from paige.path import from_git_root, from_bin_dir

def command(path, *args):
    cmd_env = os.environ.copy()
    bin_dir = from_bin_dir()
    cmd_env['PATH'] = os.pathsep.join([bin_dir, cmd_env['PATH']])

    process = subprocess.Popen([path, *args],
                               cwd=from_git_root("."),
                               env=cmd_env,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               text=True)

    return process

def output(process):
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        error_message = f"Command failed: {process.args}\nReturn Code: {process.returncode}\nStdout:\n{stdout}\nStderr:\n{stderr}"
        raise Exception(error_message)
    return stdout.strip()

def prepend_path(environ, *paths):
    path_value = environ.get("PATH", "")
    environ["PATH"] = os.pathsep.join(list(paths) + [path_value])
    return environ
