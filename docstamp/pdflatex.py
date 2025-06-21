"""LaTeX to PDF conversion helpers."""

from __future__ import annotations

import logging
import os
import shutil
from pathlib import Path
from typing import Literal

from docstamp.commands import simple_call
from docstamp.file_utils import cleanup, remove_ext

log = logging.getLogger(__name__)


def _check_latex_file_inputs(
    tex_file_path: Path,
    output_file_path: Path | None = None,
    output_format: Literal["dvi", "pdf"] = "pdf",
) -> None:
    """Check the inputs for LaTeX file conversion functions."""
    if not tex_file_path.exists():
        raise FileNotFoundError(f"Could not find file {tex_file_path}.")

    if output_format not in ("pdf", "dvi"):
        raise ValueError(
            f"Invalid output format given {output_format}. Can only accept 'pdf' or 'dvi'."
        )

    if output_file_path is not None and output_file_path.exists():
        raise FileExistsError(f"Output file {output_file_path} already exists.")


def _cleanup_aux_log_files(workdir: Path) -> None:
    """Remove auxiliary and log files from the working directory."""
    log.debug("Cleaning *.aux and *.log files from folder %s.", workdir)
    cleanup(workdir=workdir, extension="aux")
    cleanup(workdir=workdir, extension="log")


def tex2pdf(
    tex_file: os.PathLike | str,
    output_file: os.PathLike | str | None = None,
    output_format: Literal["dvi", "pdf"] = "pdf",
) -> int:
    """Call PDFLatex to convert TeX files to PDF.

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
    exit_code: int
        The exit code of the PDFLatex command call.
    """
    tex_file_path = Path(tex_file)
    output_file_path = Path(output_file) if output_file else None
    _check_latex_file_inputs(
        tex_file_path=tex_file_path,
        output_file_path=output_file_path,
        output_format=output_format,
    )

    cmd_name = "pdflatex"
    if shutil.which(cmd=cmd_name) is None:
        raise FileNotFoundError(f"Could not find command named {cmd_name}.")

    args_strings = [cmd_name]
    result_dir = tex_file_path.parent
    if output_file_path is not None:
        output_dir = output_file_path.parent.absolute()
        args_strings += [f'-output-directory="{output_dir}"']
        result_dir = output_file_path.parent

    args_strings += [f'-output-format="{output_format}"']
    args_strings += [f'"{tex_file}"']

    log.debug("Calling command %s with args: %s.", cmd_name, args_strings)
    exit_code = simple_call(args_strings)

    tex_file_name = f"{remove_ext(tex_file_path.name)}.{output_format}"
    result_file = result_dir / tex_file_name
    if not result_file.exists():
        raise FileNotFoundError("Could not find PDFLatex result file.")

    if output_file_path is not None:
        shutil.move(result_file, output_file_path)

    _cleanup_aux_log_files(workdir=result_dir)
    return exit_code


def xetex2pdf(
    tex_file: os.PathLike | str,
    output_file: os.PathLike | str | None = None,
    output_format: Literal["pdf", "dvi"] = "pdf",
) -> int:
    """Call XeLatex to convert TeX files to PDF.

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
    exit_code: int
        The exit code of the XeLatex command call.
    """
    tex_file_path = Path(tex_file)
    output_file_path = Path(output_file) if output_file else None
    _check_latex_file_inputs(
        tex_file_path=tex_file_path,
        output_file_path=output_file_path,
        output_format=output_format,
    )

    cmd_name = "xelatex"
    if shutil.which(cmd=cmd_name) is None:
        raise FileNotFoundError(f"Could not find command named {cmd_name}.")

    args_strings = [cmd_name]
    result_dir = tex_file_path.parent
    if output_file_path is not None:
        output_dir = output_file_path.parent.absolute()
        args_strings += [f'-output-directory="{output_dir}"']
        result_dir = output_file_path.parent

    if output_format == "dvi":
        args_strings += ["-no-pdf"]

    args_strings += [f'"{tex_file}"']

    log.debug("Calling command %s with args: %s.", cmd_name, args_strings)
    exit_code = simple_call(args_strings)

    tex_file_name = f"{remove_ext(tex_file_path.name)}.{output_format}"
    result_file = result_dir / tex_file_name
    if not result_file.exists():
        raise FileNotFoundError("Could not find XeLatex result file.")

    if output_file_path is not None:
        shutil.move(result_file, output_file_path)

    _cleanup_aux_log_files(workdir=result_dir)
    return exit_code
