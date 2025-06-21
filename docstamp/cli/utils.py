"""
Utilities for the CLI functions.
"""

from __future__ import annotations

import os
import re
from csv import DictReader
from typing import TYPE_CHECKING

import click
import orjson

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import Any

# different context options
CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}
UNKNOWN_OPTIONS = {"allow_extra_args": True, "ignore_unknown_options": True}

# specification of existing ParamTypes
DirPath = click.Path(file_okay=False, resolve_path=True)
ExistingDirPath = click.Path(exists=True, file_okay=False, resolve_path=True)
ExistingFilePath = click.Path(exists=True, dir_okay=False, resolve_path=True)
UnexistingFilePath = click.Path(dir_okay=False, resolve_path=True)


class RegularExpression(click.ParamType):
    """Regular expression parameter type for Click."""

    name = "regex"

    def convert(self, value: str, param: str, ctx: click.Context | None) -> re.Pattern:  # type: ignore[return]
        """Convert the value to a compiled regular expression pattern."""
        try:
            return re.compile(value, re.IGNORECASE)
        except ValueError:
            self.fail(f"Invalid regular expression: {value}.", param, ctx)


def get_items_from_csv(
    csv_filepath: os.PathLike | str,
) -> tuple[dict[int, Any], Sequence[str] | None]:
    """
    Read a CSV file and return its contents as a dictionary of enumerated items
    and a list of the header column names.
    """
    # CSV to JSON
    # one JSON object for each item
    items = {}
    with open(str(csv_filepath)) as csvfile:
        reader = DictReader(csvfile)

        for idx, row in enumerate(reader):
            item = orjson.loads(orjson.dumps(row)).decode("utf-8")
            if any(item):
                items[idx] = item

    return items, reader.fieldnames
