import threading
import os
import logging
from paige.fn import Fn
from paige.logger import new_logger, with_logger
from paige.internal.runner import run_once
import contextvars

_dependency_chain_context_key = contextvars.ContextVar('dependency_chain')

def deps(ctx, *functions):
    errs = [None] * len(functions)
    checked_functions = _check_functions(functions)
    wg = threading.Barrier(len(functions) + 1)

    for i, f in enumerate(checked_functions):
        i, f = i, f

        dependencies = _get_dependencies(ctx)
        for dependency in dependencies:
            if dependency.ID() == f.ID():
                dep_names = [dep.Name() for dep in dependencies]
                msg = f"Dependency cycle calling {f.Name()}! chain: {','.join(dep_names)}"
                raise Exception(msg)

        ctx = _with_dependency(ctx, f)

        if _is_true(os.environ.get("PAIGE_FORCE_SERIAL_DEPS", "False")):
            logger = new_logger(f.Name())
            child_ctx = with_logger(ctx, logger)
            errs[i] = run_once(f.ID(), lambda: f.Run(child_ctx))
            continue

        def run_in_thread():
            try:
                logger = new_logger(f.Name())
                child_ctx = with_logger(ctx, logger)
                errs[i] = run_once(f.ID(), lambda: f.Run(child_ctx))
            except Exception as e_recover:
                errs[i] = e_recover
            finally:
                wg.wait()


        thread = threading.Thread(target=run_in_thread) # Create thread
        thread.start() # Start thread

    wg.wait() # Wait for all threads to complete

    exit_error = False
    for i, err in enumerate(errs):
        if err:
            logger = new_logger(checked_functions[i].Name())
            logger.error(err)
            exit_error = True

    if exit_error:
        raise Exception("Deps function encountered errors.")


def serial_deps(ctx, *targets):
    for target in targets:
        deps(ctx, target)


def _check_functions(functions):
    result = []
    for f in functions:
        if isinstance(f, Fn):
            result.append(f)
            continue
        if not callable(f):
            raise TypeError(f"non-function used as a target dependency: {type(f)}")
        result.append(Fn(f))
    return result

def _is_true(s):
    s = s.lower()
    return s in ('true', '1', 'yes', 'on')

def _get_dependencies(ctx):
    dependencies = _dependency_chain_context_key.get(None)
    return dependencies if dependencies else []

def _with_dependency(ctx, target):
    dependencies = _get_dependencies(ctx)
    dependencies = list(dependencies)
    dependencies.append(target)
    new_ctx = contextvars.copy_context()
    _dependency_chain_context_key.set(dependencies)
    return ctx
