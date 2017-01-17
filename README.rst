.. -*- mode: rst -*-

|Python27|_ |Python35|_ |PyPi|_

.. |Python27| image:: https://img.shields.io/badge/python-2.7-blue.svg
.. _Python27: https://badge.fury.io/py/docstamp

.. |Python35| image:: https://img.shields.io/badge/python-3.5-blue.svg
.. _Python35: https://badge.fury.io/py/docstamp

.. |PyPi| image:: https://badge.fury.io/py/docstamp.svg
.. _PyPi: https://badge.fury.io/py/docstamp

docstamp
========

Initially it was a conference badge creator based on SVG templates (https://github.com/PythonSanSebastian/pydger), but we thought
it could be more generic and have many other applications.

DocStamp is a generic template renderer which takes the data from a .CSV file or a Google Spreadsheet and creates
one rendered template file for each row of the data.

It is PDF centric, however it can also export in some cases to PNG.

It needs:

- Inkscape for .SVG templates, and

- PDFLateX or XeLateX for LateX templates.


CLI Usage
---------

The CSV header fields must match the ones in the template file.::

    docstamp create -i badge.csv -t badge_template.svg -o badges

Installation
------------
To install the development version::

    pip install git+https://www.github.com/PythonSanSebastian/docstamp.git

To install the latest release::

    pip install docstamp


Requirements
------------

See `requirements.txt` file. Also you will need Inkscape, XeLatex, or PDFLatex
installed in your system.


Compatibility
-------------
DocStamp is compatible with Python 2 (we wish to believe) and 3.
We could not test it on Windows.


License
-------
New BSD license

Authors
-------
Alexandre M. Savio @alexsavio


Contributors
------------

Oier Etxaniz @oechaniz

Luis Javier Salvatierra @ljsalvatierra
