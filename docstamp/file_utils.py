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
import tempfile
import logging
from glob import glob

from docstamp.config import get_temp_dir

log = logging.getLogger(__name__)


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
            err = 'File not found: ' + filepath
            log.error(err)
            raise IOError(err)

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
            err = 'File not found: ' + filepath
            log.error(err)
            raise IOError(err)

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
    return filepath[:filepath.rindex(get_extension(filepath))]


def get_tempfile(suffix='.txt', dirpath=None):
    """ Return a temporary file with the given suffix within dirpath.
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
    """ Remove the files in workdir that have the given extension.

    Parameters
    ----------
    workdir:
        Folder path from where to clean the files.

    extension: str
        File extension without the dot, e.g., 'txt'
    """
    [os.remove(f) for f in glob(os.path.join(workdir, '*.' + extension))]


def mkdir(dirpath):
    """Create a folder in `dirpath` if it does'nt exist."""
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)


def csv_to_json(csv_filepath, json_filepath, fieldnames, ignore_first_line=True):
    """ Convert a CSV file in `csv_filepath` into a JSON file in `json_filepath`.

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

    csvfile = open(csv_filepath, 'r')
    jsonfile = open(json_filepath, 'w')

    reader = csv.DictReader(csvfile, fieldnames)
    rows = []
    if ignore_first_line:
        next(reader)

    for row in reader:
        rows.append(row)

    json.dump(rows, jsonfile)
    jsonfile.close()
    csvfile.close()


def write_to_file(file_path, content, encoding=None):
    """ Write `content` inside the file in `file_path` with the given encoding.
    Parameters
    ----------
    file_path: str
        Path to the output file. Will be overwritten if exists.

    content: str
        The content you want in the file.

    encoding: str
        The name of the encoding.
    """
    try:
        # TODO: check if in Python2 this should be this way
        # it's possible that we have to make this function more complex
        # to check type(content) and depending on that set 'w' without enconde
        # or 'wb' with encode.
        with open(file_path, "wb") as f:
            f.write(content.encode(encoding))
    except:
        log.exception('Error writing to file in {}'.format(file_path))
        raise


def replace_file_content(filepath, old, new, max=1):
    """ Modify the content of `filepath`, replacing `old` for `new`.

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
    with open(filepath, 'r') as f:
        content = f.read()

    content = content.replace(old, new, max)
    with open(filepath, 'w') as f:
        f.write(content)


def cleanup_docstamp_output(output_dir=''):
    """ Remove the 'tmp*.aux', 'tmp*.out' and 'tmp*.log' files in `output_dir`.
    :param output_dir:
    """
    suffixes = ['aux', 'out', 'log']
    files = [f for suf in suffixes for f in glob(os.path.join(output_dir, 'tmp*.{}'.format(suf)))]
    [os.remove(file) for file in files]
