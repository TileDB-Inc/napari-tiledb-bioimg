# napari-tiledb-bioimg

[![License MIT](https://img.shields.io/pypi/l/napari-tiledb-bioimg.svg?color=green)](https://github.com/TileDB-Inc/napari-tiledb-bioimg/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/napari-tiledb-bioimg.svg?color=green)](https://pypi.org/project/napari-tiledb-bioimg)
[![Python Version](https://img.shields.io/pypi/pyversions/napari-tiledb-bioimg.svg?color=green)](https://python.org)
[![tests](https://github.com/TileDB-Inc/napari-tiledb-bioimg/workflows/tests/badge.svg)](https://github.com/TileDB-Inc/napari-tiledb-bioimg/actions)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/napari-tiledb-bioimg)](https://napari-hub.org/plugins/napari-tiledb-bioimg)

This plugin supports reading [TileDB-BioImaging](https://github.com/TileDB-Inc/TileDB-BioImaging) multi-resolution arrays within [Napari](https://www.napari.org).

----------------------------------

## Demo

https://github.com/TileDB-Inc/napari-tiledb-bioimg/assets/327706/155a9b90-5006-46e0-9242-ef4aa6f2b4bb

## Installation

[pending PyPI release!] You can install `napari-tiledb-bioimg` via [pip]:

    pip install napari-tiledb-bioimg

## Quickstart

After [ingesting data using `tiledb-bioimg`](https://github.com/TileDB-Inc/TileDB-BioImaging#examples), then:

- Local images may be loaded using Napari's `File -> Open Folder`, and selecting the TileDB array folder. Choose the `napari-tiledb-bioimg` plugin, if prompted.

- Remote arrays (S3, TileDB Cloud) may be loaded using either the `napari` CLI command:

```
napari --plugin napari-tiledb-bioimg s3://<bucket>/<path/to/tiledb_array>
```

- or the Napari viewer `load` command within a Python prompt:

```
# Within a Napari-enabled Python/IPython prompt, run:
import napari
viewer = napari.Viewer()

viewer.open("tiledb://<namespace>/<array name or UUID>", plugin="napari-tiledb-bioimg")
```


## Contributing

Contributions are very welcome. Tests can be run with tox or pytest.

### Installation from git:

```
pip install git+https://github.com/TileDB-Inc/napari-tiledb-bioimg.git
```

## License

Distributed under the terms of the [MIT](https://github.com/TileDB-Inc/napari-tiledb-bioimg/blob/main/LICENSE) license,
"napari-tiledb-bioimg" is free and open source software.

## Issues

If you encounter any problems, please [file an issue](https://github.com/TileDB-Inc/napari-tiledb-bioimg/issues/new) along with a detailed description.
