# src/paige/deps.py
import threading
import os
import logging
from paige.fn import Fn
from paige.logger import new_logger, with_logger
from paige.internal.runner import run_once
import contextvars

_dependency_chain_context_key = contextvars.ContextVar('dependency_chain')

def deps(ctx, *functions):
    errs = [None] * len(functions) # Initialize error list
    checked_functions = _check_functions(functions) # Check and convert functions to Fn objects
    wg = threading.Barrier(len(functions) + 1) # Barrier for wait group

    for i, f in enumerate(checked_functions):
        i, f = i, f # Capture loop variables for closure

        dependencies = _get_dependencies(ctx)
        for dependency in dependencies:
            if dependency.ID() == f.ID():
                dep_names = [dep.Name() for dep in dependencies]
                msg = f"Dependency cycle calling {f.Name()}! chain: {','.join(dep_names)}"
                raise Exception(msg) # Panic in Go, Exception in Python

        ctx = _with_dependency(ctx, f) # Update context with dependency

        if _is_true(os.environ.get("SAGE_FORCE_SERIAL_DEPS", "False")): # Check for serial deps env var
            logger = new_logger(f.Name()) # Create logger for the function
            child_ctx = with_logger(ctx, logger) # Add logger to context
            errs[i] = run_once(f.ID(), lambda: f.Run(child_ctx)) # Serial run with run_once
            continue

        def run_in_thread():
            try:
                logger = new_logger(f.Name()) # Create logger for the function
                child_ctx = with_logger(ctx, logger) # Add logger to context
                errs[i] = run_once(f.ID(), lambda: f.Run(child_ctx)) # Parallel run with run_once
            except Exception as e_recover: # Catch exceptions in thread
                errs[i] = e_recover # Store exception
            finally:
                wg.wait() # Signal completion to wait group


        thread = threading.Thread(target=run_in_thread) # Create thread
        thread.start() # Start thread

    wg.wait() # Wait for all threads to complete

    exit_error = False
    for i, err in enumerate(errs):
        if err:
            logger = new_logger(checked_functions[i].Name()) # Create logger for error output
            logger.error(err) # Log the error
            exit_error = True

    if exit_error:
        raise Exception("Deps function encountered errors.") # Or decide to sys.exit, but exceptions are more pythonic


def serial_deps(ctx, *targets):
    for target in targets:
        deps(ctx, target) # Just call Deps serially


def _check_functions(functions):
    result = []
    for f in functions:
        if isinstance(f, Fn): # Check if already a Fn instance
            result.append(f)
            continue
        if not callable(f): # Check if callable (function)
            raise TypeError(f"non-function used as a target dependency: {type(f)}")
        result.append(Fn(f)) # Convert function to Fn instance
    return result

def _is_true(s):
    s = s.lower()
    return s in ('true', '1', 'yes', 'on')

def _get_dependencies(ctx):
    dependencies = _dependency_chain_context_key.get(None) # Get dependencies from context
    return dependencies if dependencies else [] # Return list or empty list if None

def _with_dependency(ctx, target):
    dependencies = _get_dependencies(ctx)
    dependencies = list(dependencies) # Create a copy to avoid modifying original
    dependencies.append(target) # Append new dependency
    new_ctx = contextvars.copy_context()
    _dependency_chain_context_key.set(dependencies) # Set updated dependencies in new context. How to properly return new context?
    return ctx # In Python contextvars are set globally within a context, so returning ctx is sufficient, as contextvars.copy_context was used before setting.
