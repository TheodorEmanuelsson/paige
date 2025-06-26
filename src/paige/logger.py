import logging
import re

LOGGER_CONTEXT_KEY = "paige_logger"


def new_logger(name: str) -> logging.Logger:
    """Returns a standard logger with formatted prefix."""
    # Clean up the name
    prefix = name
    prefix = prefix.replace("main.", "")
    prefix = prefix.replace("paige.tools.", "")

    prefix = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", prefix)
    prefix = prefix.lower().replace("_", "-")

    prefix = f"[{prefix}] "

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Create handler if it doesn't exist
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(message)s"
        )  # Just the message, prefix is in logger name
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # Store prefix in logger for later use
    logger.prefix = prefix
    return logger


def with_logger(ctx: dict, logger: logging.Logger) -> dict:
    """Attaches a logger to the provided context."""
    new_ctx = ctx.copy()
    new_ctx[LOGGER_CONTEXT_KEY] = logger
    return new_ctx


def append_logger_prefix(ctx: dict, prefix: str) -> dict:
    """Appends a prefix to the current logger."""
    logger = get_logger(ctx)
    new_logger = logging.getLogger(logger.name + prefix)
    new_logger.setLevel(logging.INFO)

    # Copy handlers
    for handler in logger.handlers:
        new_logger.addHandler(handler)

    # Update prefix
    new_logger.prefix = logger.prefix + prefix
    return with_logger(ctx, new_logger)


def get_logger(ctx: dict) -> logging.Logger:
    """Returns the logger attached to ctx, or a default logger."""
    if LOGGER_CONTEXT_KEY in ctx:
        return ctx[LOGGER_CONTEXT_KEY]
    return new_logger("paige")
