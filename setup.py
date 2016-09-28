#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os.path as op
import io
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


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
version_pyfile = op.join(module_name, 'version.py')
exec(compile(read(version_pyfile), version_pyfile, 'exec'))


LICENSE = 'new BSD'

setup_dict = dict(
    name=module_name,
    version=__version__,
	url="https://github.com/PythonSanSebastian/{}.git".format(module_name),

    description="A SVG and LateX template renderer from table data based on Inkscape and Jinja2.",

    license=LICENSE,

    author='Alexandre M. Savio',
    author_email='alexsavio@gmail.com',
    maintainer='Alexandre M. Savio',
    maintainer_email='alexsavio@gmail.com',

    packages=find_packages(),

    install_requires=[
                      'jinja2',
                      'Pillow',
                      ],

    long_description=read('README.rst', 'CHANGES.rst'),

    platforms='Linux/MacOSX',

    entry_points='''
      [console_scripts]
      docstamp=docstamp.cli:cli
      ''',

    scripts=['scripts/svg_export.py',],

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    extras_require={
        'testing': ['pytest', 'pytest-cov'],
    }
)


# Python3 support keywords
if sys.version_info >= (3,):
    setup_dict['use_2to3'] = False
    setup_dict['convert_2to3_doctests'] = ['']
    setup_dict['use_2to3_fixers'] = ['']


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup_dict.update(dict(tests_require=['pytest'],
                       cmdclass={'test': PyTest}))


if __name__ == '__main__':
    setup(**setup_dict)
