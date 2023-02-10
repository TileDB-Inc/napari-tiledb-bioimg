import pytest
import skimage as sk
from napari.layers.image.image import MultiScaleData
from tiledb.bioimg.openslide import TileDBOpenSlide

from napari_tiledb_bioimg import napari_write_image_lossless, napari_write_image_lossy


@pytest.mark.parametrize(
    "write_image", [napari_write_image_lossless, napari_write_image_lossy]
)
def test_write_image(tmp_path, write_image):
    image = sk.data.astronaut()
    write_image(str(tmp_path), image, {})
    with TileDBOpenSlide(str(tmp_path)) as t:
        assert t.level_count == 1
        assert_similar_images(image, t.read_level(0), write_image)


@pytest.mark.parametrize(
    "write_image", [napari_write_image_lossless, napari_write_image_lossy]
)
def test_write_image_pyramid(tmp_path, write_image):
    image = sk.data.astronaut()
    pyramid = sk.transform.pyramid_gaussian(image, max_layer=3, channel_axis=-1)
    data = MultiScaleData(map(sk.util.img_as_ubyte, pyramid))
    write_image(str(tmp_path), data, {})
    with TileDBOpenSlide(str(tmp_path)) as t:
        assert t.level_count == len(data)
        for i in range(t.level_count):
            assert_similar_images(data[i], t.read_level(i), write_image)


def assert_similar_images(image1, image2, write_image):
    similarity = sk.metrics.structural_similarity(image1, image2, channel_axis=-1)
    if write_image is napari_write_image_lossless:
        assert similarity == 1
    else:
        assert similarity > 0.95
