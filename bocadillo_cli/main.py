import pathlib
import pkgutil
import typing

import click
from jinja2 import Template

from . import formatutils as fmt
from .version import __version__

try:
    import bocadillo
except ImportError:
    BOCADILLO_VERSION = fmt.muted("[not installed]")
else:
    BOCADILLO_VERSION = fmt.version(bocadillo.__version__)

LIB_REPO = "https://github.com/bocadilloproject/bocadillo"
DOCS = "https://bocadilloproject.github.io/"


def _get_template(name: str) -> Template:
    path = str(pathlib.Path("templates", name))
    content: bytes = pkgutil.get_data("bocadillo_cli", path)
    if content is None:
        raise ValueError(f"Template not found: {name}")
    return Template(content.decode("utf-8"))


class Writer:
    CREATE = click.style("CREATE", fg="green")

    def __init__(self, dry: bool):
        self.dry = dry

    def mkdir(self, path: pathlib.Path, **kwargs):
        click.echo(f"{self.CREATE} {path}")
        if self.dry:
            return
        path.mkdir(**kwargs)

    def writefile(self, path: str, content: str):
        nbytes = len(content.encode())
        click.echo(f"{self.CREATE} {path} ({nbytes} bytes)")
        if self.dry:
            return
        with open(str(path), "w") as f:
            f.write(content)


class Project:
    def __init__(self, location: pathlib.Path, name: str, writer: Writer):
        self.location = location
        self.name = name
        self._writer = writer

    def _get_template_context(self) -> dict:
        return {"name": self.name, "version": __version__}

    def _apply_templates(self, names, root: pathlib.Path):
        context = self._get_template_context()
        for name in names:
            content = _get_template(name).render(context)
            path = pathlib.Path(root, name)
            self._writer.writefile(path, content)

    def _create_meta(self):
        self._writer.mkdir(self.location)
        self._apply_templates(
            [".gitignore", "README.md", "requirements.txt"], root=self.location
        )

    def _create_package(self):
        root = self.location / self.name
        self._writer.mkdir(root)
        self._apply_templates(
            [
                "__init__.py",
                "app.py",
                "asgi.py",
                "settings.py",
                "providerconf.py",
            ],
            root=root,
        )

    def _after_success(self):
        click.echo()
        click.echo(f"Success! Created project at {self.location.absolute()}")

        click.echo()
        cd = fmt.code(f"cd {self.location}")
        readme = fmt.code("README.md")
        click.echo(f"You can now run {cd} and read {readme} to get started.")

        click.echo()
        click.echo("To get help about Bocadillo, visit the docs:")
        click.echo(fmt.link(DOCS))

        click.echo()
        click.echo("If you like it, give it a star!")
        click.echo(fmt.link(LIB_REPO))

        click.echo()
        click.echo("Happy coding! 🥪")

    def create(self):
        self._create_meta()
        self._create_package()
        self._after_success()


@click.group()
@click.version_option(
    fmt.version(__version__),
    "-V",
    "--version",
    prog_name="Bocadillo CLI",
    message=f"%(prog)s: %(version)s\nBocadillo: {BOCADILLO_VERSION}",
)
def cli():
    pass


@cli.command()
@click.argument("name")
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
def create(name: str, directory: typing.Optional[str], dry: bool):
    """Initialize a Bocadillo project."""
    if directory is None:
        directory = name

    if dry:
        click.secho(
            "Warning: running in dry mode. No files will be written.",
            fg="yellow",
        )

    project = Project(
        location=pathlib.Path(directory), name=name, writer=Writer(dry=dry)
    )
    project.create()
