# -*- coding: utf-8 -*-
"""
Utilities for the CLI functions.
"""
import re
import json
import logging
from csv import DictReader

import click

from docstamp.model import json_to_dict

# different context options
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
UNKNOWN_OPTIONS = dict(allow_extra_args=True,
                       ignore_unknown_options=True)

# specification of existing ParamTypes
DirPath = click.Path(file_okay=False, resolve_path=True)
ExistingDirPath = click.Path(exists=True, file_okay=False, resolve_path=True)
ExistingFilePath = click.Path(exists=True, dir_okay=False, resolve_path=True)
UnexistingFilePath = click.Path(dir_okay=False, resolve_path=True)


# validators
def check_not_none(ctx, param, value):
    if value is None:
        raise click.BadParameter('got {}.'.format(value))
    return value


# declare custom click.ParamType
class RegularExpression(click.ParamType):
    name = 'regex'

    def convert(self, value, param, ctx):
        try:
            rex = re.compile(value, re.IGNORECASE)
        except ValueError:
            self.fail('%s is not a valid regular expression.' % value, param, ctx)
        else:
            return rex


# other utilities
def echo_list(alist):
    for i in alist:
        click.echo(i)


def get_items_from_csv(csv_filepath):
    # CSV to JSON
    # one JSON object for each item
    items = {}
    with open(str(csv_filepath), 'r') as csvfile:

        reader = DictReader(csvfile)

        for idx, row in enumerate(reader):
            item = json_to_dict(json.dumps(row))
            if any([item[i] != '' for i in item]):
                items[idx] = item

    return items, reader.fieldnames


def verbose_switch(verbose=False):
    if verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logging.getLogger().setLevel(log_level)
