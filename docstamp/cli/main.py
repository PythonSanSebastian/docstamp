#!python
from __future__ import annotations

import logging
import math
import sys
from pathlib import Path

import click

from docstamp.cli.utils import (
    CONTEXT_SETTINGS,
    DirPath,
    ExistingFilePath,
    get_items_from_csv,
)
from docstamp.file_utils import get_extension
from docstamp.template import TextDocument

ACCEPTED_DOCS = "Inkscape (.svg), PDFLatex (.tex), XeLatex (.tex)"


# declare the CLI group
@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-i",
    "--input",
    type=ExistingFilePath,
    required=False,
    help="Path to the CSV file with the data elements to be used to "
    "fill the template. This file must have the same fields as "
    "the template file.",
)
@click.option(
    "-t",
    "--template",
    type=ExistingFilePath,
    required=True,
    help="Template file path. The extension of this file will be "
    "used to determine what software to use to render the "
    "documents: \n" + ACCEPTED_DOCS,
)
@click.option(
    "-f",
    "--field",
    type=str,
    multiple=True,
    help="The field or fields that will be used to name "
    "the output files. Use many of this to declare many values. "
    "Otherwise files will be numbered.",
)
@click.option(
    "-o",
    "--outdir",
    type=DirPath,
    default="stamped",
    show_default=True,
    help="Output folder path.",
)
@click.option(
    "-p", "--prefix", type=str, help="Output files prefix. Default: Template file name."
)
@click.option(
    "-d",
    "--otype",
    type=click.Choice(["pdf", "png", "svg"]),
    default="pdf",
    show_default=True,
    help="Output file type.",
)
@click.option(
    "-c",
    "--command",
    type=click.Choice(["inkscape", "pdflatex", "xelatex"]),
    default="inkscape",
    show_default=True,
    help="The rendering command to be used in case file name "
    "extension is not specific.",
)
@click.option(
    "--index",
    type=int,
    multiple=True,
    help="Index/es of the CSV file that you want to create the "
    "document from. Note that the samples numbers start from 0 "
    "and the empty ones do not count.",
)
@click.option("--dpi", type=int, default=150, help="Output file resolution")
@click.option("-v", "--verbose", is_flag=True, help="Output debug logs.")
@click.option(
    "-u",
    "--unicode_support",
    is_flag=True,
    default=False,
    help="Allows unicode characters to be correctly encoded in the PDF.",
)
def create(  # noqa: C901, PLR0912, PLR0913, PLR0915
    input,
    template,
    field,
    outdir,
    prefix,
    otype,
    command,
    index,
    dpi,
    verbose,
    unicode_support,
):
    """Use docstamp to create documents from the content of a CSV file.

    Examples: \n
    docstamp create -i badge.csv -t badge_template.svg -o badges
    docstamp create -i badge.csv -t badge_template.svg -o ./badges -d pdf
    """
    logging.basicConfig(level="INFO")
    log = logging.getLogger(__name__)

    # setup verbose mode
    if verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logging.getLogger().setLevel(log_level)

    input_file = input
    fields = field

    # init set of template contents
    log.debug("Reading CSV elements from %s.", input_file)
    items, header_fields = get_items_from_csv(input_file)
    if not header_fields:
        raise ValueError(
            f"Could not read the header from '{input_file}'. "
            "Please check the input file format."
        )

    # check if got any item
    if len(items) == 0:
        click.echo("Quiting because found 0 items.")
        sys.exit(-1)

    if not fields:
        # set the number of zeros that the file name will have
        n_zeros = int(math.floor(math.log10(len(items))) + 1)
    else:
        # check that fields has all valid fields
        for field_name in fields:
            if field_name not in header_fields:
                raise ValueError(
                    f"Field name {field_name} not found in input file header."
                )

    # filter the items if index
    if index:
        picked_items = {idx: items[idx] for idx in index}
        items = picked_items
        log.debug("Using the elements with index %s of the input file.", index)

    # make output folder
    output_directory = Path(outdir)
    output_directory.mkdir(parents=True, exist_ok=True)

    # create template document model
    log.debug("Creating the template object using the file %s.", template)
    template_doc = TextDocument.from_template_file(template, command)
    log.debug("Created an object of type %s.", type(template_doc))

    # let's stamp them!
    for idx in items:
        item = items[idx]

        if not fields:
            file_suffix = str(idx).zfill(n_zeros)
        else:
            field_values = []
            try:
                for field_name in fields:
                    field_values.append(item[field_name].replace(" ", ""))
            except KeyError as _:
                log.exception("Could not get field %s value from %s.", field_name, item)
                sys.exit(-1)
            else:
                file_suffix = "_".join(field_values)

        log.debug("Filling template %s with values of item %s.", file_suffix, idx)
        try:
            template_doc.render(item)
        except Exception as error:
            log.exception("Error filling document for %sth item: %s.", idx, error)
            continue

        # set output file path
        if prefix is None:
            file_extension = get_extension(template)
            basename = Path(template).name.replace(file_extension, "")
        else:
            basename = prefix

        file_path = output_directory / f"{basename}_{file_suffix}.{otype}"
        log.debug("Rendering file %s.", file_path)
        try:
            template_doc.export(
                file_path=file_path,
                file_type=otype,
                dpi=dpi,
                support_unicode=unicode_support,
            )
        except Exception as error:
            log.exception("Error creating %s for %s: %s.", file_path, item, error)
            sys.exit(-1)
        else:
            log.debug("Successfully rendered %s.", file_path)
