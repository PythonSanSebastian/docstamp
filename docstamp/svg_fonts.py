# coding=utf-8
# -------------------------------------------------------------------------------
# Author: Alexandre Manhaes Savio <alexsavio@gmail.com>
# Asociación Python San Sebastián (ACPySS)
#
# 2017, Alexandre Manhaes Savio
# Use this at your own risk!
# -------------------------------------------------------------------------------


import os
import base64
from lxml import etree

from .file_utils import get_extension

FONT_TYPES = {'ttf': 'truetype',
              'otf': 'opentype'}


def get_base64_encoding(bin_filepath):
    """Return the base64 encoding of the given binary file"""
    return base64.b64encode(open(bin_filepath, 'r').read())


def remove_ext(filepath):
    """Return the basename of filepath without extension."""
    return os.path.basename(filepath).split('.')[0]


class FontFace(object):
    """CSS font-face object"""

    def __init__(self, filepath, fonttype=None, name=None):
        self.filepath = filepath
        self.ftype = fonttype
        self.given_name = name

    @classmethod
    def from_file(cls, filepath):
        return cls(filepath)

    @property
    def name(self):
        if self.given_name is None:
            return remove_ext(self.filepath)
        else:
            return self.given_name

    @property
    def base64(self):
        return get_base64_encoding(self.filepath)

    @property
    def fonttype(self):
        if self.ftype is None:
            return FONT_TYPES[get_extension(self.filepath)]
        else:
            return self.ftype

    @property
    def ext(self):
        return get_extension(self.filepath)

    @property
    def css_text(self):
        css_text = u"@font-face{\n"
        css_text += u"font-family: " + self.name + ";\n"
        css_text += u"src: url(data:font/" + self.ext + ";"
        css_text += u"base64," + self.base64 + ") "
        css_text += u"format('" + self.fonttype + "');\n}\n"
        return css_text


class FontFaceGroup(object):
    """Group of FontFaces"""

    def __init__(self):
        self.fontfaces = []

    @property
    def css_text(self):
        css_text = u'<style type="text/css">'
        for ff in self.fontfaces:
            css_text += ff.css_text
        css_text += u'</style>'
        return css_text

    @property
    def xml_elem(self):
        return etree.fromstring(self.css_text)

    def append(self, font_face):
        self.fontfaces.append(font_face)


def _embed_font_to_svg(filepath, font_files):
    """ Return the ElementTree of the SVG content in `filepath`
    with the font content embedded.
    """
    with open(filepath, 'r') as svgf:
        tree = etree.parse(svgf)

    if not font_files:
        return tree

    fontfaces = FontFaceGroup()
    for font_file in font_files:
        fontfaces.append(FontFace(font_file))

    for element in tree.iter():
        if element.tag.split("}")[1] == 'svg':
            break

    element.insert(0, fontfaces.xml_elem)

    return tree


def embed_font_to_svg(filepath, outfile, font_files):
    """ Write ttf and otf font content from `font_files`
    in the svg file in `filepath` and write the result in
    `outfile`.

    Parameters
    ----------
    filepath: str
        The SVG file whose content must be modified.

    outfile: str
        The file path where the result will be written.

    font_files: iterable of str
        List of paths to .ttf or .otf files.
    """
    tree = _embed_font_to_svg(filepath, font_files)
    tree.write(out_path, encoding='utf-8', pretty_print=True)
