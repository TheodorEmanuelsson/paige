import paige as pg


def main():
    """Generate Makefile for this project."""
    pg.generate_makefiles(
        [
            pg.Makefile(path=pg.from_git_root("Makefile"), default_target="default"),
        ]
    )


def default(ctx):
    """Default target - add your main tasks here."""
    print("Add your default tasks here")
    # Example: pg.Deps(ctx, format, lint, test)


def ruff_format(ctx):
    """Format code using ruff."""
    pg.run(ctx, "ruff", "format", ".")


def ruff_fix(ctx):
    """Autofix code using ruff."""
    pg.run(ctx, "ruff", "check", ".", "--fix")


if __name__ == "__main__":
    main()
