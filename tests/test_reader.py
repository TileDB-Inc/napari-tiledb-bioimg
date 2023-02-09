import pathlib

import numpy as np
import pytest
import tiledb

from napari_tiledb_bioimg import napari_get_reader

TEST_DIR = pathlib.Path(__file__).parent / "rand_uint16.tdb"


def test_get_reader_not_dir_fail(tmp_path):
    """Not receiving a directory"""
    f = tmp_path / "hello.txt"
    assert not f.is_file()
    f.write_text("")
    assert f.is_file()

    with pytest.warns(UserWarning, match="Not a directory"):
        assert napari_get_reader(str(f)) is None


def test_get_reader_invalid_dir_fail(tmp_path):
    """Not receiving a proper TileDB group directory"""
    with pytest.warns(UserWarning, match="Failed to open"):
        assert napari_get_reader(str(tmp_path)) is None


def test_get_reader_list_fail():
    """Not receiving a single directory"""
    with pytest.warns(UserWarning, match="Not a single path"):
        assert napari_get_reader([str(TEST_DIR)]) is None


def test_get_reader_succeed():
    """Valid TileDB group dir"""
    original_data = []
    for level_dir in sorted(TEST_DIR.glob("l_*")):
        with tiledb.open(str(level_dir), attr="intensity") as a:
            original_data.append(a[:])

    reader = napari_get_reader(str(TEST_DIR))
    assert callable(reader)

    # make sure we're delivering the right format
    layer_data_list = reader(str(TEST_DIR))
    assert isinstance(layer_data_list, list) and len(layer_data_list) == 1
    layer_data_tuple = layer_data_list[0]
    assert isinstance(layer_data_tuple, tuple) and len(layer_data_tuple) == 2

    # make sure it's the same as it started
    layers_data = layer_data_tuple[0]
    assert isinstance(layers_data, list)
    assert len(layers_data) == len(original_data)
    for layer_data, orig_layer_data in zip(layers_data, original_data):
        # original data are in CYX axes, layer data are YXC
        transposed_layer_data = np.moveaxis(layer_data, 2, 0)
        np.testing.assert_allclose(transposed_layer_data, orig_layer_data)
