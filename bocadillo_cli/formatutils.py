import typing

import click


def _make_formatter(
    color: str, mode: str = "full", name: str = None
) -> typing.Callable[[typing.Any], str]:
    assert mode in ("full", "prefix")

    def _format_full(obj: typing.Any):
        return click.style(str(obj), fg=color)

    if mode == "prefix":
        assert name is not None

        def _format_prefix(obj: typing.Any):
            return f"{click.style(name.upper(), fg=color)} {obj}"

        return _format_full, _format_prefix

    return _format_full


success, pre_success = _make_formatter("green", mode="prefix", name="success")
warn, pre_warn = _make_formatter("yellow", mode="prefix", name="warn")
hint, pre_hint = _make_formatter("blue", mode="prefix", name="hint")
code = _make_formatter("magenta")
link = _make_formatter("blue")
muted = _make_formatter("black")
version = code
