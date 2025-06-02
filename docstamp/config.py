import os
import re
from pathlib import Path
from sys import platform as _platform

from docstamp.commands import is_exe, which


def find_file_match(folder_path, regex=""):
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
        outlist.extend([os.path.join(root, f) for f in files if re.match(regex, f)])

    return outlist


def get_system_path():
    if _platform == "linux" or _platform == "linux2" or _platform == "darwin":
        return os.environ["PATH"]
    elif _platform == "win32":
        # don't know if this works
        return os.environ["PATH"]


def get_other_program_folders():
    if _platform == "linux" or _platform == "linux2":
        return ["/opt/bin"]
    elif _platform == "darwin":
        return ["/Applications", os.path.join(os.environ["HOME"], "Applications")]
    elif _platform == "win32":
        # don't know if this works
        return [r"C:\Program Files"]


def get_temp_dir():
    if _platform == "linux" or _platform == "linux2":
        return "/tmp"
    elif _platform == "darwin":
        return "."
    elif _platform == "win32":
        # don't know if this works
        return None


def find_in_other_programs_folders(app_name):
    app_name_regex = "^" + app_name + "$"
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


def ask_for_path_of(app_name: str) -> str:
    """Ask the user for the path of the application binary.
    This function will repeatedly prompt the user until a valid executable
    file is provided.
    Parameters
    ----------
    app_name: str
        The name of the application to find.
    Returns
    -------
    str
        The path to the binary file.
    Raises
    ------
    ValueError
        If the provided path does not exist or is not executable.
    """
    bin_path = None
    while bin_path is not None:
        bin_path = input(
            f"Insert path of {app_name} executable file [Press Ctrl+C to exit]: "
        )

        if not os.path.exists(bin_path):
            print(f"Could not find file {bin_path}. Try it again.")
            bin_path = None
            continue

        if not is_exe(bin_path):
            print(f"No execution permissions on file {bin_path}. Try again.")
            bin_path = None
            continue

        return bin_path


def proactive_search_of(app_name: str) -> str | None:
    """Proactively search for the binary of the given application.
    This function checks the system PATH, common program folders, and prompts
    the user for the path if the binary is not found.
    Parameters
    ----------
    app_name: str
        The name of the application to search for.
    Returns
    -------
    str | None
        The path to the binary if found, otherwise None.
    """
    if _platform == "win32":
        bin_name = app_name + ".exe"
    else:
        bin_name = app_name

    bin_path = which(app_name)
    if bin_path is not None and is_exe(bin_path):
        return bin_path

    bin_path = find_in_other_programs_folders(bin_name)
    if bin_path is not None:
        return bin_path

    return ask_for_path_of(bin_name)


def get_inkscape_binpath() -> Path | None:
    """Return the Inkscape binary path."""
    bin_name = "inkscape"
    if _platform == "darwin":
        bin_name = "inkscape-bin"

    if "INKSCAPE_BINPATH" not in globals():
        global INKSCAPE_BINPATH
        INKSCAPE_BINPATH = proactive_search_of(bin_name)

    return Path(INKSCAPE_BINPATH) if INKSCAPE_BINPATH else None


def get_lyx_binpath() -> Path | None:
    """Return the LyX binary path."""
    if "LYX_BINPATH" not in globals():
        global LYX_BINPATH
        LYX_BINPATH = proactive_search_of("lyx")
    return Path(LYX_BINPATH) if LYX_BINPATH else None
