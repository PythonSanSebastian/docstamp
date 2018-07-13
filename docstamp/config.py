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
import re
import logging
from sys import platform as _platform

from docstamp.commands import which, is_exe

LOGGING_LVL = logging.INFO
logging.basicConfig(level=LOGGING_LVL)


def find_file_match(folder_path, regex=''):
    """
    Returns absolute paths of files that match the regex within folder_path and
    all its children folders.

    Note: The regex matching is done using the match function
    of the re module.

    Parameters
    ----------
    folder_path: string

    regex: string

    Returns
    -------
    A list of strings.

    """
    outlist = []
    for root, dirs, files in os.walk(folder_path):
        outlist.extend([os.path.join(root, f) for f in files
                        if re.match(regex, f)])

    return outlist


def get_system_path():
    if _platform == "linux" or _platform == "linux2":
        return os.environ['PATH']
    elif _platform == "darwin":
        return os.environ['PATH']
    elif _platform == "win32":
        # don't know if this works
        return os.environ['PATH']


def get_other_program_folders():
    if _platform == "linux" or _platform == "linux2":
        return ['/opt/bin']
    elif _platform == "darwin":
        return ['/Applications', os.path.join(os.environ['HOME'], 'Applications')]
    elif _platform == "win32":
        # don't know if this works
        return ['C:\Program Files']


def get_temp_dir():
    if _platform == "linux" or _platform == "linux2":
        return '/tmp'
    elif _platform == "darwin":
        return '.'
    elif _platform == "win32":
        # don't know if this works
        return None


def find_in_other_programs_folders(app_name):
    app_name_regex = '^' + app_name + '$'
    other_folders = get_other_program_folders()

    for folder in other_folders:
        abin_file = find_program(folder, app_name_regex)
        if abin_file is not None:
            return abin_file

    return None


def find_program(root_dir, exec_name):
    file_matches = find_file_match(root_dir, exec_name)
    for f in file_matches:
        if is_exe(f):
            return f
    return None


def ask_for_path_of(app_name):
    bin_path = None
    while bin_path is not None:
        bin_path = input('Insert path of {} executable file [Press Ctrl+C to exit]: '.format(app_name))

        if not os.path.exists(bin_path):
            print('Could not find file {}. Try it again.'.format(bin_path))
            bin_path = None
            continue

        if not is_exe(bin_path):
            print('No execution permissions on file {}. Try again.'.format(bin_path))
            bin_path = None
            continue

        return bin_path


def proactive_search_of(app_name):
    if _platform == 'win32':
        bin_name = app_name + '.exe'
    else:
        bin_name = app_name

    bin_path = which(app_name)
    if bin_path is not None and is_exe(bin_path):
        return bin_path

    bin_path = find_in_other_programs_folders(bin_name)
    if bin_path is not None:
        return bin_path

    return ask_for_path_of(bin_name)


def get_inkscape_binpath():
    bin_name = 'inkscape'
    if _platform == "darwin":
        bin_name = 'inkscape-bin'

    if 'INKSCAPE_BINPATH' not in globals():
        global INKSCAPE_BINPATH
        INKSCAPE_BINPATH = proactive_search_of(bin_name)

    return INKSCAPE_BINPATH


def get_lyx_binpath():
    if 'LYX_BINPATH' not in globals():
        global LYX_BINPATH
        LYX_BINPATH = proactive_search_of('lyx')
    return LYX_BINPATH

# TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

# JINJA_ENV = Environment(loader=PackageLoader('docstamp', 'templates'))
# JINJA_ENV = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

# FILE_EXPORTERS = {'.svg': Inkscape,}
#                   '.tex': PdfLatex,
#                   '.lyx': LyX}
