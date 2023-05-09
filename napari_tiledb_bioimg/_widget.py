from typing import TYPE_CHECKING
import os
from qtpy.QtWidgets import QWidget
from qtpy import QtWidgets

if TYPE_CHECKING:
    import napari


class TileDBWidget(QWidget):
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        layout = QtWidgets.QFormLayout()
        fields_grow = QtWidgets.QFormLayout.ExpandingFieldsGrow
        self.setLayout(layout)
        layout.setFieldGrowthPolicy(fields_grow)
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.folderEdit = QtWidgets.QLineEdit(self.path)
        layout.insertRow(0, 'Path:', self.folderEdit)

        #Open Button
        self.openbtn = QtWidgets.QPushButton('Open')
        self.openbtn.clicked.connect(self._open_tdb)
        layout.insertRow(1, self.openbtn)

        # Sample button
        self.sample_btn = QtWidgets.QPushButton('Sample')
        self.sample_btn.clicked.connect(self._sample_tdb)
        layout.insertRow(1, self.sample_btn)

    def _set_scale_bar(self):
        self.viewer.scale_bar.visible = True
        self.viewer.scale_bar.colored = True
        image_pixel_meta = self.viewer.layers[0].metadata['metadata']['OME']['Image'][0]['Pixels']
        mpp_x = image_pixel_meta['PhysicalSizeX']
        mpp_y = image_pixel_meta['PhysicalSizeY']
        self.viewer.layers[0].scale = [mpp_x, mpp_y]
        self.viewer.scale_bar.unit = image_pixel_meta['PhysicalSizeXUnit']

    def _open_tdb(self):
        tdb_path = self.folderEdit.text()
        if tdb_path:
            self.viewer.open(tdb_path, plugin='napari-tiledb-bioimg')
            self._set_scale_bar()

    def _sample_tdb(self):
        self.viewer.open(os.path.join(self.path, 'samples/CMU-1-Small-Region-rgb.ome.tiff.tdb'),
                         plugin='napari-tiledb-bioimg'
                         )
        self._set_scale_bar()
