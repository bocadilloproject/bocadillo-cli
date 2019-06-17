import pathlib

import click

from . import formatutils as fmt
from . import constants as cst
from .helpers import Writer
from .version import __version__


def create_project(
    location: pathlib.Path, name: str, package: str, writer: Writer
):
    package_root = location / package
    writer.generate(
        {
            location: [".gitignore", "README.md", "requirements.txt"],
            package_root: [
                "__init__.py",
                "app.py",
                "asgi.py",
                "settings.py",
                "providerconf.py",
            ],
        }
    )

    click.echo()
    click.echo(
        fmt.pre_success(f"Created project {name} at {fmt.code(location)}")
    )

    click.echo()
    readme = fmt.code(location / "README.md")
    click.echo(fmt.pre_hint(f"Read {readme} to get started."))
    click.echo(
        fmt.pre_hint(
            "To learn more about Bocadillo, "
            f"visit the docs: {fmt.link(cst.DOCS)}"
        )
    )

    click.echo()
    click.echo("Happy coding!")
