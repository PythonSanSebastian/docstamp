"""A module to hold custom exceptions for the docstamp package."""


class RenderingError(Exception):
    """Exception raised when there is an error rendering a document template."""


class ExportError(Exception):
    """Exception raised when there is an error exporting a document template."""


class QRCodeError(Exception):
    """Exception raised when there is an error generating or saving a QR code."""


class FileDeletionError(Exception):
    """Exception raised when there is an error deleting a file."""
