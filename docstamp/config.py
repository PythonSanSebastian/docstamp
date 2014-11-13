# -*- coding: utf-8 -*-

import os
import logging
from jinja2 import Environment, FileSystemLoader

LOGGING_LVL = logging.INFO
logging.basicConfig(level=LOGGING_LVL)


def which(program):
    import os

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


INKSCAPE_BINPATH = which('inkscape')
LYX_BINPATH = which('lyx')

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'templates')

# JINJA_ENV = Environment(loader=PackageLoader('docstamp', 'templates'))
JINJA_ENV = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

# FILE_EXPORTERS = {'.svg': Inkscape,}
#                   '.tex': PdfLatex,
#                   '.lyx': LyX}
