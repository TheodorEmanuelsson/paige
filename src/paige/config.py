class Makefile:
    """
    Represents the configuration for generating a Makefile.
    """
    def __init__(self, path, default_target, namespace="_global_namespace"):
        """
        Initializes a Makefile configuration.

        Args:
            path (str): The path where the Makefile should be created (e.g., "Makefile", "terraform/Makefile").
            default_target (str): The default target to be executed when 'make' is run (e.g., "all").
            namespace (str, optional): The namespace for tasks in this Makefile.
                                         Defaults to "_global_namespace".
        """
        self.path = path
        self.default_target = default_target
        self.namespace = namespace
