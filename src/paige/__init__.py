from paige.makefile import MakefileConfig, generate_makefile
from paige.path import (
    from_git_root,
    from_work_dir,
    from_tools_dir,
    from_bin_dir,
    from_build_dir,
)
from paige.exec import command, output, prepend_path
