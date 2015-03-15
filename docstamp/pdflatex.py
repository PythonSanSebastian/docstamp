# coding=utf-8
# -------------------------------------------------------------------------------
# Author: Alexandre Manhaes Savio <alexsavio@gmail.com>
# Grupo de Inteligencia Computational <www.ehu.es/ccwintco>
# Universidad del Pais Vasco UPV/EHU
#
# 2015, Alexandre Manhaes Savio
# Use this at your own risk!
# -------------------------------------------------------------------------------

import os
import shutil
import os.path      as      op
from   glob         import  glob

from   .commands    import  call_command
from   .filenames   import  remove_ext


def tex2pdf(tex_file, output_file=None, output_format='pdf'):
    """ Call PDFLatex to convert TeX files to PDF.

    Parameters
    ----------
    tex_file: str
        Path to the input LateX file.

    output_file: str
        Path to the output PDF file.
        If None, will use the same output directory as the tex_file.

    output_format: str
        Output file format. Choices: 'pdf' or 'dvi'. Default: 'pdf'

    Returns
    -------
    return_value
        PDFLatex command call return value.
    """
    if not op.exists(tex_file):
        raise IOError('Could not find file {}.'.format(tex_file))

    if output_format != 'pdf' and output_format != 'dvi':
        raise ValueError("Invalid output format given {}. Can only accept 'pdf' or 'dvi'.".format(output_format))

    cmd_name = 'pdflatex'

    args_strings = ' '
    if output_file is not None:
        args_strings += '-output-directory={} '.format(op.abspath(op.dirname(output_file)))

    if output_file:
        args_strings += '-output-format={} '.format(output_format)
        result_dir    = op.dirname(output_file)
    else:
        result_dir    = op.dirname(tex_file)

    args_strings += tex_file

    ret = call_command(cmd_name, args_strings.split())

    result_file = op.join(result_dir, remove_ext(op.basename(tex_file)) + '.' + output_format)
    if op.exists(result_file):
        shutil.move(result_file, output_file)
    else:
        raise IOError('Could not find PDFLatex result file.')

    [os.remove(f) for f in glob(op.join(result_dir, '*.aux'))]
    [os.remove(f) for f in glob(op.join(result_dir, '*.log'))]

    return ret
