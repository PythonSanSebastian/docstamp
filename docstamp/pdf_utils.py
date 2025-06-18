"""Function helpers to manage PDF files."""

from __future__ import annotations

import os
from pathlib import Path

from PyPDF2 import PdfFileMerger, PdfFileReader

from .commands import call_command


def merge_pdfs(
    pdf_filepaths: list[os.PathLike | str],
    out_filepath: str | os.PathLike,
) -> Path:
    """Merge all the PDF files in `pdf_filepaths` in a new PDF file `out_filepath`.

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
        pdf_filepath = Path(pdf)
        merger.append(PdfFileReader(pdf_filepath.open("rb")))

    merger.write(str(out_filepath))
    return out_filepath


def pdf_to_cmyk(input_file: os.PathLike | str, output_file: os.PathLike | str) -> int:
    """Use `gs` (Ghostscript) to convert the colour model of a PDF to CMYK
    for printing.

    Parameters
    ----------
    input_file: str

    output_file: str

    Returns
    -------
    exit_code: int
        The exit code of the `gs` command call.
    """
    cmd_args = [
        "-dSAFER",
        "-dBATCH",
        "-dNOPAUSE",
        "-dNOCACHE",
        "-sDEVICE=pdfwrite",
        "-sColorConversionStrategy=CMYK",
        "-dProcessColorModel=/DeviceCMYK",
        f'-sOutputFile="{output_file}" "{input_file}"',
    ]
    return call_command("gs", cmd_args)
