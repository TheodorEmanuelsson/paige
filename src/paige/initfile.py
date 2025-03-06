import os
import sys
import subprocess
import contextvars
from paige.logger import new_logger, with_logger, logger
from paige.const import TOOL_DIR_NAME, TOOL_DIR_PATH


STRING_TYPE = "string"
INT_TYPE = "int"
BOOL_TYPE = "bool"


def generate_init_file():
    """Generates the initial paigefile.py, .paige directory, venv, and .gitignore."""
    tool_folder = TOOL_DIR_NAME
    os.makedirs(tool_folder, exist_ok=True)

    # Create virtual environment
    venv_path = os.path.join(tool_folder)
    print(f"Debug: Creating venv in: {venv_path}")
    try:
        subprocess.check_call([sys.executable, "-m", "venv", venv_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Created virtual environment in: {venv_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment: {e}")
        print(f"Debug: subprocess.CalledProcessError: {e}")
        return
    except FileNotFoundError:
        print("Error: Python 'venv' module not found. Ensure Python 3 and 'venv' are installed.")
        print("Debug: FileNotFoundError: venv module not found")
        return
    print(f"Debug: Venv creation successful")


    # Generate paigefile.py
    paigefile_content = """\
import paige as pg

makefiles_config = [
    pg.MakefileConfig(
        path="Makefile",
        default_target="default_task", # Example default target
    ),
]
"""
    paigefile_path = os.path.join(tool_folder, "paigefile.py")
    try:
        with open(paigefile_path, "w") as f:
            f.write(paigefile_content)
    except Exception as e:
        print(f"Error generating paigefile: {paigefile_path}: {e}")
        print(f"Debug: paigefile generation exception: {e}")
        return

    # Generate .gitignore
    gitignore_content = f"""\
/.gitignore
/bin
/include
/lib
pyvenv.cfg
"""
    gitignore_path = os.path.join(tool_folder, ".gitignore")
    try:
        with open(gitignore_path, "w") as f:
            f.write(gitignore_content)
    except Exception as e:
        print(f"Error generating .gitignore: {gitignore_path}: {e}")
        print(f"Debug: .gitignore generation exception: {e}")
        return

    # Generate initial Makefile
    initial_makefile_content = """\
.PHONY: paige
paige:
\t@python .paige/paigefile.py
"""

    makefile_path = "Makefile"
    try:
        with open(makefile_path, "w") as f:
            f.write(initial_makefile_content)
    except Exception as e:
        print(f"Error generating initial Makefile: {makefile_path}: {e}")
        return

def run_makefile_gen():
    ctx = contextvars.Context()
    logger = new_logger("paige")
    ctx = with_logger(ctx, logger)

    logger.info("Running Makefile generation process...")

    paigefile_path = os.path.join(TOOL_DIR_PATH, "paigefile.py")

    if not os.path.exists(paigefile_path):
        logger.error(f"paigefile.py not found at: {paigefile_path}. Run 'paige init' first.")
        sys.exit(1)


    try:
        subprocess_args = [sys.executable, paigefile_path] # Run paigefile.py directly - no --paige-run
        process = subprocess.Popen(subprocess_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            logger.error(f"Makefile generation failed. paigefile.py exited with code: {process.returncode}")
            if stderr:
                logger.error(f"Error output from paigefile.py:\n{stderr.decode()}")
            sys.exit(1)
        else:
            logger.info("Makefile generation triggered (via direct paigefile.py execution).")
            if stdout:
                logger.debug(f"Output from paigefile.py:\n{stdout.decode()}")

    except FileNotFoundError:
        logger.fatal(f"Python executable not found. Ensure Python is in your PATH.")
    except Exception as e:
        logger.error(f"Error running paigefile.py for Makefile generation: {e}")
        sys.exit(1)
