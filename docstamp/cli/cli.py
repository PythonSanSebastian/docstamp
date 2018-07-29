#!python
import click

import os
import math
import logging

from docstamp.file_utils import get_extension
from docstamp.template import TextDocument
from docstamp.config import LOGGING_LVL
from docstamp.data_source import GoogleData

from docstamp.cli.utils import (
    CONTEXT_SETTINGS,
    verbose_switch,
    get_items_from_csv,
    ExistingFilePath,
    DirPath,
    check_not_none,
)

ACCEPTED_DOCS = "Inkscape (.svg), PDFLatex (.tex), XeLatex (.tex)"


# declare the CLI group
@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i', '--input', type=ExistingFilePath, required=False,
              help='Path to the CSV file with the data elements to be used to '
                   'fill the template. This file must have the same fields as '
                   'the template file.')
@click.option('-t', '--template', type=ExistingFilePath, required=True,
              help='Template file path. The extension of this file will be '
                   'used to determine what software to use to render the '
                   'documents: \n' + ACCEPTED_DOCS)
@click.option('-f', '--field', type=str, multiple=True,
              help='The field or fields that will be used to name '
                   'the output files. Use many of this to declare many values. '
                   'Otherwise files will be numbered.')
@click.option('-o', '--outdir', type=DirPath, default='stamped',
              show_default=True, help='Output folder path.')
@click.option('-p', '--prefix', type=str,
              help='Output files prefix. Default: Template file name.')
@click.option('-d', '--otype', type=click.Choice(['pdf', 'png', 'svg']),
              default='pdf', show_default=True,
              help='Output file type.')
@click.option('-c', '--command', type=click.Choice(['inkscape', 'pdflatex', 'xelatex']),
              default='inkscape', show_default=True,
              help='The rendering command to be used in case file name '
                   'extension is not specific.')
@click.option('--index', default=[],
              help='Index/es of the CSV file that you want to create the '
                   'document from. Note that the samples numbers start from 0 '
                   'and the empty ones do not count.')
@click.option('--dpi', type=int, default=150, help='Output file resolution')
@click.option('-g', '--google', is_flag=True, 
              help='Fetch data from Google Drive')
@click.option('-v', '--verbose', is_flag=True, 
              help='Output debug logs.')
@click.option('-u', '--unicode_support', is_flag=True, default=False,
              help='Allows unicode characters to be correctly encoded in the PDF.')
def create(input, template, field, outdir, prefix, otype, command, index,
           dpi, google, verbose, unicode_support):
    """Use docstamp to create documents from the content of a CSV file or
    a Google Spreadsheet.

    Examples: \n
    docstamp create -i badge.csv -t badge_template.svg -o badges
    docstamp create -i badge.csv -t badge_template.svg -o ./badges -d pdf
    """
    logging.basicConfig(level=LOGGING_LVL)
    log = logging.getLogger(__name__)

    # setup verbose mode
    verbose_switch(verbose)

    # check from where the input comes from
    if google:
        input_file = Google_data.getCSV()
    else:
        input_file = input

    fields = field

    # init set of template contents
    log.debug('Reading CSV elements from {}.'.format(input_file))
    items, fieldnames = get_items_from_csv(input_file)

    # check if got any item
    if len(items) == 0:
        click.echo('Quiting because found 0 items.')
        exit(-1)

    if not fields:
        # set the number of zeros that the files will have
        n_zeros = int(math.floor(math.log10(len(items))) + 1)
    else:
        # check that fields has all valid fields
        for field_name in fields:
            if field_name not in fieldnames:
                raise ValueError('Field name {} not found in input file '
                                 ' header.'.format(field_name))

    # filter the items if index
    if index:
        myitems = {int(idx): items[int(idx)] for idx in index}
        items = myitems
        log.debug('Using the elements with index {} of the input '
                  'file.'.format(index))

    # make output folder
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    # create template document model
    log.debug('Creating the template object using the file {}.'.format(template))
    template_doc = TextDocument.from_template_file(template, command)
    log.debug('Created an object of type {}.'.format(type(template_doc)))

    # let's stamp them!
    for idx in items:
        item = items[idx]

        if not len(fields):
            file_name = str(idx).zfill(n_zeros)
        else:
            field_values = []
            try:
                for field_name in fields:
                    field_values.append(item[field_name].replace(' ', ''))
            except:
                log.exception('Could not get field {} value from'
                              ' {}'.format(field_name, item))
                exit(-1)
            else:
                file_name = '_'.join(field_values)

        log.debug('Filling template {} with values of item {}.'.format(file_name, idx))
        try:
            template_doc.fill(item)
        except:
            log.exception('Error filling document for {}th item'.format(idx))
            continue

        # set output file path
        file_extension = get_extension(template)
        if prefix is None:
            basename = os.path.basename(template).replace(file_extension, '')

        file_name = basename + '_' + file_name
        file_path = os.path.join(outdir, file_name + '.' + otype)

        kwargs = {'file_type': otype,
                  'dpi': dpi, 
                  'support_unicode': unicode_support}

        log.debug('Rendering file {}.'.format(file_path))
        try:
            template_doc.render(file_path, **kwargs)
        except:
            log.exception('Error creating {} for {}.'.format(file_path, item))
            exit(-1)
        else:
            log.debug('Successfully rendered {}.'.format(file_path))
