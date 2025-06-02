from __future__ import annotations

import os
import tempfile
from glob import glob
from pathlib import Path

from docstamp.config import get_temp_dir


def get_extension(filepath, check_if_exists=False):
    """Return the extension of fpath.

    Parameters
    ----------
    fpath: string
    File name or path

    check_if_exists: bool

    Returns
    -------
    str
    The extension of the file name or path
    """
    if check_if_exists:
        if not os.path.exists(filepath):
            err = "File not found: " + filepath
            log.error(err)
            raise FileNotFoundError(err)

    try:
        rest, ext = os.path.splitext(filepath)
    except:
        raise
    else:
        return ext


def add_extension_if_needed(filepath, ext, check_if_exists=False):
    """Add the extension ext to fpath if it doesn't have it.

    Parameters
    ----------
    filepath: str
    File name or path

    ext: str
    File extension

    check_if_exists: bool

    Returns
    -------
    File name or path with extension added, if needed.
    """
    if not filepath.endswith(ext):
        filepath += ext

    if check_if_exists:
        if not os.path.exists(filepath):
            err = "File not found: " + filepath
            log.error(err)
            raise OSError(err)

    return filepath


def remove_ext(filepath):
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
    return filepath[: filepath.rindex(get_extension(filepath))]


def get_tempfile(suffix=".txt", dirpath=None):
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

    return tempfile.NamedTemporaryFile(suffix=suffix, dir=dirpath)


def cleanup(workdir, extension):
    """Remove the files in workdir that have the given extension.

    Parameters
    ----------
    workdir:
        Folder path from where to clean the files.

    extension: str
        File extension without the dot, e.g., 'txt'
    """
    [os.remove(f) for f in glob(os.path.join(workdir, "*." + extension))]


def csv_to_json(csv_filepath, json_filepath, fieldnames, ignore_first_line=True):
    """Convert a CSV file in `csv_filepath` into a JSON file in `json_filepath`.

    Parameters
    ----------
    csv_filepath: str
        Path to the input CSV file.

    json_filepath: str
        Path to the output JSON file. Will be overwritten if exists.

    fieldnames: List[str]
        Names of the fields in the CSV file.

    ignore_first_line: bool
    """
    import csv
    import json

    csvfile = open(csv_filepath)
    jsonfile = open(json_filepath, "w")

    reader = csv.DictReader(csvfile, fieldnames)
    rows = []
    if ignore_first_line:
        next(reader)

    for row in reader:
        rows.append(row)

    json.dump(rows, jsonfile)
    jsonfile.close()
    csvfile.close()


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
    content = content.replace(old=old, new=new, count=max)
    _filepath.write_text(content)


def cleanup_docstamp_output(output_dir=""):
    """Remove the 'tmp*.aux', 'tmp*.out' and 'tmp*.log' files in `output_dir`.
    :param output_dir:
    """
    suffixes = ["aux", "out", "log"]
    files = [
        f for suf in suffixes for f in glob(os.path.join(output_dir, f"tmp*.{suf}"))
    ]
    [os.remove(file) for file in files]
