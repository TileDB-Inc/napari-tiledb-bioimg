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

        # Path placeholder
        layout.setFieldGrowthPolicy(fields_grow)
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.folderEdit = QtWidgets.QLineEdit(self.path)
        layout.insertRow(0, 'Path:', self.folderEdit)

        # Open Button
        self.openbtn = QtWidgets.QPushButton('Open')
        self.openbtn.clicked.connect(self._open_tdb)
        layout.insertRow(1, self.openbtn)

        # Sample button
        self.sample_btn = QtWidgets.QPushButton('Load Sample Dataset')
        self.sample_btn.clicked.connect(self._sample_tdb)
        layout.insertRow(2, self.sample_btn)

    def _open_tdb(self):
        tdb_path = self.folderEdit.text()
        if tdb_path:
            self.viewer.open(tdb_path, plugin='napari-tiledb-bioimg')

    def _sample_tdb(self):
        self.viewer.open(os.path.join(self.path, 'samples/CMU-1-Small-Region-rgb.ome.tiff.tdb'),
                         plugin='napari-tiledb-bioimg'
                         )