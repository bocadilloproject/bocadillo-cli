__version__ = "0.2.2"

try:
    import bocadillo
except ImportError:
    __bocadillo_version__ = None
else:
    __bocadillo_version__ = bocadillo.__version__
