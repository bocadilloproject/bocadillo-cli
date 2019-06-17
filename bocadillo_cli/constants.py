from . import formatutils as fmt
from .version import __bocadillo_version__, __version__

DOCS = "https://bocadilloproject.github.io"
VERSION = __version__
BOCADILLO_VERSION = (
    fmt.muted("[not installed]")
    if __bocadillo_version__ is None
    else fmt.version(__bocadillo_version__)
)
