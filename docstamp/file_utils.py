from __future__ import annotations

import os
import tempfile
from pathlib import Path

from docstamp.config import get_temp_dir
from docstamp.exceptions import FileDeletionError


def get_extension(filepath: os.PathLike | str) -> str:
    """Return the extension of fpath.

    Parameters
    ----------
    filepath: string
        File name or path

    Returns
    -------
    str
    The extension of the file name or path
    """
    try:
        ext = "".join(Path(filepath).suffixes[-2:])
    except:
        raise
    else:
        return ext


def remove_ext(filepath: os.PathLike | str) -> str:
    """Removes the extension of the file.

    Parameters
    ----------
    filepath: str
        File path or name

    Returns
    -------
    str
        File path or name without extension
    """
    extension = get_extension(filepath)
    if not extension:
        return str(filepath)
    return str(filepath).removesuffix(extension)


def get_tempfile(
    suffix: str = ".txt",
    dirpath: os.PathLike | str | None = None,
) -> tempfile._TemporaryFileWrapper[bytes]:
    """Return a temporary file with the given suffix within dirpath.
    If dirpath is None, will look for a temporary folder in your system.

    Parameters
    ----------
    suffix: str
        Temporary file name suffix

    dirpath: str
        Folder path where create the temporary file

    Returns
    -------
    temp_filepath: str
        The path to the temporary path
    """
    if dirpath is None:
        dirpath = get_temp_dir()

    return tempfile.NamedTemporaryFile(suffix=suffix, dir=str(dirpath))


def cleanup(workdir: os.PathLike | str, extension: str):
    """Remove the files in workdir that have the given extension.

    Parameters
    ----------
    workdir:
        Folder path from where to clean the files.

    extension: str
        File extension without the dot, e.g., 'txt'
    """
    cleanup_target = Path(workdir)
    for f in cleanup_target.glob("*." + extension):
        try:
            f.unlink()
        except OSError as exc:
            raise FileDeletionError(
                f"Error trying to delete file {f} in {workdir}."
            ) from exc


def replace_file_content(filepath: os.PathLike | str, old: str, new: str, max: int = 1):
    """Modify the content of `filepath`, replacing `old` for `new`.

    Parameters
    ----------
    filepath: str
        Path to the file to be modified. It will be overwritten.

    old: str
        This is old substring to be replaced.

    new: str
        This is new substring, which would replace old substring.

    max: int
        If larger than 0, Only the first `max` occurrences are replaced.
    """
    _filepath = Path(filepath)
    content = _filepath.read_text()
    content = content.replace(old, new, max)
    _filepath.write_text(content)
