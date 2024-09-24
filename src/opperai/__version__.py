from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("opperai")
except PackageNotFoundError:
    __version__ = "unknown"
