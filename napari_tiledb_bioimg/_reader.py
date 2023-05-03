import os
import warnings
from tiledb.bioimg.openslide import TileDBOpenSlide
import tiledb

def napari_get_reader(path):

    if not isinstance(path, str):
        warnings.warn(f"Not a single path: {path}")
        return None

    config = None
    if path.startswith('tiledb://'):
        # This tiledb paths should be resolved with cloud creds found under $HOME./tiledb/cloud.json
        # the current spec of napari_get_reader does not allow parameter passing
        # Read through tiledb-cloud
        try:
          import tiledb.cloud
          config = tiledb.cloud.Config()
        except ImportError as exc:
            raise ImportError("TileDB URIs require installation of tiledb-cloud") from exc

    # Scope with ctx
    with tiledb.scope_ctx(ctx_or_config=config):
        if tiledb.object_type(path) != "group":
            warnings.warn(f"Not a tiledb group: {path}")
            return None

        try:
            slide = TileDBOpenSlide(path)
        except tiledb.TileDBError as ex:
            warnings.warn(f"napari-tiledb plugin failed to open {path}: {ex}")
            return None

        def reader_function(_):
            level_data = list(map(slide.read_level_dask, range(slide.level_count)))
            name = os.path.basename(os.path.abspath(path))
            return [(level_data, {"name": name})]

        return reader_function
