try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

from ._reader import napari_get_reader
from ._writer import napari_write_image_lossless, napari_write_image_lossy

__all__ = (
    "napari_get_reader",
    "napari_write_image_lossy",
    "napari_write_image_lossless",
)
