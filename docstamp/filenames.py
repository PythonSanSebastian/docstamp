# coding=utf-8
# -------------------------------------------------------------------------------
# Author: Alexandre Manhaes Savio <alexsavio@gmail.com>
# Grupo de Inteligencia Computational <www.ehu.es/ccwintco>
# Universidad del Pais Vasco UPV/EHU
#
# 2015, Alexandre Manhaes Savio
# Use this at your own risk!
# -------------------------------------------------------------------------------

import tempfile
import os.path      as op
import logging

from   .config import get_temp_dir


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


def get_tempfile(suffix='.txt'):
    """
    Parameters
    ----------

    Returns
    -------
    """
    return tempfile.NamedTemporaryFile(suffix=suffix, dir=get_temp_dir())
