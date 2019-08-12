"""
Function helpers to manage PDF files.
"""
from PyPDF2 import PdfFileMerger, PdfFileReader

from docstamp.commands import call_command


def merge_pdfs(pdf_filepaths, out_filepath):
    """ Merge all the PDF files in `pdf_filepaths` in a new PDF file `out_filepath`.

    Parameters
    ----------
    pdf_filepaths: list of str
        Paths to PDF files.

    out_filepath: str
        Path to the result PDF file.

    Returns
    -------
    path: str
        The output file path.
    """
    merger = PdfFileMerger()
    for pdf in pdf_filepaths:
        merger.append(PdfFileReader(open(pdf, 'rb')))

    merger.write(out_filepath)

    return out_filepath


def pdf_to_cmyk(input_file, output_file):
    """ User `gs` (Ghostscript) to convert the colore model of a PDF to CMYK.

    Parameters
    ----------
    input_file: str

    output_file: str
    """
    cmd_args = [
        '-dSAFER',
        '-dBATCH',
        '-dNOPAUSE',
        '-dNOCACHE',
        '-sDEVICE=pdfwrite',
        '-sColorConversionStrategy=CMYK',
        '-dProcessColorModel=/DeviceCMYK',
        '-sOutputFile="{}" "{}"'.format(output_file, input_file),
    ]
    call_command('gs', cmd_args)
