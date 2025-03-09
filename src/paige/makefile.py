# src/paige/makefile.py
import os
import inspect
import re
from paige.path import from_git_root
from paige.const import PAIGE_FILE_NAME
from paige import discover

class MakefileConfig:
    def __init__(self, path, default_target=None, namespace=None):
        self.path = path
        self.default_target = default_target
        self.namespace = namespace

    def get_namespace_name(self):
        if self.namespace is None:
            return ""
        return str(self.namespace).split('.')[-1]

    def get_default_target_name(self):
        if self.default_target is None:
            return ""
        target_name = self.default_target.__name__
        target_name = re.sub(r'^main\.', '', target_name)
        target_name = re.sub(r'^' + re.escape(self.get_namespace_name()) + r'\.', '', target_name)
        target_name = target_name.split('-')[0]
        if not re.match(r'^[a-zA-Z]+$', target_name):
            raise ValueError(f"Invalid default target name: {target_name}")
        return target_name
