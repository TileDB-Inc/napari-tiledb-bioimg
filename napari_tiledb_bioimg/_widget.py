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
        self.openbtn = QtWidgets.QPushButton('Open')
        self.openbtn.clicked.connect(self._open_tdb)
        layout.insertRow(1, self.openbtn)

    def _open_tdb(self):
        tdb_path = self.folderEdit.text()
        if tdb_path:
            self.viewer.open(tdb_path, plugin='napari-tiledb-bioimg')