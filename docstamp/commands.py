from __future__ import annotations

import logging
import shutil
import subprocess
from pathlib import Path
from subprocess import CalledProcessError

log = logging.getLogger(__name__)


def simple_call(cmd_args: list[str]) -> int:
    """Call a command with arguments and returns its return value."""
    return subprocess.call(" ".join(cmd_args), shell=True)  # noqa: S602


def check_command(cmd_name):
    """Raise a FileNotFoundError if the command is not found.
    :param cmd_name:
    """
    if shutil.which(cmd_name) is None:
        raise FileNotFoundError(f"Could not find command named {cmd_name}.")


def call_command(cmd_name: str, args_strings: list[str]) -> int:
    """Call CLI command with arguments and returns its return value.

    Parameters
    ----------
    cmd_name: str
        Command name or full path to the binary file.

    arg_strings: List[str]
        Argument strings list.

    Returns
    -------
    return_value
        Command return value.
    """
    cmd_path = Path(cmd_name)
    if not cmd_path.is_absolute():
        cmd_fullpath = shutil.which(cmd_name)
    else:
        cmd_fullpath = cmd_name

    try:
        cmd_line = [cmd_fullpath, *args_strings]
        shell_command = " ".join(cmd_line)
        log.debug("Calling: `%s`.", shell_command)
        retval = subprocess.call(shell_command, shell=True)  # noqa: S602
    except CalledProcessError as error:
        log.exception(
            "Error calling command with arguments: " "%s \n With return code: %s",
            cmd_line,
            error.returncode,
        )
        raise
    else:
        return retval
