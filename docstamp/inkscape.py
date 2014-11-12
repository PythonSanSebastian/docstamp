# -*- coding: utf-8 -*-

import os
import os.path as op
import logging
import subprocess
from subprocess import CalledProcessError

from .config import INKSCAPE_BINPATH


log = logging.getLogger(__name__)


class FileExporter(object):
    """A base class to template a basic file converter: from the template to
    anything the output_filepath extension says.
    """
    def export(input_filepath, output_filepath, args_string, **kwargs):
        raise NotImplementedError


#class Inkscape(FileExporter):
#    def export(input_filepath, output_filepath, args_string, **kwargs):
#TODO?


def call_inkscape(args_string):
    """Call inkscape CLI with arguments and returns its return value
    """
    if INKSCAPE_BINPATH is None or not op.exists(INKSCAPE_BINPATH):
        raise IOError('Inkscape binary has not been found. Please check '
                      'configuration.')

    try:
        ret = subprocess.check_call([INKSCAPE_BINPATH] + args_string)
        return ret
    except CalledProcessError as ce:
        log.exception("Error calling inkscape with arguments: "
                      "{} \n With return code: {}".format(args_string,
                                                          ce.returncode))
        raise


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

    """
    if not op.exists(input_file):
        log.error('File {} not found.'.format(input_file))
        raise IOError((0, 'File not found.', input_file))

    if not '=' in export_flag:
        export_flag += ' '

    try:
        ret = call_inkscape("{}{} --export-dpi={} {}".format(export_flag,
                                                             output_file, dpi,
                                                             input_file).split())
    except CalledProcessError as ce:
        log.exception("Error converting file {} to PDF.".format(input_file))
        raise


def svg2pdf(svg_file_path, pdf_file_path, dpi=150):
    """ Transform SVG file to PDF file
    """
    return inkscape_export(svg_file_path, pdf_file_path, export_flag="-A",
                           dpi=dpi)


def svg2png(svg_file_path, png_file_path, dpi=150):
    """ Transform SVG file to PNG file
    """
    return inkscape_export(svg_file_path, png_file_path, export_flag="-e",
                           dpi=dpi)
