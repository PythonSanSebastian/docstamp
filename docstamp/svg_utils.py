"""
Function helpers to do stuff on svg files.
"""
from docstamp.commands import call_command
import svgutils.transform as sg


def replace_chars_for_svg_code(svg_content):
    """ Replace known special characters to SVG code.

    Parameters
    ----------
    svg_content: str

    Returns
    -------
    corrected_svg: str
        Corrected SVG content
    """
    result = svg_content
    svg_char = [('&', '&amp;'),
                ('>', '&gt;'),
                ('<', '&lt;'),
                ('"', '&quot;'),
                ]
    for c, entity in svg_char:
        result = result.replace(c, entity)

    return result


def _check_svg_file(svg_file):
    """ Try to read a SVG file if `svg_file` is a string.
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
            svg = sg.fromfile(svg_file)
        except Exception as exc:
            raise Exception('Error reading svg file {}.'.format(svg_file)) from exc
        else:
            return svg
    elif isinstance(svg_file, sg.SVGFigure):
        return svg_file
    else:
        raise ValueError('Expected `svg_file` to be `str` or `svgutils.SVG`, got {}.'.format(type(svg_file)))


def merge_svg_files(svg_file1, svg_file2, x_coord, y_coord, scale=1):
    """ Merge `svg_file2` in `svg_file1` in the given positions `x_coord`, `y_coord` and `scale`.

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
    svg1 = _check_svg_file(svg_file1)
    svg2 = _check_svg_file(svg_file2)

    svg2_root = svg2.getroot()
    svg1.append([svg2_root])

    svg2_root.moveto(x_coord, y_coord, scale=scale)

    return svg1



def rsvg_export(input_file, output_file, dpi=90, rsvg_binpath=None):
    """ Calls the `rsvg-convert` command, to convert a svg to a PDF (with unicode).

    Parameters
    ----------

    rsvg_binpath: str
        Path to `rsvg-convert` command

    input_file: str
        Path to the input file

    output_file: str
        Path to the output file

    Returns
    -------
    return_value
        Command call return value

    """
    if not os.path.exists(input_file):
        log.error('File {} not found.'.format(input_file))
        raise IOError((0, 'File not found.', input_file))

    args_strings = []
    args_strings += ["-f pdf"]
    args_strings += ["-o {} {}".format(input_file, output_file)]
    args_strings += ["--dpi-x {}".format(dpi)]
    args_strings += ["--dpi-y {}".format(dpi)]

    return call_command(rsvg_binpath, args_strings)
