try:
    from ._version import version as __version__
    from ._version import version_tuple
except ImportError:
    __version__ = "unknown"
    version_tuple = (0, 0, "unknown")

from .extension import sort, sort_inplace, argsort  # noqa: F401
