#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import io
import sys
from setuptools import setup, find_packages


# long description
def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


# Get version without importing, which avoids dependency issues
module_name = find_packages(exclude=['tests'])[0]
version_pyfile = os.path.join(module_name, 'version.py')
exec(compile(read(version_pyfile), version_pyfile, 'exec'))

LICENSE = 'new BSD'

setup_dict = dict(
    name=module_name,
    version=__version__,
    url="https://github.com/PythonSanSebastian/docstamp.git",

    description="A SVG and LateX template renderer from table data based on Inkscape and Jinja2.",

    license=LICENSE,

    author='Alexandre M. Savio',
    author_email='alexsavio@gmail.com',
    maintainer='Alexandre M. Savio',
    maintainer_email='alexsavio@gmail.com',

    packages=find_packages(),

    install_requires=read('requirements.txt'),

    long_description=read('README.rst', 'CHANGES.rst'),

    platforms='Linux/MacOSX',

    entry_points='''
      [console_scripts]
      docstamp=docstamp.cli:cli
      ''',

    scripts=['scripts/svg_export.py',
             'scripts/embed_font_to_svg.py'],

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)


if __name__ == '__main__':
    setup(**setup_dict)
