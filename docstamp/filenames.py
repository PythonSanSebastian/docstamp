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
import os.path  as op
import tempfile
import logging
from   glob     import glob

from   .config  import get_temp_dir


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
        if not op.exists(filepath):
            err = 'File not found: ' + filepath
            log.error(err)
            raise IOError(err)

    try:
        rest, ext = op.splitext(filepath)
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
        if not op.exists(filepath):
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
    [os.remove(f) for f in glob(op.join(workdir, '*.' + extension))]
