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
        if not self.dry:
            try:
                path.mkdir(**kwargs)
            except FileExistsError as exc:
                if path == pathlib.Path.cwd():
                    return
                raise exc from None
        click.echo(f"{self.CREATE} {path}")

    def writefile(self, path: pathlib.Path, content: str):
        if path.exists():
            return

        if not self.dry:
            with open(str(path), "w", encoding="utf-8") as f:
                f.write(content)
                f.write("\n")

        nbytes = len(content.encode())
        click.echo(f"{self.CREATE} {path} ({nbytes} bytes)")


class Project:
    def __init__(
        self, location: pathlib.Path, name: str, package: str, writer: Writer
    ):
        self.location = location.absolute()
        self.name = name
        self.package = package
        self.package_root = (self.location / self.package).absolute()
        self._writer = writer

    def _get_template_context(self) -> dict:
        return {
            "name": self.name,
            "package": self.package,
            "version": __version__,
        }

    def _apply_templates(self, names, root: pathlib.Path):
        context = self._get_template_context()
        for name in names:
            template_name = f"{name}.jinja"
            content = _get_template(template_name).render(context)
            path = pathlib.Path(root, name)
            self._writer.writefile(path, content)

    def _create_dirs(self):
        self._writer.mkdir(self.location)
        self._writer.mkdir(self.package_root)

    def _create_meta(self):
        self._apply_templates(
            [".gitignore", "README.md", "requirements.txt"], root=self.location
        )

    def _create_package(self):
        self._apply_templates(
            [
                "__init__.py",
                "app.py",
                "asgi.py",
                "settings.py",
                "providerconf.py",
            ],
            root=self.package_root,
        )

    def _after_success(self):
        click.echo("\n---\n")
        click.echo(f"Success! ✨🌟✨ Created {self.name} at {self.location}")

        click.echo()
        cd = fmt.code(f"cd {self.location}")
        readme = fmt.code("README.md")
        click.echo(f"Get started: {cd} and refer to instructions in {readme}.")

        click.echo()
        click.echo("To get help about Bocadillo, visit the docs:")
        click.echo(fmt.link(DOCS))

        click.echo()
        click.echo("If you like it, give it a star!")
        click.echo(fmt.link(LIB_REPO))

        click.echo()
        click.echo("Happy coding! 🥪")

    def create(self):
        self._create_dirs()
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


def add_package_param(ctx: click.Context, param: str, value: str) -> str:
    package = value.replace("-", "_")

    if not package.isidentifier():
        raise click.BadParameter(
            f"{package} is not a valid Python identifier. "
            "Please use another project name."
        )

    ctx.params["package"] = package

    return value


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

    project = Project(
        location=pathlib.Path(directory),
        name=name,
        package=package,
        writer=Writer(dry=dry),
    )
    project.create()
