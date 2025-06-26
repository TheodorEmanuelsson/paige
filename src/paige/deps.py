import os
import threading
import inspect
from typing import List, Dict, Any, Callable, Union
from functools import wraps

from paige.logger import new_logger, with_logger, get_logger


class Target:
    """Represents a target function that can be run with Deps."""

    def name(self) -> str:
        """Non-unique display name for the Target."""
        raise NotImplementedError

    def id(self) -> str:
        """Unique identifier for the Target."""
        raise NotImplementedError

    def run(self, ctx: dict) -> None:
        """Run the Target."""
        raise NotImplementedError


class FnTarget(Target):
    """Creates a Target from a compatible function and args."""

    def __init__(self, target: Callable, *args):
        self.target = target
        self.args = args
        self._name = self._get_function_name()
        self._id = self._generate_id()

    def _get_function_name(self) -> str:
        """Get the function name."""
        return self.target.__name__

    def _generate_id(self) -> str:
        """Generate unique ID for this function call."""
        import json

        args_json = json.dumps(self.args)
        return f"{self.target.__name__}({args_json})"

    def name(self) -> str:
        return self._name

    def id(self) -> str:
        return self._id

    def run(self, ctx: dict) -> None:
        """Run the target function."""
        try:
            self.target(ctx, *self.args)
        except Exception as e:
            if get_logger(ctx):
                get_logger(ctx).error(f"Error in {self.name()}: {e}")
            raise


def Fn(target: Callable, *args) -> Target:
    """Create a Target from a compatible function and args."""
    return FnTarget(target, *args)


class Runner:
    """Global runner for ensuring functions run exactly once."""

    def __init__(self):
        self._lock = threading.Lock()
        self._once_fns = {}

    def run_once(self, ctx: dict, key: str, fn: Callable[[dict], None]) -> None:
        """Run function exactly once and always return the result from the initial run."""
        with self._lock:
            if key not in self._once_fns:
                self._once_fns[key] = self._make_once_fn(fn)

        self._once_fns[key](ctx)

    def _make_once_fn(self, fn: Callable[[dict], None]) -> Callable[[dict], None]:
        """Create a function that runs exactly once."""
        result = {"error": None, "run": False}

        def once_fn(ctx: dict) -> None:
            if not result["run"]:
                try:
                    fn(ctx)
                except Exception as e:
                    result["error"] = e
                finally:
                    result["run"] = True

            if result["error"]:
                raise result["error"]

        return once_fn


# Global runner instance
_runner = Runner()


def check_functions(*functions: Union[Target, Callable]) -> List[Target]:
    """Convert functions to targets."""
    result = []
    for f in functions:
        if isinstance(f, Target):
            result.append(f)
        elif callable(f):
            result.append(Fn(f))
        else:
            raise ValueError(f"non-function used as a target dependency: {type(f)}")
    return result


def is_true(s: str) -> bool:
    """Check if a string represents a true boolean value."""
    return s.lower() in ("true", "1", "yes", "on")


# Context key for dependency chain
DEPENDENCY_CHAIN_KEY = "dependency_chain"


def get_dependencies(ctx: dict) -> List[Target]:
    """Get the current dependency chain from context."""
    return ctx.get(DEPENDENCY_CHAIN_KEY, [])


def with_dependency(ctx: dict, target: Target) -> dict:
    """Create a new context with an additional dependency."""
    new_ctx = ctx.copy()
    dependencies = get_dependencies(ctx)
    dependencies = dependencies + [target]
    new_ctx[DEPENDENCY_CHAIN_KEY] = dependencies
    return new_ctx


def Deps(ctx: dict, *functions: Union[Target, Callable]) -> None:
    """Run each of the provided functions in parallel.

    Dependencies must be of type function or Target.
    Each function will be run exactly once, even across multiple calls to Deps.
    """
    if not functions:
        return

    # Convert functions to targets
    targets = check_functions(*functions)

    # Check for dependency cycles
    for target in targets:
        dependencies = get_dependencies(ctx)
        for dep in dependencies:
            if dep.id() == target.id():
                dep_names = [d.name() for d in dependencies]
                msg = f"dependency cycle calling {target.name()}! chain: {','.join(dep_names)}"
                raise RuntimeError(msg)

    # Run targets in parallel
    errors = []
    threads = []

    for target in targets:
        target_ctx = with_dependency(ctx, target)

        def run_target(t=target, tc=target_ctx):
            try:
                _runner.run_once(tc, t.id(), t.run)
            except Exception as e:
                errors.append((t.name(), e))

        thread = threading.Thread(target=run_target)
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Report errors
    if errors:
        for name, error in errors:
            logger = get_logger(ctx)
            if logger:
                logger.error(f"Error in {name}: {error}")
            else:
                print(f"Error in {name}: {error}")
        raise RuntimeError(f"Errors occurred in {len(errors)} targets")


def SerialDeps(ctx: dict, *targets: Union[Target, Callable]) -> None:
    """Run all dependencies serially instead of in parallel."""
    for target in targets:
        Deps(ctx, target)
