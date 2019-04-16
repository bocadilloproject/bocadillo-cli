import pathlib
import pkgutil
import typing

import click
from jinja2 import Template

from .version import __version__


def _get_template(name: str) -> Template:
    path = str(pathlib.Path("templates", name))
    content: bytes = pkgutil.get_data("bocadillo_cli", path)
    if content is None:
        raise ValueError(f"Template not found: {name}")
    return Template(content.decode("utf-8"))


BOCADILLO = "https://github.com/bocadilloproject/bocadillo"
DOCS = "https://bocadilloproject.github.io"
CREATE = click.style("CREATE", fg="green")
DRY = False


class Writer:
    def __init__(self, dry: bool = False):
        self.dry = dry

    def mkdir(self, path: pathlib.Path, **kwargs):
        click.echo(f"{CREATE} {path}")
        if self.dry:
            return
        path.mkdir(**kwargs)

    def writefile(self, path: str, content: str):
        nbytes = len(content.encode())
        click.echo(f"{CREATE} {path} ({nbytes} bytes)")
        if self.dry:
            return
        with open(str(path), "w") as f:
            f.write(content)


def _code(text: str) -> str:
    return click.style(text, fg="magenta")


def _link(text: str) -> str:
    return click.style(text, fg="blue")


class Project:
    def __init__(self, location: pathlib.Path, name: str):
        self.location = location
        self.name = name
        self._writer = None

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
        cd = _code(f"cd {self.location}")
        click.echo(f"You can now {cd} and read the README to get started.")

        click.echo()
        click.echo(
            f"To get help about Bocadillo, visit the docs: {_link(DOCS)}"
        )

        click.echo()
        click.echo(f"If you like it, give it a star! {_link(BOCADILLO)}")

        click.echo()
        click.echo("Happy coding! 🥪")

    def create(self, writer: Writer):
        self._writer = writer
        self._create_meta()
        self._create_package()
        self._after_success()


@click.group()
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

    project = Project(location=pathlib.Path(directory), name=name)
    writer = Writer(dry=dry)

    if dry:
        click.secho(
            "Warning: running in dry mode. No files will be written.",
            fg="yellow",
        )

    project.create(writer)
