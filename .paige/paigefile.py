
import paige as pg

def main():
    pg.generate_makefiles(
        pg.Makefile(
            path = pg.from_git_root(),
            default_target = all()
    ),
)

pg.task()
def all():
    pass
