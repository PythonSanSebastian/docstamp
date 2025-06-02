"""
Function helpers to treat XML content.
"""

from __future__ import annotations

import os
from xml.sax.saxutils import escape, unescape

from .file_utils import replace_file_content

xml_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
}

xml_unescape_table = {v: k for k, v in xml_escape_table.items()}


def xml_escape(text: str) -> str:
    """
    Replace not valid characters for XML such as &, < and > to
    their valid replacement strings

    Parameters
    ----------
    text: str
        The text to be escaped.

    Returns
    -------
    escaped_text: str
    """
    return escape(text, xml_escape_table)


def xml_unescape(text: str) -> str:
    """Do the inverse of `xml_escape`.

    Parameters
    ----------
    text: str
        The text to be escaped.

    Returns
    -------
    escaped_text: str
    """
    return unescape(text, xml_unescape_table)


def change_xml_encoding(
    filepath: os.PathLike | str, src_enc: str, dst_enc: str = "utf-8"
):
    """Modify the encoding entry in the XML file.

    Parameters
    ----------
    filepath: str
        Path to the file to be modified.

    src_enc: str
        Encoding that is written in the file

    dst_enc: str
        Encoding to be set in the file.
    """
    enc_attr = "encoding='{}'"
    replace_file_content(
        filepath=filepath,
        old=enc_attr.format(src_enc),
        new=enc_attr.format(dst_enc),
        max=1,
    )
