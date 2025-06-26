import paige as pg


def main():
    """Generate Makefile for ruff formatting and fixing."""
    pg.generate_makefiles(
        [
            pg.Makefile(
                path=pg.from_git_root("Makefile"), default_target="ruff_format"
            ),
        ]
    )


def ruff_format(ctx):
    """Format code using ruff."""
    cmd = pg.command(ctx, "ruff", "format", ".")
    pg.output(cmd)


def ruff_fix(ctx):
    """Autofix code using ruff."""
    cmd = pg.command(ctx, "ruff", "check", ".", "--fix")
    pg.output(cmd)


if __name__ == "__main__":
    main()
