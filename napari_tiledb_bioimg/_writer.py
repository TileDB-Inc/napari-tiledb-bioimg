from __future__ import annotations

import os
from typing import Any, Dict, Optional, Sequence, Tuple, Iterator
import logging
import numpy as np
import tiledb
from napari.layers.image.image import MultiScaleData
from tiledb.bioimg.converters.base import Axes, ImageConverterMixin, ImageReader, ImageWriter
from tiledb.bioimg.helpers import iter_color
from tiledb.filter import WebpFilter 


class NapariDataReader:

    def __init__(self, 
                 data,
                 logger:  Optional[logging.Logger] = None):
        self._data = data

    # adapted from https://github.com/napari/napari/blob/ee94c35c04674ddc8e89ed63ac7674c27fa8fc6c/napari/layers/image/_image_utils.py#L27-L30
    @property
    def _rgb(self) -> bool:
        return len(self._data.shape) > 2 and self._data.shape[-1] == 3

    @property
    def _rgba(self) -> bool:
        return len(self._data.shape) > 2 and self._data.shape[-1] == 4

    @property
    def axes(self) -> Axes:
        # adapted from https://github.com/stardist/stardist-napari/blob/cb3436bde2d7c0d72cf6d2768ea4311be1c11957/stardist_napari/_dock_widget.py#L1573-L1582
        ndim = len(self._data.shape)
        if ndim == 2:
            axes = "YX"
        elif ndim == 3:
            axes = "YXC" if (self._rgb or self._rgba) else None
        elif ndim == 4:
            axes = None if (self._rgb or self._rgba) else "TZYX"
        else:
            axes = None

        if axes is None:
            raise NotImplementedError("Cannot determine the image axes")
        return Axes(axes)

    @property
    def channels(self) -> Sequence[str]:
        if self._rgb:
            return "RED", "GREEN", "BLUE"
        if self._rgba:
            return "RED", "GREEN", "BLUE", "ALPHA"
        return ()

    @property
    def webp_format(self) -> WebpFilter.WebpInputFormat:
        if self._rgb:
            return WebpFilter.WebpInputFormat.WEBP_RGB
        if self._rgba:
            return WebpFilter.WebpInputFormat.WEBP_RGBA
        return WebpFilter.WebpInputFormat.WEBP_NONE

    @property
    def group_metadata(self) -> Dict[str, Any]:
        return {}

    @property
    def image_metadata(self) -> Dict[str, Any]:
        metadata: Dict[str, Any] = {}
        color_generator = iter_color(np.dtype(np.uint8), 3)
        metadata["channels"] = [
            {"id": f"{idx}", "name": f"{name}", "color": next(color_generator)}
            for idx, name in enumerate(["red", "green", "blue"])
        ]
        return metadata
    
    @property
    def original_metadata(self) -> Dict[str, Any]:
        return {}
    
    def optimal_reader(
        self, level: int, max_workers: int = 0
    ) -> Optional[Iterator[Tuple[Tuple[slice, ...], NDArray[Any]]]]:
        return None


class NapariSingleScaleDataReader(NapariDataReader):
    def __init__(self, data: np.ndarray, logger:  Optional[logging.Logger] = None):
        super().__init__(data)
    
    def __enter__(self) -> NapariSingleScaleDataReader:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass

    @property
    def source_ctx(self) -> tiledb.Ctx:
        pass

    @property
    def dest_ctx(self) -> tiledb.Ctx:
        pass

    @property
    def level_count(self) -> int:
        return 1

    def level_dtype(self, level: int) -> np.dtype:
        return self._data.dtype

    def level_shape(self, level: int) -> Tuple[int, ...]:
        return self._data.shape

    def level_image(
        self, level: int, tile: Optional[Tuple[slice, ...]] = None
    ) -> np.ndarray:
        return self._data[tile] if tile is not None else self._data

    def level_metadata(self, level: int) -> Dict[str, Any]:
        return {}
    
    @property
    def image_metadata(self) -> Dict[str, Any]:
        metadata: Dict[str, Any] = {}
        color_generator = iter_color(np.dtype(np.uint8), 3)
        metadata["channels"] = [
            {"id": f"{idx}", "name": f"{name}", "color": next(color_generator)}
            for idx, name in enumerate(["red", "green", "blue"])
        ]
        return metadata
    
    @property
    def original_metadata(self) -> Dict[str, Any]:
        return {}
    
    def optimal_reader(
        self, level: int, max_workers: int = 0
    ) -> Optional[Iterator[Tuple[Tuple[slice, ...], NDArray[Any]]]]:
        return None


class NapariMultiScaleDataReader(NapariDataReader):
    def __init__(self, data: MultiScaleData, logger:  Optional[logging.Logger] = None):
        super().__init__(data)

    def __enter__(self) -> NapariMultiScaleDataReader:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass

    @property
    def source_ctx(self) -> tiledb.Ctx:
        pass

    @property
    def dest_ctx(self) -> tiledb.Ctx:
        pass
    
    @property
    def level_count(self) -> int:
        return len(self._data)

    def level_dtype(self, level: int) -> np.dtype:
        return self._data[level].dtype

    def level_shape(self, level: int) -> Tuple[int, ...]:
        return self._data[level].shape

    def level_image(
        self, level: int, tile: Optional[Tuple[slice, ...]] = None
    ) -> np.ndarray:
        dask_array = self._data[level]
        if tile is not None:
            dask_array = dask_array[tile]
        return np.asarray(dask_array)

    def level_metadata(self, level: int) -> Dict[str, Any]:
        return {}


class NapariSingleScaleConverter(ImageConverterMixin[NapariSingleScaleDataReader, Any]):
    _ImageReaderType = NapariSingleScaleDataReader


class NapariMultiScaleConverter(ImageConverterMixin[NapariMultiScaleDataReader, Any]):
    _ImageReaderType = NapariMultiScaleDataReader


def napari_write_image_lossless(path, data, attributes):
    return _napari_write_image(path, data, lossless=True)


def napari_write_image_lossy(path, data, attributes):
    return _napari_write_image(path, data, lossless=False)


def _napari_write_image(path, data, lossless):
    kwargs = dict(compressor=tiledb.WebpFilter(lossless=lossless))
    if isinstance(data, MultiScaleData):
        kwargs.update(chunked=True, max_workers=os.cpu_count())
        converter = NapariMultiScaleConverter
    else:
        converter = NapariSingleScaleConverter
    converter.to_tiledb(source=data, output_path=path, **kwargs)
    return [path]
