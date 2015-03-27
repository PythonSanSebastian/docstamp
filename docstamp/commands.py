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
import sys
import shutil
import logging
import subprocess
import os.path      as op
from   subprocess   import CalledProcessError
from   functools    import partial

log = logging.getLogger(__name__)


def simple_call(cmd_args):
    return subprocess.call(' '.join(cmd_args), shell=True)


def is_exe(fpath):
    """Return True if fpath is an executable file path.

    Parameters
    ----------
    fpath: str
        File path

    Returns
    -------
    is_executable: bool
    """
    return op.isfile(fpath) and os.access(fpath, os.X_OK)


def which(program):
    """Returns the absolute path of the given CLI program name."""
    if (sys.version_info > (3, 0)):
        return which_py3(program)
    else:
        # Python 2 code in this block
        return which_py2(program)


def which_py3(program):
    return shutil.which(program)


def which_py2(program):
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def call_command(cmd_name, args_strings):
    """Call CLI command with arguments and returns its return value.

    Parameters
    ----------
    cmd_name: str
        Command name or full path to the binary file.

    arg_strings: str
        Argument strings list.

    Returns
    -------
    return_value
        Command return value.
    """
    if not op.isabs(cmd_name):
        cmd_fullpath = which(cmd_name)
    else:
        cmd_fullpath = cmd_name

    try:
        cmd_line = [cmd_fullpath] + args_strings

        log.info('Calling: {}.'.format(cmd_line))
        retval = subprocess.check_call(cmd_line)
    except CalledProcessError as ce:
        log.exception("Error calling command {} with arguments: "
                      "{} \n With return code: {}".format(cmd_name, args_strings,
                                                          ce.returncode))
        raise
    else:
        return retval
