"""A module to handle Inkscape CLI commands for SVG and PDF conversions."""

from __future__ import annotations

import os
from pathlib import Path

from docstamp.commands import call_command
from docstamp.config import get_inkscape_binpath
from docstamp.svg_utils import rsvg_export


def call_inkscape(
    args_strings: list[str],
    inkscape_binpath: os.PathLike | str | None = None,
) -> int:
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
    log.debug("Looking for the binary file for inkscape.")

    if inkscape_binpath is None:
        inkscape_binpath = get_inkscape_binpath()

    if inkscape_binpath is None or not Path.exists(inkscape_binpath):
        raise FileNotFoundError(
            "Inkscape binary has not been found. Please check configuration."
        )

    return call_command(cmd_name=inkscape_binpath, args_strings=args_strings)


def inkscape_export(
    input_file: os.PathLike | str,
    output_file: os.PathLike | str,
    export_flag: str = "-A",
    dpi: int = 90,
    inkscape_binpath: os.PathLike | str | None = None,
) -> int:
    """Call Inkscape to export the input_file to output_file using the
    specific export argument flag for the output file type.

    Parameters
    ----------

    input_file: str
        Path to the input file

    output_file: str
        Path to the output file

    export_flag: str
        Inkscape CLI flag to indicate the type of the output file

    dpi: int
        Dots per inch for the output file. Default is 90.

    inkscape_binpath: str | None
        Path to the Inkscape command binary.
        If None, it will try to find the binary in your computer.

    Returns
    -------
    return_value
        Command call return value

    """
    if not Path.exists(input_file):
        raise FileNotFoundError(f"File {input_file} not found.")

    if "=" not in export_flag:
        export_flag += " "

    arg_strings = []
    arg_strings += ["--without-gui"]
    arg_strings += ["--export-text-to-path"]
    arg_strings += ["--export-pdf-version=1.5"]
    arg_strings += [f'{export_flag}"{output_file}"']
    arg_strings += [f"--export-dpi={dpi}"]
    arg_strings += [f'"{input_file}"']
    return call_inkscape(arg_strings=arg_strings, inkscape_binpath=inkscape_binpath)


def svg2pdf(
    svg_file_path: os.PathLike | str,
    pdf_file_path: os.PathLike | str,
    dpi: int = 150,
    command_binpath: os.PathLike | str | None = None,
    support_unicode: bool = False,
):
    """Transform SVG file to PDF file"""

    if support_unicode:
        return rsvg_export(
            input_file=svg_file_path,
            output_file=pdf_file_path,
            dpi=dpi,
            rsvg_binpath=command_binpath,
        )

    return inkscape_export(
        input_file=svg_file_path,
        output_file=pdf_file_path,
        export_flag="-A",
        dpi=dpi,
        inkscape_binpath=command_binpath,
    )


def svg2png(
    svg_file_path: os.PathLike | str,
    png_file_path: os.PathLike | str,
    dpi: int = 150,
    inkscape_binpath: os.PathLike | str | None = None,
) -> int:
    """Transform SVG file to PNG file"""
    return inkscape_export(
        intput_file=svg_file_path,
        output_file=png_file_path,
        export_flag="-e",
        dpi=dpi,
        inkscape_binpath=inkscape_binpath,
    )
