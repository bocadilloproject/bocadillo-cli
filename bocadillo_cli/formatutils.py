import typing

import click


def _make_formatter(color: str) -> typing.Callable[[typing.Any], str]:
    def _format(obj: typing.Any):
        return click.style(str(obj), fg=color)

    return _format


success = _make_formatter("green")
code = _make_formatter("magenta")
link = _make_formatter("blue")
muted = _make_formatter("black")
version = code
