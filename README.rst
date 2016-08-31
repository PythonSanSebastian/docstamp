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

    docstamp -i badge.csv -t badge_template.svg -o badges

Installation
------------
To install the development version::

    pip install git+https://www.github.com/PythonSanSebastian/docstamp.git

To install the latest release::

    pip install docstamp


Requirements
------------

- Pillow>=3.1.0
- jinja2>=2.8
- gspread>=0.3.0
- oauth2client>=2.0.0
- pycrypto>=2.6.1
- svgutils>=0.1.0
- PyPDF2>=1.25.1
- qrcode>=5.1


Compatibility
-------------
DocStamp is compatible with Python 2 and 3. I could not test it on Windows.


Licence
-------
New BSD license

Authors
-------
Alexandre M. Savio @alexsavio


Contributors
------------

Oier Etxaniz @oechaniz

Luis Javier Salvatierra @ljsalvatierra

