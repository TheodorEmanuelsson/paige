class Makefile:
    def __init__(self, path:str, default_target:str=None, namespace:str=None):
        self.path = path
        self.default_target = default_target
        self.namespace = namespace

    def get_namespace_name(self):
        if self.namespace is None:
            return ""
        return str(self.namespace)

    def get_default_target_name(self):
        if self.default_target is None:
            return ""
        return str(self.default_target)

def generate_makefile():
    pass
