import pathlib
import typing

import click

from . import constants as cst
from . import formatutils as fmt
from .helpers import Templates, Writer
from .project import create_project


def add_package_param(ctx: click.Context, param: str, value: str) -> str:
    package = value.replace("-", "_")

    if not package.isidentifier():
        raise click.BadParameter(
            f"{package} is not a valid Python identifier. "
            "Please use another project name."
        )

    ctx.params["package"] = package

    return value


@click.group()
@click.version_option(
    fmt.version(cst.VERSION),
    "-V",
    "--version",
    prog_name="Bocadillo CLI",
    message=f"%(prog)s: %(version)s\nBocadillo: {cst.BOCADILLO_VERSION}",
)
def cli():
    pass


@cli.command()
@click.argument("name", callback=add_package_param)
@click.option(
    "-d",
    "--directory",
    type=click.Path(file_okay=False),
    help=(
        "Directory where the project should be created. "
        "Created if does not exist. "
        "Defaults to `NAME`."
    ),
)
@click.option(
    "--dry",
    is_flag=True,
    default=False,
    help="Dry mode: does not write anything.",
)
def create(name: str, package: str, directory: typing.Optional[str], dry: bool):
    """Initialize a Bocadillo project."""
    if directory is None:
        directory = name

    if dry:
        click.secho(
            "Warning: running in dry mode. No files will be written.",
            fg="yellow",
        )

    create_project(
        location=pathlib.Path(directory),
        name=name,
        package=package,
        writer=Writer(
            dry=dry,
            templates=Templates(
                context={
                    "name": name,
                    "package": package,
                    "version": cst.VERSION,
                }
            ),
        ),
    )
