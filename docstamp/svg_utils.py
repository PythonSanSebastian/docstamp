"""Function helpers to do stuff on svg files."""

from __future__ import annotations

import os
from pathlib import Path

import svgutils
import svgutils.transform as sg

from docstamp.commands import call_command, check_command, which


def replace_chars_for_svg_code(svg_content: str) -> str:
    """Replace known special characters to SVG code.

    Parameters
    ----------
    svg_content: str

    Returns
    -------
    corrected_svg: str
        Corrected SVG content
    """
    result = svg_content
    svg_char = [
        ("&", "&amp;"),
        (">", "&gt;"),
        ("<", "&lt;"),
        ('"', "&quot;"),
    ]

    for c, entity in svg_char:
        result = result.replace(c, entity)

    return result


def _check_svg_file(svg_file: str | svgutils.SVGFigure) -> svgutils.SVGFigure:
    """Try to read a SVG file if `svg_file` is a string.
    Raise an exception in case of error or return the svg object.

    If `svg_file` is a svgutils svg object, will just return it.

    Parameters
    ----------
    svg_file: str or svgutils.transform.SVGFigure object
        If a `str`: path to a '.svg' file,
        otherwise a svgutils svg object is expected.

    Returns
    -------
    svgutils svg object

    Raises
    ------
    Exception if any error happens.
    """
    if isinstance(svg_file, str):
        try:
            return sg.fromfile(svg_file)
        except Exception as exc:
            raise ValueError(f"Error reading svg file {svg_file}.") from exc

    if isinstance(svg_file, sg.SVGFigure):
        return svg_file

    raise ValueError(
        f"Expected `svg_file` to be `str` or `svgutils.SVG`, got {type(svg_file)}."
    )


def merge_svg_files(
    svg_file1: str | svgutils.SVGFigure,
    svg_file2: str | svgutils.SVGFigure,
    x_coord: float,
    y_coord: float,
    scale: float = 1,
) -> svgutils.SVGFigure:
    """Merge `svg_file2` in `svg_file1` in the given positions `x_coord`, `y_coord` and `scale`.

    Parameters
    ----------
    svg_file1: str or svgutils svg document object
        Path to a '.svg' file.

    svg_file2: str or svgutils svg document object
        Path to a '.svg' file.

    x_coord: float
        Horizontal axis position of the `svg_file2` content.

    y_coord: float
        Vertical axis position of the `svg_file2` content.

    scale: float
        Scale to apply to `svg_file2` content.

    Returns
    -------
    `svg1` svgutils object with the content of 'svg_file2'
    """
    svg1 = _check_svg_file(svg_file=svg_file1)
    svg2 = _check_svg_file(svg_file=svg_file2)

    svg2_root = svg2.getroot()
    svg1.append([svg2_root])
    svg2_root.moveto(x_coord, y_coord, scale=scale)

    return svg1


def rsvg_export(
    input_file: os.PathLike | str,
    output_file: str | Path,
    dpi: int = 90,
    rsvg_binpath: str | None = None,
):
    """Calls the `rsvg-convert` command, to convert a svg to a PDF (with unicode).

    Parameters
    ----------

    input_file: str
        Path to the input file

    output_file: str
        Path to the output file

    dpi: int
        Dots per inch for the output file. Default is 90.

    rsvg_binpath: str
        Path to `rsvg-convert` command

    Returns
    -------
    return_value
        Command call return value
    """
    _input_file = Path(input_file)
    if not input_file.exists():
        raise FileNotFoundError(f"File {input_file} not found.")

    if rsvg_binpath is None:
        rsvg_binpath = which(cmd_name="rsvg-convert")
        check_command(cmd_name=rsvg_binpath)

    args_strings = [
        "-f pdf",
        f"-o {output_file}",
        f"--dpi-x {dpi}",
        f"--dpi-y {dpi}",
        input_file,
    ]

    return call_command(cmd_name=rsvg_binpath, args_strings=args_strings)
