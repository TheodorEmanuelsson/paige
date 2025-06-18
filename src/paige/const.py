PACKAGE_NAME = "paige"
PAIGE_DIR_NAME = ".paige"
PAIGE_FILE_NAME = "paigefile.py"
MAKEFILE_NAME = "Makefile"

UV_CONTENT = """\
[project]
name = "build_with_paige"
version = "0.1.0"
description = "A Python build tool inspired by Sage/Mage."
requires-python = ">={python_version}"
dependencies = [
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
