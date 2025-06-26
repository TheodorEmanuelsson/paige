from typing import Dict, Any, Optional


class Namespace:
    """Namespace allows for the grouping of similar commands."""

    pass


class NamespaceMetadata:
    """Base class for namespace metadata."""

    pass


def is_namespace_class(cls) -> bool:
    """Check if a class is a namespace (inherits from Namespace)."""
    try:
        return issubclass(cls, Namespace)
    except TypeError:
        return False


def get_namespace_name(namespace_instance) -> str:
    """Get the name of a namespace instance."""
    if namespace_instance is None:
        return ""

    # If it's a class, get the class name
    if isinstance(namespace_instance, type):
        return namespace_instance.__name__

    # If it's an instance, get the class name
    return type(namespace_instance).__name__


def get_namespace_metadata(namespace_instance) -> Dict[str, Any]:
    """Get metadata from a namespace instance."""
    if namespace_instance is None:
        return {}

    metadata = {}

    # Get instance attributes (for instances)
    if not isinstance(namespace_instance, type):
        for attr_name in dir(namespace_instance):
            if not attr_name.startswith("_"):
                attr_value = getattr(namespace_instance, attr_name)
                if not callable(attr_value):
                    metadata[attr_name] = attr_value

    # Get class attributes (for classes)
    else:
        for attr_name in dir(namespace_instance):
            if not attr_name.startswith("_"):
                attr_value = getattr(namespace_instance, attr_name)
                if not callable(attr_value):
                    metadata[attr_name] = attr_value

    return metadata
