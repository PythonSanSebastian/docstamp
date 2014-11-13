#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import argparse

from docstamp.inkscape import svg2pdf, svg2png

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def create_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', action='store', dest='input',
                        help='Input .svg file path')
    parser.add_argument('-o', '--output', action='store', dest='output',
                        help='Output file path')
    parser.add_argument('-t', '--type', choices=['pdf', 'png'],
                        action='store', dest='file_type', default='pdf',
                        help='Output file type')
    parser.add_argument('--dpi', type=int, action='store', dest='dpi',
                        default=150, help='Output file resolution')
    return parser


if __name__ == '__main__':

    parser = create_argparser()

    try:
        args = parser.parse_args()
    except argparse.ArgumentError as exc:
        log.exception('Error parsing arguments.')
        parser.error(str(exc.message))
        exit(-1)

    input_file = args.input
    output_file = args.output
    file_type = args.file_type
    dpi = args.dpi

    if file_type == 'png':
        svg2png(input_file, output_file, dpi=dpi)
    elif file_type == 'pdf':
        svg2pdf(input_file, output_file, dpi=dpi)
