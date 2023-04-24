from magicgui import magicgui
from magicgui.widgets import FileEdit, PushButton
from napari_plugin_engine import napari_hook_implementation
import warnings
import os
from types import FunctionType
from typing import List, Union

from napari_plugin_engine import napari_hook_implementation
from magicgui import magic_factory
from magicgui.widgets import FileEdit
from qtpy.QtWidgets import QPushButton
import napari
import tiledb
from tiledb.bioimg.openslide import TileDBOpenSlide
import numpy as np
from typing import TYPE_CHECKING
from pathlib import Path

if TYPE_CHECKING:
    # your plugin doesn't need to import napari at all just to use these types
    # just put these imports here and wrap the hints in quotes
    import napari.types
    import napari.viewer

from qtpy.QtWidgets import QWidget, QGridLayout
from magicgui.widgets import FileEdit

#
# class MyWidget(QWidget):
#     def __init__(self, napari_viewer):
#         self.viewer = napari_viewer
#         super().__init__()
#
#         # initialize layout
#         layout = QGridLayout()
#
#         # add a button
#         btn = QPushButton('Click me!', self)
#
#         def trigger():
#             print("napari has", len(napari_viewer.layers), "layers")
#
#         btn.changed.connect(trigger)
#         layout.addWidget(btn)
#
#         # activate layout
#         self.setLayout(layout)

#
# @magic_factory(image_path = {"widget_type":'FileEdit' , "label":"Load Image"}, call_button = "Import Images")
# def gui_load_file(
#     viewer: 'napari.viewer.Viewer',
#     image_path : Path) -> 'napari.types.LabelsData':
#
#     if tiledb.object_type(image_path) == 'group':
#         try:
#             slide = TileDBOpenSlide(image_path)
#         except tiledb.TileDBError as ex:
#             warnings.warn(f"Failed to open {image_path}: {ex}")
#             return None
#
#     def reader_function(_):
#         level_data = list(map(slide.read_level_dask, range(slide.level_count)))
#         name = os.path.basename(os.path.abspath(image_path))
#         return [(level_data, {"name": name})]
#
#     #reader_function()
#     viewer.add_image(np.random.random((5, 5)), colormap='red', opacity=0.8)


# def load_data(uri: str):
#     if tiledb.object_type(uri) == 'group':
#         try:
#             slide = TileDBOpenSlide(uri)
#         except tiledb.TileDBError as ex:
#             warnings.warn(f"Failed to open {uri}: {ex}")
#             return None
#
#     def reader_function(_):
#         level_data = list(map(slide.read_level_dask, range(slide.level_count)))
#         name = os.path.basename(os.path.abspath(uri))
#         return [(level_data, {"name": name})]
#
#     return reader_function
#
from typing import Sequence


@magicgui(filenames={"label": "Choose TileDB files:", "filter": "*.tdb"})
def filespicker(filenames: Sequence[Path]):
    """Take a filename and do something with it."""
    print("The filenames are:", filenames)
    return filenames
# import napari
# from pathlib import Path
#
# @magic_factory(call_button="Run segmentation",filename={"label": "Pick a file:"})
# def gui_load_file(filename=Path.home(), napari_viewer=napari.Viewer()):
#     print('Test')
#     print('Test')
#
@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return filespicker


#
# @magic_factory(auto_call=False, call_button=True, filename={'widget_type': FileEdit, 'label': 'File:', 'mode': 'r'})
# def gui_load_file(filename) -> FunctionType:
#     #def print_path():
#     return print(f"Selected file:")
    # button = PushButton(label='Load', tooltip='Load the file', auto_trigger=False)
    # button.changed.connect(print_path)

# @magic_factory(auto_call=False, path={'label': 'File:', 'mode': 'r'})
# def gui_load_file(filename: FileEdit()):
#
#     def tiledb_load():
#         import tiledb
#         from tiledb.bioimg.openslide import TileDBOpenSlide
#
#         if tiledb.object_type(str(filename.value)) == 'group':
#             try:
#                 slide = TileDBOpenSlide(str(filename.value))
#             except tiledb.TileDBError as ex:
#                 warnings.warn(f"Failed to open {str(filename.value)}: {ex}")
#                 return None
#
#         def reader_function(_):
#             level_data = list(map(slide.read_level_dask, range(slide.level_count)))
#             name = os.path.basename(os.path.abspath(str(filename.value)))
#             return [(level_data, {"name": name})]
#
#         return reader_function

    # button = PushButton(label='Load', tooltip='Load the file', auto_trigger=False)
    # button.changed.connect(tiledb_load)

#
# @napari_hook_implementation
# def napari_experimental_provide_function_widget() -> Union[FunctionType, List[FunctionType]]:
#     return gui_load_file
