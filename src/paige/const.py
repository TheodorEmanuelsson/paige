PACKAGE_NAME = "paige"
PAIGE_DIR_NAME = ".paige"
PAIGE_FILE_NAME = "paigefile.py"
MAKEFILE_NAME = "Makefile"
GITHUB_URL = "https://github.com/TheodorEmanuelsson/paige.git"
GITHUB_URL_SHORT = f"git+{GITHUB_URL}"


UV_CONTENT = """\
[project]
name = "dot_paige"
version = "0.1.0"
description = "A Python build tool inspired by Sage/Mage."
requires-python = ">={python_version}"
dependencies = [
   "paige @ {github_url}"
]
"""

GITIGNORE_CONTENT = """\
/.gitignore
/bin
/include
/lib
pyvenv.cfg
.venv/
"""

PAIGE_FILE_CONTENT = """\
import paige as pg

def main():
    pass

if __name__ == "__main__":
    pass
"""
