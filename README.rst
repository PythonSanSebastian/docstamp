docstamp
======

.. image:: https://pypip.in/v/docstamp/badge.png
    :target: https://pypi.python.org/pypi/docstamp
    :alt: Latest PyPI version

.. image:: ''.png
   :target: ''
   :alt: Latest Travis CI build status


Initially it was a conference badge creator based on SVG templates (https://github.com/PythonSanSebastian/pydger), but we thought
it could be more generic and have many other applications.


Usage
-----

DocStamp is a generic .SVG template renderer. The CSV header fields must match the ones in the SVG file.::

    docstamp -i registrations.csv -t my_template.svg -f name -f surname -o out_folder -n talk_certificate --idx 10

Installation
------------
To install the development version::

    pip install git+https://www.github.com/PythonSanSebastian/docstamp.git

To install the latest release::

    pip install docstamp


Requirements
------------

.. include:: ./requirements.txt
   :literal:

gspread
Pillow
jinja2

Compatibility
-------------
DocStamp is compatible with Python 2 and 3.


Licence
-------
New BSD license

Authors
-------
The author of `docstamp` is `Alexandre M. Savio @PythonSanSebastian`_.

Contributors:

Oier Etxaniz @oechaniz

Luis Javier Salvatierra @ljsalvatierra
