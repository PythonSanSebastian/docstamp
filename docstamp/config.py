from __future__ import annotations

import os
import re
import shutil
from pathlib import Path
from sys import platform as _platform


def find_file_match(folder_path: Path, regex: str = ".*") -> list[Path]:
    """
    Returns absolute paths of files that match the regex within folder_path and
    all its children folders.

    Note: The regex matching is done using the match function
    of the re module.

    Parameters
    ----------
    folder_path: Path
        The folder path to search in.

    regex: string

    Returns
    -------
    A list of strings.

    """
    outlist = []
    for root, _, files in folder_path.walk():
        outlist.extend([Path(root) / f for f in files if re.match(regex, f)])

    return outlist


def get_other_program_folders() -> list[Path]:
    if _platform == "linux" or _platform == "linux2":
        return [
            Path("/opt/bin"),
            Path("/usr/local/bin"),
            Path("/usr/bin"),
            Path("/bin"),
            Path("/usr/sbin"),
            Path("/sbin"),
        ]
    elif _platform == "darwin":
        return [Path("/Applications"), Path(os.environ["HOME"]) / "Applications"]
    elif _platform == "win32":
        # don't know if this works
        return Path(r"C:\Program Files")


def get_temp_dir():
    if _platform == "linux" or _platform == "linux2":
        return "/tmp"
    elif _platform == "darwin":
        return "."
    elif _platform == "win32":
        # don't know if this works
        return None


def find_in_other_programs_folders(app_name: str) -> Path | None:
    app_name_regex = "^" + app_name + "$"
    other_folders = get_other_program_folders()

    for folder in other_folders:
        abin_file = find_program(folder, app_name_regex)
        if abin_file is not None:
            return abin_file

    return None


def find_program(root_dir: Path, exec_name: str) -> Path | None:
    """Find the executable file in the given directory and its subdirectories."""
    file_matches = find_file_match(root_dir, exec_name)
    for f in file_matches:
        if is_executable(f):
            return f
    return None


def is_executable(filepath: str | Path) -> bool:
    """Check if the given file is executable."""
    filepath = Path(filepath)
    if not filepath.exists():
        return False
    if _platform == "win32":
        return filepath.suffix.lower() in (".exe", ".bat", ".cmd")
    else:
        return filepath.is_file() and os.access(filepath, os.X_OK)


def ask_for_path_of(app_name: str) -> Path | None:
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

        if not Path(bin_path).exists():
            print(f"Could not find file {bin_path}. Try it again.")
            bin_path = None
            continue

        if not is_executable(bin_path):
            print(f"No execution permissions on file {bin_path}. Try again.")
            bin_path = None
            continue

        return Path(bin_path) if bin_path else None


def proactive_search_of(app_name: str) -> Path | None:
    """Proactively search for the binary of the given application.
    This function checks the system PATH, common program folders, and prompts
    the user for the path if the binary is not found.
    Parameters
    ----------
    app_name: str
        The name of the application to search for.
    Returns
    -------
    Path | None
        The path to the binary if found, otherwise None.
    """
    if _platform == "win32":
        bin_name = app_name + ".exe"
    else:
        bin_name = app_name

    which_result = shutil.which(cmd=app_name)
    if which_result is not None and is_executable(filepath=which_result):
        return Path(which_result)

    search_result = find_in_other_programs_folders(app_name=bin_name)
    if search_result is not None:
        return search_result

    return ask_for_path_of(bin_name)


def get_inkscape_binpath() -> Path | None:
    """Return the Inkscape binary path."""
    bin_name = "inkscape"
    if _platform == "darwin":
        bin_name = "inkscape-bin"

    if "INKSCAPE_BINPATH" not in globals():
        global INKSCAPE_BINPATH
        INKSCAPE_BINPATH = proactive_search_of(bin_name)

    return INKSCAPE_BINPATH


def get_lyx_binpath() -> Path | None:
    """Return the LyX binary path."""
    if "LYX_BINPATH" not in globals():
        global LYX_BINPATH
        LYX_BINPATH = proactive_search_of("lyx")
    return LYX_BINPATH
