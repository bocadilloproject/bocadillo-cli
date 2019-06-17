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
    SKIP = fmt.muted("SKIP")

    def __init__(self, dry: bool, no_input: bool, templates: Templates):
        self.dry = dry
        self.no_input = no_input
        self.templates = templates
        self.root = None

    def mkdir(self, path: pathlib.Path, **kwargs):
        if path.exists():
            action = self.SKIP
        else:
            action = self.CREATE
            if not self.dry:
                path.mkdir(**kwargs)
        click.echo(f"{action} {path} {fmt.muted('directory')}")

    def writefile(self, path: pathlib.Path, content: str):
        if path.exists() and (
            self.no_input
            or not click.confirm(
                fmt.pre_warn(
                    f"File {fmt.code(path)} already exists. Overwrite?"
                )
            )
        ):
            nbytes = None
            action = self.SKIP
        else:
            if not self.dry:
                with open(str(path), "w", encoding="utf-8") as f:
                    f.write(content)
                    f.write("\n")
            nbytes = len(content.encode())
            action = self.CREATE

        nbytes_formatted = fmt.muted(f" ({nbytes} bytes)") if nbytes else ""
        click.echo(f"{action} {path}{nbytes_formatted}")

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
