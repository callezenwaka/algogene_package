# src/krane/__init__.py
"""
Krane - A light-weight bioinformatics package
"""

try:
    from importlib.metadata import version
    __version__ = version("krane")
except ImportError:
    # For Python < 3.8
    # from importlib_metadata import version
    # __version__ = version("krane")
    __version__ = "0.0.0.dev0" # If the version file doesn't exist (like during development)


from .core.sequence import Sequence

# Define public API
__all__ = [
    'Sequence',
    # Add other public classes/functions
]

# Package metadata
__author__ = "Callis Ezenwaka"
__email__ = "callisezenwaka@outlook.com"
