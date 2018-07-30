#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import io
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


setup_dict = dict(
    name="docstamp",
    version="0.4.1",
    url="https://github.com/PythonSanSebastian/docstamp.git",

    description="A SVG and LateX template renderer from table data based on Inkscape and Jinja2.",

    license='new BSD',
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
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)


if __name__ == '__main__':
    setup(**setup_dict)
