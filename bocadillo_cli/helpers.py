import pathlib
import pkgutil
import typing
from contextlib import contextmanager

import click
from jinja2 import Template

from . import formatutils as fmt


class Templates:
    def __init__(self, context: dict):
        self.context = context

    @staticmethod
    def _get(name: str) -> Template:
        path = str(pathlib.Path("templates", name))
        content: bytes = pkgutil.get_data("bocadillo_cli", path)
        if content is None:
            raise ValueError(f"Template not found: {name}")
        return Template(content.decode("utf-8"))

    def render(self, name: str) -> str:
        return self._get(f"{name}.jinja").render(self.context)


class Writer:
    CREATE = fmt.success("CREATE")

    def __init__(self, dry: bool, templates: Templates):
        self.dry = dry
        self.templates = templates
        self.root = None

    def mkdir(self, path: pathlib.Path, **kwargs):
        if not self.dry:
            try:
                path.mkdir(**kwargs)
            except FileExistsError as exc:
                if path == pathlib.Path.cwd():
                    return
                raise exc from None
        click.echo(f"{self.CREATE} {path} {fmt.muted('directory')}")

    def writefile(self, path: pathlib.Path, content: str):
        if path.exists():
            return

        if not self.dry:
            with open(str(path), "w", encoding="utf-8") as f:
                f.write(content)
                f.write("\n")

        nbytes = len(content.encode())
        nbytes_formatted = fmt.muted(f"({nbytes} bytes)")
        click.echo(f"{self.CREATE} {path} {nbytes_formatted}")

    def writetemplate(self, *names: str, root: pathlib.Path = None) -> None:
        if root is None:
            assert self.root is not None
            root = self.root

        for name in names:
            content = self.templates.render(name)
            path = pathlib.Path(root, name)
            self.writefile(path, content)

    @contextmanager
    def cd(self, directory: pathlib.Path):
        self.mkdir(directory, exist_ok=True)
        self.root = directory
        try:
            yield self
        finally:
            self.root = None

    def generate(self, config: typing.Dict[str, typing.List[str]]):
        for directory, filenames in config.items():
            with self.cd(directory):
                for filename in filenames:
                    self.writetemplate(filename)
