import os
import warnings
import json

from typing import Sequence, Mapping, Any


def _get_meta(name: str, level_metadata: Sequence[Any]) -> Mapping[str, Any]:
    try:
        # TODO: clean this up
        meta: Mapping[str, Any] = {"name": name, "metadata": dict(json.loads(level_metadata[0]['json_write_kwargs']))}
    except KeyError as exc:
        warnings.warn(f"[TileDB:Napari:BioImg] - Error: napari-tiledb plugin did not find expected metadata: {exc}")
        return dict()
    return meta


def napari_get_reader(path):
    import tiledb
    from tiledb.bioimg.openslide import TileDBOpenSlide

    if not isinstance(path, str):
        warnings.warn(f"Not a single path: {path}")
        raise ValueError('[TileDB::Napari] - Error: The single path given should be of string type')

    config = None
    if path.startswith('tiledb://'):
        # This tiledb paths should be resolved with cloud creds found under $HOME./tiledb/cloud.json
        # the current spec of napari_get_reader does not allow parameter passing
        # Read through tiledb-cloud
        try:
          import tiledb.cloud
          config = tiledb.cloud.Config()
        except ImportError as exc:
            raise ImportError("[TileDB:Napari:BioImg] - Error: TileDB URIs require installation of tiledb-cloud") from exc

    # Scope with ctx
    with tiledb.scope_ctx(ctx_or_config=config):
        if tiledb.object_type(path) != "group":
            raise ValueError('[TileDB::Napari] - Error: The path given should correspond to a tiledb group')
        try:
            slide = TileDBOpenSlide(path)
        except tiledb.TileDBError as ex:
            warnings.warn(f"[TileDB::Napari] - Error: TileDBOpenSlide failed to open {path}: {ex}")
            return None

        def reader_function(_):
            level_data = list(map(slide.read_level_dask, range(slide.level_count)))
            level_metadata = list(map(slide.level_properties, range(slide.level_count)))
            name = os.path.basename(os.path.abspath(path))
            meta = _get_meta(name, level_metadata)
            return [(level_data, meta, "image")]

        return reader_function
