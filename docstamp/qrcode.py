"""Utility functions to create QRCodes using `qrcode`."""

from __future__ import annotations

import os

import qrcode
import qrcode.image.svg

from .exceptions import QRCodeError
from .file_utils import replace_file_content


def _create_qrcode_image(
    text: str,
    box_size: float = 10,
) -> qrcode.image.svg.SvgPathImage:
    """Create a QR code image from `text`.

    Parameters
    ----------
    text: str
        The string to be codified in the QR image.
    box_size: float
        Size of the QR code boxes.
    Returns
    -------
    qrcode.image.svg.SvgPathImage
    The QR code image object.
    Raises
    ------
    QRCodeError
    If there is an error trying to generate the QR code image.
    """
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=box_size,
            border=0,
        )
        qr.add_data(text)
        qr.make(fit=True)
        return qr.make_image(image_factory=qrcode.image.svg.SvgPathImage)
    except Exception as exc:
        raise QRCodeError(
            f"Error trying to generate QR code  from `vcard_string`: {text}"
        ) from exc


def save_into_qrcode(
    text: str,
    out_filepath: os.PathLike | str,
    color: str = "",
    box_size: float = 10,
):
    """Save `text` in a qrcode svg image file.

    Parameters
    ----------
    text: str
        The string to be codified in the QR image.

    out_filepath: str
        Path to the output file

    color: str
        A RGB color expressed in 6 hexadecimal values.

    box_size: scalar
        Size of the QR code boxes.
    """
    img = _create_qrcode_image(text=text, box_size=box_size)
    _ = _save_qrcode(qrcode=img, out_filepath=out_filepath)
    if color:
        replace_file_content(out_filepath, "fill:#000000", f"fill:#{color}")


def _save_qrcode(qrcode: qrcode.image.svg.SvgPathImage, out_filepath: str):
    """Save a `qrcode` object into `out_filepath`.
    Parameters
    ----------
    qrcode: qrcode object

    out_filepath: str
        Path to the output file.
    """
    try:
        qrcode.save(out_filepath)
    except Exception as exc:
        raise RuntimeError(
            f"Error trying to save QR code file {out_filepath}."
        ) from exc
    else:
        return qrcode
