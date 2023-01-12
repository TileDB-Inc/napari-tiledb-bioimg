import os
import warnings

import tiledb
from tiledb.bioimg.openslide import TileDBOpenSlide


def napari_get_reader(path):
    if not isinstance(path, str):
        warnings.warn(f"Not a single path: {path}")
        return None

    if not os.path.isdir(path):
        warnings.warn(f"Not a directory: {path}")
        return None

    try:
        slide = TileDBOpenSlide.from_group_uri(path)
    except tiledb.TileDBError as ex:
        warnings.warn(f"Failed to open {path}: {ex}")
        return None

    def reader_function(_):
        with slide:
            level_data = list(map(slide.read_level, range(slide.level_count)))
        name = os.path.basename(os.path.abspath(path))
        return [(level_data, {"name": name})]

    return reader_function
