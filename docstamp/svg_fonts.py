"""SVG font embedding helpers."""

from __future__ import annotations

import base64
import os
from pathlib import Path
from typing import TYPE_CHECKING

from lxml import etree

from .file_utils import get_extension

if TYPE_CHECKING:
    from typing import Literal


FONT_TYPES: dict[str, Literal["truetype", "opentype"]] = {
    "ttf": "truetype",
    "otf": "opentype",
}


def get_base64_encoding(bin_filepath: os.PathLike | str) -> bytes:
    """Return the base64 encoding of the given binary file"""
    _bin_filepath = Path(bin_filepath)
    return base64.b64encode(_bin_filepath.open(mode="rb").read())


def remove_ext(filepath: os.PathLike | str) -> str:
    """Return the basename of filepath without extension."""
    _filepath = Path(filepath)
    return _filepath.name.split(".")[0]


class FontFace:
    """CSS font-face object

    Represents a font-face object that can be used in CSS.
    It contains the font file path, font type, name, and provides
    methods to generate the CSS text for embedding the font in a web page.

    Parameters
    ----------
    filepath: str or Path
        The path to the font file (e.g., .ttf or .otf).

    fonttype: str, optional
        The type of the font (e.g., 'truetype' or 'opentype').
        If not provided, it will be inferred from the file extension.

    name: str, optional
        The name of the font. If not provided, it will be derived
        from the file name without extension.
    """

    def __init__(
        self,
        filepath: os.PathLike | str,
        fonttype: Literal["ttf", "otf"] | None = None,
        name: str | None = None,
    ):
        self.filepath = Path(filepath)
        self.ftype = fonttype
        self.given_name = name

    @classmethod
    def from_file(cls, filepath: os.PathLike | str) -> FontFace:
        """Create a FontFace instance from a file path."""
        return cls(filepath)

    @property
    def name(self) -> str:
        """Return the name of the font."""
        if self.given_name is None:
            return remove_ext(filepath=self.filepath)
        else:
            return self.given_name

    @property
    def base64(self) -> bytes:
        """Return the base64 encoding of the font file."""
        return get_base64_encoding(bin_filepath=self.filepath)

    @property
    def fonttype(self) -> Literal["truetype", "opentype"]:
        """Return the font type based on the file extension."""
        if self.ftype is None:
            file_extension = get_extension(filepath=self.filepath)
            if file_extension not in FONT_TYPES:
                raise ValueError(
                    f"Unsupported font type for file {self.filepath}. "
                    "Supported types are: " + ", ".join(FONT_TYPES.keys())
                )
            return FONT_TYPES[file_extension]
        else:
            return FONT_TYPES[self.ftype]

    @property
    def ext(self) -> str:
        """Return the file extension of the font file."""
        return get_extension(filepath=self.filepath)

    @property
    def css_text(self) -> str:
        """Return the CSS text for embedding the font."""
        css_text = "@font-face"
        css_text += "{\n"
        css_text += f"font-family: {self.name};\n"
        css_text += f"src: url(data:font/{self.ext};base64,{self.base64!r}) "
        css_text += f"format('{self.fonttype}');\n"
        css_text += "}\n"
        return css_text


class FontFaceGroup:
    """Group of FontFaces"""

    def __init__(self, fontfaces: list[FontFace] | None = None):
        self.fontfaces: list[FontFace] = fontfaces or []

    @property
    def css_text(self) -> str:
        """Return the CSS text for all font faces in the group."""
        css_text = '<style type="text/css">'
        for ff in self.fontfaces:
            css_text += ff.css_text
        css_text += "</style>"
        return css_text

    @property
    def xml_elem(self) -> etree.Element:
        """Return the XML element for the CSS text."""
        return etree.fromstring(self.css_text)

    def append(self, font_face) -> None:
        """Append a FontFace to the group."""
        self.fontfaces.append(font_face)


def _embed_font_to_svg(
    filepath: os.PathLike | str, font_files: list[os.PathLike | str] | None = None
) -> etree.ElementTree:
    """Return the ElementTree of the SVG content in `filepath`
    with the font content embedded.
    """
    _filepath = Path(filepath)
    with _filepath.open() as svgf:
        tree = etree.parse(svgf)

    if not font_files:
        return tree

    fontfaces = FontFaceGroup()
    for font_file in font_files:
        fontfaces.append(FontFace(font_file))

    for element in tree.iter():
        if element.tag.split("}")[1] == "svg":
            break

    element.insert(0, fontfaces.xml_elem)

    return tree


def embed_font_to_svg(
    filepath: os.PathLike | str,
    outfile: os.PathLike | str,
    font_files: list[os.PathLike | str] | None = None,
) -> None:
    """Write ttf and otf font content from `font_files`
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
    tree = _embed_font_to_svg(filepath=filepath, font_files=font_files)
    tree.write(outfile, encoding="utf-8", pretty_print=True)
