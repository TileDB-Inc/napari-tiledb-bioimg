# napari-tiledb-bioimg

[![License MIT](https://img.shields.io/pypi/l/napari-tiledb-bioimg.svg?color=green)](https://github.com/TileDB-Inc/napari-tiledb-bioimg/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/napari-tiledb-bioimg.svg?color=green)](https://pypi.org/project/napari-tiledb-bioimg)
[![Python Version](https://img.shields.io/pypi/pyversions/napari-tiledb-bioimg.svg?color=green)](https://python.org)
[![tests](https://github.com/TileDB-Inc/napari-tiledb-bioimg/workflows/tests/badge.svg)](https://github.com/TileDB-Inc/napari-tiledb-bioimg/actions)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/napari-tiledb-bioimg)](https://napari-hub.org/plugins/napari-tiledb-bioimg)

This plugin supports reading and writing TileDB-BioImaging multi-resolution arrays within Napari.

----------------------------------

This [napari] plugin was generated with [Cookiecutter] using [@napari]'s [cookiecutter-napari-plugin] template.
## Demo
![screencast](https://github.com/TileDB-Inc/napari-tiledb-bioimg/releases/download/0.1-rc0/napari-tiledb-bioimg-demo.480p.mp4)

<!--
Don't miss the full getting started guide to set up your new package:
https://github.com/napari/cookiecutter-napari-plugin#getting-started

and review the napari docs for plugin developers:
https://napari.org/stable/plugins/index.html
-->

## Installation

[pending PyPI release!] You can install `napari-tiledb-bioimg` via [pip]:

    pip install napari-tiledb-bioimg

## Quickstart

After [ingesting data using `tiledb-bioimg`](https://github.com/TileDB-Inc/TileDB-BioImaging#examples), then:

- Local images can be loaded using Napari's `File -> Open Folder`, and selecting the TileDB array folder. Choose the `napari-tiledb-bioimg` plugin, if prompted.

- Remote arrays (S3, TileDB Cloud) may be loaded using either the `napari` CLI command:

```
napari --plugin napari-tiledb-bioimg s3://<bucket>/<path/to/tiledb_array>
```

- ... or the Napari viewer load command within the Python prompt:

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

Distributed under the terms of the [MIT] license,
"napari-tiledb-bioimg" is free and open source software.

## Issues

If you encounter any problems, please [file an issue](https://github.com/TileDB-Inc/napari-tiledb-bioimg/issues/new) along with a detailed description.
