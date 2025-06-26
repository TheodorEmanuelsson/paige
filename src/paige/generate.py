import os
import subprocess
import importlib.util
import sys
from typing import List

from paige.path import from_paige_dir
from paige.makefile import Makefile, generate_makefile_content
from paige.logger import new_logger, with_logger, get_logger
from paige.parser import parse_python_files, generate_init_file


def generate_makefiles(makefiles: List[Makefile]):
    ctx = with_logger({}, new_logger("paige"))
    logger = get_logger(ctx)
    logger.info("building binary and generating Makefiles...")

    if len(makefiles) == 0:
        raise ValueError(
            "no makefiles to generate, see https://github.com/TheodorEmanuelsson/paige for more info"
        )

    # Parse Python files to find target functions
    functions = parse_python_files()
    if not functions:
        raise ValueError("no target functions found in .paige directory")

    # Generate the init file
    init_filename = from_paige_dir("generating_paigefile.py")
    init_content = generate_init_file(functions, makefiles)

    with open(init_filename, "w") as f:
        f.write(init_content)

    # Make the file executable
    os.chmod(init_filename, 0o755)

    try:
        # Test that the generated file works
        result = subprocess.run([init_filename], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("Generated executable file works correctly")
        else:
            logger.warning(f"Generated file had issues: {result.stderr}")
    except Exception as e:
        logger.error(f"Error testing generated file: {e}")

    # Generate the makefiles
    for makefile in makefiles:
        if not makefile.path:
            raise ValueError("Path needs to be defined for Makefile")

        # Ensure directory exists
        os.makedirs(os.path.dirname(makefile.path), exist_ok=True)

        # Generate Makefile content
        content = generate_makefile_content(
            makefile, functions, init_filename, makefiles
        )

        # Write Makefile
        with open(makefile.path, "w") as f:
            f.write(content)

        logger.info(f"Generated Makefile: {makefile.path}")

    # Don't clean up the temporary file - it's needed by the Makefile
    # os.remove(init_filename)

    logger.info("Makefile generation complete!")


def execute_paigefile():
    """Execute the main() function from the paigefile."""
    paige_dir = from_paige_dir()
    paigefile_path = os.path.join(paige_dir, "paigefile.py")

    if not os.path.exists(paigefile_path):
        raise ValueError("paigefile.py not found in .paige directory")

    # Add .paige directory to Python path
    sys.path.insert(0, paige_dir)

    # Import and execute the paigefile
    spec = importlib.util.spec_from_file_location("paigefile", paigefile_path)
    paigefile = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(paigefile)

    # Call the main function
    if hasattr(paigefile, "main"):
        paigefile.main()
    else:
        raise ValueError("main() function not found in paigefile.py")


if __name__ == "__main__":
    execute_paigefile()
