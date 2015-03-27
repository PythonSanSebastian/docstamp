# coding=utf-8
# -------------------------------------------------------------------------------
# Author: Alexandre Manhaes Savio <alexsavio@gmail.com>
# Grupo de Inteligencia Computational <www.ehu.es/ccwintco>
# Universidad del Pais Vasco UPV/EHU
#
# 2015, Alexandre Manhaes Savio
# Use this at your own risk!
# -------------------------------------------------------------------------------

import os.path      as op
import logging

from   .config      import get_inkscape_binpath
from   .commands    import call_command

log = logging.getLogger(__name__)


class FileExporter(object):
    """A base class to template a basic file converter: from the template to
    anything the output_filepath extension says.
    """
    def export(input_filepath, output_filepath, args_string, **kwargs):
        raise NotImplementedError


def call_inkscape(args_strings, inkscape_binpath=None):
    """Call inkscape CLI with arguments and returns its return value.

    Parameters
    ----------
    args_string: list of str

    inkscape_binpath: str

    Returns
    -------
    return_value
        Inkscape command CLI call return value.
    """
    log.debug('Looking for the binary file for inkscape.')

    if inkscape_binpath is None:
        inkscape_binpath = get_inkscape_binpath()

    if inkscape_binpath is None or not op.exists(inkscape_binpath):
        raise IOError('Inkscape binary has not been found. Please check '
                      'configuration.')

    return call_command(inkscape_binpath, args_strings)


def inkscape_export(input_file, output_file, export_flag="-A", dpi=90):
    """ Call Inkscape to export the input_file to outpu_file using the
    specific export argument flag for the output file type.

    Parameters
    ----------

    input_file: str
        Path to the input file

    output_file: str
        Path to the output file

    export_flag: str
        Inkscape CLI flag to indicate the type of the output file

    Returns
    -------
    return_value
        Command call return value

    """
    if not op.exists(input_file):
        log.error('File {} not found.'.format(input_file))
        raise IOError((0, 'File not found.', input_file))

    if not '=' in export_flag:
        export_flag += ' '

    arg_strings  = []
    arg_strings += ['{}{}'.format(export_flag, output_file)]
    arg_strings += ['--export-dpi={}'.format(dpi)]
    arg_strings += [input_file]

    return call_inkscape(arg_strings)


def svg2pdf(svg_file_path, pdf_file_path, dpi=150):
    """ Transform SVG file to PDF file
    """
    return inkscape_export(svg_file_path, pdf_file_path, export_flag="-A", dpi=dpi)


def svg2png(svg_file_path, png_file_path, dpi=150):
    """ Transform SVG file to PNG file
    """
    return inkscape_export(svg_file_path, png_file_path, export_flag="-e", dpi=dpi)
