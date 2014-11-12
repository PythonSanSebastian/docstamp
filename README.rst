stampy
======

.. image:: https://pypip.in/v/stampy/badge.png
    :target: https://pypi.python.org/pypi/stampy
    :alt: Latest PyPI version

.. image:: ''.png
   :target: ''
   :alt: Latest Travis CI build status

Initially it was a conference badge creator based on SVG templates (https://github.com/alexsavio/pydger), but we thought
it could be more generic and have any use.


Usage
-----

Stampy is a generic .SVG template renderer. The CSV header fields must match the ones in the SVG file.::

    stampy -i registrations.csv -t my_template.svg -f name -f surname -o out_folder -n talk_certificate --idx 10

Installation
------------
Install it with the command::

    pip install git+https://www.github.com/alexsavio/stampy.git

Requirements
------------

| Jinja2
| gspread


Compatibility
-------------
Stampy is compatible with Python 2 and 3.


Licence
-------
New BSD license

Authors
-------
The author of `stampy` is `Alexandre M. Savio @alexsavio`_.

Contributors:

Oier Etxaniz @oechaniz

Luis Javier Salvatierra @ljsalvatierra
