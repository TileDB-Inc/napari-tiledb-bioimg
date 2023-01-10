try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

from ._reader import napari_get_reader

# from ._writer import write_multiple, write_single_image

__all__ = (
    "napari_get_reader",
    # "write_single_image",
    # "write_multiple",
)
