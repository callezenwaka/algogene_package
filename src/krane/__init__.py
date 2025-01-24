# src/krane/__init__.py
from .core.sequence import Sequence  # Not .Sequence

try:
    from .version import version as __version__ # type: ignore
except ImportError:
    # If the version file doesn't exist (like during development)
    __version__ = "0.0.0.dev0"