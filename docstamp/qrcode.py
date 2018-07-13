"""
Utility functions to create QRCodes using `qrcode`.
"""
import qrcode
import qrcode.image.svg

from docstamp.file_utils import replace_file_content


def save_into_qrcode(text, out_filepath, color='', box_size=10, pixel_size=1850):
    """ Save `text` in a qrcode svg image file.

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
    try:
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,
                           box_size=box_size, border=0, )
        qr.add_data(text)
        qr.make(fit=True)
    except Exception as exc:
        raise Exception('Error trying to generate QR code '
                        ' from `vcard_string`: {}'.format(text)) from exc
    else:
        img = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage)

    _ = _qrcode_to_file(img, out_filepath)

    if color:
        replace_file_content(out_filepath, 'fill:#000000', 'fill:#{}'.format(color))


def _qrcode_to_file(qrcode, out_filepath):
    """ Save a `qrcode` object into `out_filepath`.
    Parameters
    ----------
    qrcode: qrcode object

    out_filepath: str
        Path to the output file.
    """
    try:
        qrcode.save(out_filepath)
    except Exception as exc:
        raise IOError('Error trying to save QR code file {}.'.format(out_filepath)) from exc
    else:
        return qrcode
