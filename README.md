# docstamp

[![](https://img.shields.io/badge/python-3.6-blue.svg)](https://badge.fury.io/py/docstamp)
[![](https://badge.fury.io/py/docstamp.svg)](https://badge.fury.io/py/docstamp)

Initially it was a conference badge creator based on SVG templates,
but we thought it could be more generic and have many other applications.

DocStamp is a generic template renderer which takes the data from a
.CSV file and creates one rendered template file for each row of the data.

It is PDF centric, however it can also export in some cases to PNG.

It needs:

- Inkscape or rsvg-convert for .SVG templates, and
- PDFLateX or XeLateX for LateX templates.

## CLI Usage

The CSV header fields must match the ones in the template file.

```bash
docstamp create -i badge.csv -t badge_template.svg -o badges
```

## Installation

To install the development version:

```bash
python -m pip install git+https://www.github.com/PythonSanSebastian/docstamp.git
```

To install the latest release:

```bash
python -m pip install docstamp
```

## Requirements
See `setup.cfg` file. Also you will need Inkscape, XeLatex, or PDFLatex
installed in your system.

For unicode support in SVG exports, you need to install `rsvg-convert`,
which is available in `librsvg-bin`.

## Compatibility

DocStamp is compatible with Python 2 (we wish to believe) and 3.

We could not test it on Windows.

## Authors

- Alexandre M. Savio @alexsavio

## Contributors

- Oier Etxaniz @oechaniz
- Luis Javier Salvatierra @ljsalvatierra
- Haseeb Majid
