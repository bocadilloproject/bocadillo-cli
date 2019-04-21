import click


def code(text: str) -> str:
    return click.style(text, fg="magenta")


def link(text: str) -> str:
    return click.style(text, fg="blue")


def muted(text: str) -> str:
    return click.style(text, fg="black")


def version(text: str) -> str:
    return click.style(text, fg="magenta")
