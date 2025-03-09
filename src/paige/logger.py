import logging
import sys
import contextvars
import re

_logger_context_key = contextvars.ContextVar('logger')

def to_kebab_case(name:str) -> str:
    """Converts a string to kebab-case."""
    name = re.sub(r"main\.", "", name)
    parts = name.split(".")
    if len(parts) > 1:
        name = ":".join(parts)
    name = name.replace("_", "-")
    return name

def new_logger(name):
    """Returns a standard logger."""
    prefix = name
    prefix = to_kebab_case(prefix)
    prefix = f"[{prefix}] "
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter(prefix + '%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def with_logger(ctx, logger):
    """Attaches a logging.Logger to the provided context."""
    token = _logger_context_key.set(logger)
    return contextvars.copy_context()

def AppendLoggerPrefix(ctx, prefix):
    """Appends a prefix to the current logger in the context."""
    logger = logger(ctx)
    new_prefix = logger.handlers[0].formatter._fmt[:logger.handlers[0].formatter._fmt.find('%(message)s')] + prefix
    new_logger = new_logger(logger.name)
    new_logger.handlers[0].setFormatter(logging.Formatter(new_prefix + '%(message)s'))
    return with_logger(ctx, new_logger)

def logger(ctx):
    """Returns the logging.Logger attached to ctx, or a default logger."""
    logger = _logger_context_key.get(None)
    if logger:
        return logger
    return new_logger("paige")
