"""A module for handling document templates and rendering them."""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import TYPE_CHECKING

from jinja2 import Environment, FileSystemLoader

from .exceptions import ExportError, RenderingError
from .file_utils import get_tempfile
from .inkscape import svg2pdf, svg2png
from .pdflatex import tex2pdf, xetex2pdf
from .svg_utils import replace_chars_for_svg_code

if TYPE_CHECKING:
    from typing import Any, Literal


def get_doctype_by_extension(
    extension: Literal["txt", "svg", "tex"],
) -> type[TextDocument]:
    if "txt" in extension:
        doc_type = TextDocument
    elif "svg" in extension:
        doc_type = SVGDocument
    elif "tex" in extension:
        doc_type = LateXDocument
    else:
        raise ValueError(
            f"Could not determine the document type for `extension` {extension}."
        )
    return doc_type


def get_doctype_by_command(
    command: Literal["inkscape", "pdflatex", "xelatex"] | None,
) -> type[TextDocument]:
    if not command:
        doc_type = TextDocument
    elif command == "inkscape":
        doc_type = SVGDocument
    elif command == "pdflatex":
        doc_type = PDFLateXDocument
    elif command == "xelatex":
        doc_type = XeLateXDocument
    else:
        raise ValueError(
            f"Could not determine the document type for `command` {command}."
        )

    return doc_type


class TextDocument:
    """A plain text document model.

    Parameters
    ----------
    template_file_path: str
        Document template file path.
    """

    def __init__(
        self,
        template_file_path: os.PathLike | str,
    ):
        self._template_file = Path(template_file_path)

        if not self._template_file.exists():
            raise FileNotFoundError(
                f"Could not find template file {template_file_path}."
            )

        self._template_env = Environment(
            loader=FileSystemLoader(self._template_file.parent),
            autoescape=False,  # noqa: S701
        )
        self.template = self._template_env.get_template(template_file_path.name)

    def render(self, doc_contents: dict[str, Any] | None = None) -> str:
        """Render the content of the document with the information in doc_contents.

        Parameters
        ----------
        doc_contents: dict[str, Any]
            Dictionary with content values for the template to be filled.

        Returns
        -------
        filled_doc: str
            The content of the document with the template information filled.
        """
        try:
            return self.template.render(**doc_contents)
        except Exception as error:
            raise RenderingError(
                f"Error rendering document for {doc_contents}."
            ) from error

    def export(
        self,
        file_path: os.PathLike | str,
        doc_contents: dict[str, Any],
        **kwargs: Any,
    ):
        """Export the rendered document to a file.

        Parameters
        ----------
        file_path: Path
            Path to the output file.
        doc_contents: dict[str, Any]
            Dictionary with content values for the template to be filled.
        encoding: str
            Encoding to use when writing the file. Default is 'utf-8'.
        """
        rendered_content = self.render(doc_contents=doc_contents)
        _file_path = Path(file_path)
        encoding = kwargs.get("encoding", "utf-8")
        try:
            _file_path.write_text(
                rendered_content,
                encoding=encoding,
            )
        except Exception as error:
            raise ExportError(f"Error exporting document to {file_path}.") from error

    @classmethod
    def from_template_file(cls, template_file_path: Path, command=None):
        """Factory function to create a specific document of the
        class given by the `command` or the extension of `template_file_path`.

        See get_doctype_by_command and get_doctype_by_extension.

        Parameters
        ----------
        template_file_path: str

        command: str

        Returns
        -------
        doc

        """
        # get template file extension
        ext = template_file_path.suffix.lower().removeprefix(".")

        try:
            doc_type = get_doctype_by_command(command)
        except ValueError:
            doc_type = get_doctype_by_extension(ext)
        except:
            raise
        else:
            return doc_type(template_file_path)


class SVGDocument(TextDocument):
    """A .svg template document model. See TextDocument."""

    def render(self, doc_contents: dict[str, Any]) -> str:
        """Render the content of the document with the information in doc_contents.
        This is different from the TextDocument fill function, because this will
        check for symbools in the values of `doc_content` and replace them
        to good XML codes before filling the template.

        Parameters
        ----------
        doc_contents: dict
            Set of values to set the template document.

        Returns
        -------
        filled_doc: str
            The content of the document with the template information filled.
        """
        for key, content in doc_contents.items():
            doc_contents[key] = replace_chars_for_svg_code(content)

        try:
            return super().render(doc_contents=doc_contents)
        except Exception as error:
            raise RenderingError(
                f"Error rendering SVG document for {doc_contents}."
            ) from error

    def export(
        self,
        file_path: os.PathLike | str,
        doc_contents: dict[str, Any],
        **kwargs,
    ):
        """Export the content of the .svg file in the chosen rendered format.

        Parameters
        ----------
        file_path: str
            Path to the output file.

        doc_contents: dict[str, Any]
            Dictionary with content values for the template to be filled.

        Kwargs
        ------
        encoding: str
            Encoding to use when writing the file. Default is 'utf-8'.

        file_type: str
            Choices: 'png', 'pdf', 'svg'
            Default: 'pdf'

        dpi: int
            Dots-per-inch for the png and pdf.
            Default: 150

        support_unicode: bool
            Whether to allow unicode to be encoded in the PDF.
            Default: True
        """
        temp = get_tempfile(suffix=".svg")
        rendered_content = self.render(doc_contents=doc_contents)
        _file_path = Path(file_path)
        try:
            _file_path.write_text(
                rendered_content,
                encoding=kwargs.get("encoding", "utf-8"),
            )
        except Exception as error:
            raise ExportError(
                f"Error exporting SVG document to {file_path}."
            ) from error

        file_type = kwargs.get("file_type", "pdf")
        dpi = kwargs.get("dpi", 150)
        support_unicode = kwargs.get("support_unicode", True)
        try:
            if file_type == "svg":
                shutil.copyfile(src=temp.name, dst=file_path)
            elif file_type == "png":
                svg2png(svg_file_path=temp.name, png_file_path=file_path, dpi=dpi)
            elif file_type == "pdf":
                svg2pdf(
                    svg_file_path=temp.name,
                    pdf_file_path=file_path,
                    dpi=dpi,
                    support_unicode=support_unicode,
                )
        except Exception as e:
            raise RenderingError(
                f"Error exporting file {file_path} to {file_type}."
            ) from e


class LateXDocument(TextDocument):
    """A .tex template document model. See GenericDocument."""

    _export = staticmethod(tex2pdf)

    def export(
        self, file_path: os.PathLike | str, doc_contents: dict[str, Any], **kwargs
    ):
        """Export the content of the .tex file in the PDF.

        Parameters
        ----------
        file_path: str
            Path to the output file.

        doc_contents: dict[str, Any]
            Dictionary with content values for the template to be filled.

        Kwargs
        ------
        encoding: str
            Encoding to use when writing the file. Default is 'utf-8'.
        """
        temp = get_tempfile(suffix=".tex")
        rendered_content = self.render(doc_contents=doc_contents)
        _file_path = Path(file_path)
        try:
            file_path.write_text(
                rendered_content,
                encoding=kwargs.get("encoding", "utf-8"),
            )
        except Exception as error:
            raise ExportError(
                f"Error exporting TeX document to {file_path}."
            ) from error

        try:
            self._export(temp.name, file_path, output_format="pdf")
        except Exception as error:
            raise ExportError(f"Error exporting file {file_path} to PDF.") from error


class PDFLateXDocument(LateXDocument):
    pass


class XeLateXDocument(LateXDocument):
    _export = staticmethod(xetex2pdf)
