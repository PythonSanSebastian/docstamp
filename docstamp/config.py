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
    """Return a list of common program folders based on the platform."""
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
        return [Path(r"C:\Program Files")]
    else:
        raise NotImplementedError(
            f"Platform {_platform} is not supported for finding other program folders."
        )


def get_temp_dir() -> Path | None:
    """Return the temporary directory based on the platform."""
    if _platform == "linux" or _platform == "linux2":
        return Path("/tmp")
    elif _platform == "darwin":
        return Path.cwd()
    elif _platform == "win32":
        # don't know if this works
        return None
    else:
        raise NotImplementedError(
            f"Platform {_platform} is not supported for getting the temporary directory."
        )


def find_in_other_programs_folders(app_name: str) -> Path | None:
    """Search for the application binary in common program folders."""
    app_name_regex = f"^{app_name}$"
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
    if _platform in ("linux", "linux2", "darwin"):
        return filepath.is_file() and os.access(filepath, os.X_OK)
    elif _platform == "win32":
        return filepath.suffix.lower() in (".exe", ".bat", ".cmd")
    else:
        raise NotImplementedError(
            f"Platform {_platform} is not supported for checking executable files."
        )


def get_executable_path(app_name: str) -> Path | None:
    """Search for the binary of the given application.
    This function checks the system PATH, common program folders.
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

    raise FileNotFoundError(
        f"Could not find {app_name} binary in the system PATH or common program folders. "
        "Please provide the path manually."
    )


def get_inkscape_binpath() -> Path | None:
    """Return the Inkscape binary path."""
    bin_name = "inkscape"
    if _platform == "darwin":
        bin_name = "inkscape-bin"
    return get_executable_path(bin_name)


def get_lyx_binpath() -> Path | None:
    """Return the LyX binary path."""
    bin_name = "lyx"
    return get_executable_path(bin_name)
