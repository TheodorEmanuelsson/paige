import os
import subprocess

from paige.path import from_git_root, from_bin_dir, from_paige_dir
from paige.logger import get_logger
from paige.generate import create_generating_paigefile


# Context key for storing environment variables
CMD_ENV_KEY = "cmd_env"


def clean_up_paige_executable():
    """Clean up the paige executable."""
    paige_executable = from_paige_dir("generating_paigefile.py")
    if os.path.exists(paige_executable):
        os.remove(paige_executable)


def context_with_env(ctx: dict, *env_vars: str) -> dict:
    """Returns a context with environment variables which are appended to Command."""
    new_ctx = ctx.copy()
    new_ctx[CMD_ENV_KEY] = env_vars
    return new_ctx


def command(ctx: dict, path: str, *args: str) -> subprocess.Popen:
    """Should be used when returning exec.Cmd from tools to set opinionated standard fields."""
    # Create command with context
    cmd_args = [path] + list(args)
    cmd = subprocess.Popen(
        cmd_args,
        cwd=from_git_root("."),
        env=prepare_env(ctx),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return cmd


def prepare_env(ctx: dict) -> dict:
    """Prepare environment variables for command execution."""
    env = os.environ.copy()

    # Add environment variables from context
    if CMD_ENV_KEY in ctx:
        env_vars = ctx[CMD_ENV_KEY]
        for env_var in env_vars:
            if "=" in env_var:
                key, value = env_var.split("=", 1)
                env[key] = value

    # Prepend .paige/.venv/bin directory to PATH for commands like ruff
    paige_venv_bin = from_paige_dir(".venv", "bin")
    if os.path.exists(paige_venv_bin):
        env["PATH"] = f"{paige_venv_bin}:{env.get('PATH', '')}"

    # Prepend bin directory to PATH
    bin_dir = from_bin_dir()
    if os.path.exists(bin_dir):
        env["PATH"] = f"{bin_dir}:{env.get('PATH', '')}"

    return env


def has_file_references(line: str) -> bool:
    """Check if a line contains file references (e.g., lint errors)."""
    line = line.strip()
    if ":" in line:
        # Check if the part before ':' is a valid file path
        file_part = line.split(":", 1)[0]
        if os.path.exists(file_part):
            return True
    return False


class LogWriter:
    """Custom writer that handles logging with file reference detection."""

    def __init__(self, ctx: dict, output_stream):
        self.ctx = ctx
        self.output_stream = output_stream
        self.logger = get_logger(ctx)
        self.has_file_references = False

    def write(self, data: str):
        """Write data with proper logging."""
        lines = data.split("\n")
        for line in lines:
            if not line.strip():
                continue

            if not self.has_file_references:
                self.has_file_references = has_file_references(line)
                if self.has_file_references:
                    # Print empty line with logger prefix to enable GitHub autodetection
                    if self.logger:
                        self.logger.info("")

            if self.has_file_references:
                # Print line without logger prefix for file references
                line = line.strip()
                print(line, file=self.output_stream)
            else:
                # Print with logger prefix
                if self.logger:
                    self.logger.info(line)
                else:
                    print(line, file=self.output_stream)

    def flush(self):
        """Flush the output stream."""
        if hasattr(self.output_stream, "flush"):
            self.output_stream.flush()


def output(cmd: subprocess.Popen) -> str:
    """Run the given command, and return all output from stdout in a neatly, trimmed manner,
    raising an exception if an error occurs."""
    stdout, stderr = cmd.communicate()
    if cmd.returncode != 0:
        raise RuntimeError(f"{cmd.args[0]} failed: {stderr}")
    return stdout.strip()


def run_command(ctx: dict, path: str, *args: str) -> subprocess.Popen:
    """Convenience function to create and return a command."""
    return command(ctx, path, *args)


def run_command_output(ctx: dict, path: str, *args: str) -> str:
    """Convenience function to run a command and return its output."""
    cmd = command(ctx, path, *args)
    return output(cmd)


def run(ctx: dict, path: str, *args: str) -> None:
    """Run a command and log its output, handling empty output gracefully."""
    logger = get_logger(ctx)
    create_generating_paigefile()
    cmd = command(ctx, path, *args)

    stdout, stderr = cmd.communicate()

    # Log stdout if there is any
    if stdout.strip():
        for line in stdout.strip().split("\n"):
            if line.strip():
                logger.info(line.strip())

    # Log stderr if there is any
    if stderr.strip():
        for line in stderr.strip().split("\n"):
            if line.strip():
                logger.warning(line.strip())

    # Check return code
    if cmd.returncode != 0:
        error_msg = (
            stderr.strip()
            if stderr.strip()
            else f"{path} failed with exit code {cmd.returncode}"
        )
        raise RuntimeError(error_msg)

    # If no output but command succeeded, log a success message
    if not stdout.strip() and not stderr.strip():
        logger.info(f"{path} completed successfully")

    # If this was a generated paigefile, clean it up
    if path.endswith("generating_paigefile.py"):
        try:
            os.remove(path)
            logger.info("Cleaned up temporary executable")
        except Exception:
            pass
