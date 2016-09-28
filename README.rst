docstamp
========

.. image:: https://pypip.in/v/docstamp/badge.png
    :target: https://pypi.python.org/pypi/docstamp
    :alt: Latest PyPI version

.. image:: ''.png
   :target: ''
   :alt: Latest Travis CI build status



Initially it was a conference badge creator based on SVG templates (https://github.com/PythonSanSebastian/pydger), but we thought
it could be more generic and have many other applications.

DocStamp is a generic template renderer which takes the data from a .CSV file or a Google Spreadsheet and creates
one rendered template file for each row of the data.

It needs Inkscape for .SVG templates and PDFLateX or XeLateX for LateX templates.

Usage
-----

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
