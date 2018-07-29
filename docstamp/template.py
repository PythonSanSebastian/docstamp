# coding=utf-8
# -------------------------------------------------------------------------------
# Author: Alexandre Manhaes Savio <alexsavio@gmail.com>
# Grupo de Inteligencia Computational <www.ehu.es/ccwintco>
# Universidad del Pais Vasco UPV/EHU
#
# 2015, Alexandre Manhaes Savio
# Use this at your own risk!
# -------------------------------------------------------------------------------


import os
import shutil
import logging

from jinja2 import Environment, FileSystemLoader

from .inkscape import svg2pdf, svg2png
from .pdflatex import tex2pdf, xetex2pdf
from .file_utils import get_tempfile, write_to_file
from .svg_utils import replace_chars_for_svg_code

log = logging.getLogger(__name__)


def get_environment_for(file_path):
    """Return a Jinja2 environment for where file_path is.

    Parameters
    ----------
    file_path: str

    Returns
    -------
    jinja_env: Jinja2.Environment

    """
    work_dir = os.path.dirname(os.path.abspath(file_path))

    if not os.path.exists(work_dir):
        raise IOError('Could not find folder for dirname of file {}.'.format(file_path))

    try:
        jinja_env = Environment(loader=FileSystemLoader(work_dir))
    except:
        raise
    else:
        return jinja_env


def get_doctype_by_extension(extension):
    if 'txt' in extension:
        doc_type = TextDocument
    elif 'svg' in extension:
        doc_type = SVGDocument
    elif 'tex' in extension:
        doc_type = LateXDocument
    else:
        raise ValueError('Could not identify the `doc_type` for `extension` {}.'.format(extension))

    return doc_type


def get_doctype_by_command(command):
    if not command:
        doc_type = TextDocument
    elif command == 'inkscape':
        doc_type = SVGDocument
    elif command == 'pdflatex':
        doc_type = PDFLateXDocument
    elif command == 'xelatex':
        doc_type = XeLateXDocument
    else:
        raise ValueError('Could not identify the `doc_type` for `command` {}.'.format(command))

    return doc_type


class TextDocument(object):
    """ A plain text document model.

    Parameters
    ----------
    template_file_path: str
        Document template file path.

    doc_contents: dict
        Dictionary with content values for the template to be filled.
    """

    def __init__(self, template_file_path, doc_contents=None):
        if not os.path.exists(template_file_path):
            raise IOError('Could not find template file {}.'.format(template_file_path))

        self._setup_template_file(template_file_path)

        if doc_contents is not None:
            self.file_content_ = self.fill(doc_contents)

    def _setup_template_file(self, template_file_path):
        """ Setup self.template

        Parameters
        ----------
        template_file_path: str
            Document template file path.
        """
        try:
            template_file = template_file_path
            template_env = get_environment_for(template_file_path)
            template = template_env.get_template(os.path.basename(template_file))
        except:
            raise
        else:
            self._template_file = template_file
            self._template_env = template_env
            self.template = template

    def fill(self, doc_contents):
        """ Fill the content of the document with the information in doc_contents.

        Parameters
        ----------
        doc_contents: dict
            Set of values to set the template document.

        Returns
        -------
        filled_doc: str
            The content of the document with the template information filled.
        """
        try:
            filled_doc = self.template.render(**doc_contents)
        except:
            log.exception('Error rendering Document '
                          'for {}.'.format(doc_contents))
            raise
        else:
            self.file_content_ = filled_doc
            return filled_doc

    def save_content(self, file_path, encoding='utf-8'):
        """ Save the content of the .txt file in a text file.

        Parameters
        ----------
        file_path: str
            Path to the output file.
        """
        if self.file_content_ is None:
            msg = 'Template content has not been updated. \
                   Please fill the template before rendering it.'
            log.exception(msg)
            raise ValueError(msg)

        try:
            write_to_file(file_path, content=self.file_content_,
                          encoding=encoding)
        except Exception as exc:
            msg = 'Document of type {} got an error when \
                   writing content.'.format(self.__class__)
            log.exception(msg)
            raise Exception(msg) from exc

    def render(self, file_path, **kwargs):
        """ See self.save_content """
        return self.save_content(file_path)

    @classmethod
    def from_template_file(cls, template_file_path, command=None):
        """ Factory function to create a specific document of the
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
        ext = os.path.basename(template_file_path).split('.')[-1]

        try:
            doc_type = get_doctype_by_command(command)
        except ValueError:
            doc_type = get_doctype_by_extension(ext)
        except:
            raise
        else:
            return doc_type(template_file_path)


class SVGDocument(TextDocument):
    """ A .svg template document model. See GenericDocument. """
    _template_file = 'badge_template.svg'

    def fill(self, doc_contents):
        """ Fill the content of the document with the information in doc_contents.
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

        return super(SVGDocument, self).fill(doc_contents=doc_contents)

    def render(self, file_path, **kwargs):
        """ Save the content of the .svg file in the chosen rendered format.

        Parameters
        ----------
        file_path: str
            Path to the output file.

        Kwargs
        ------
        file_type: str
            Choices: 'png', 'pdf', 'svg'
            Default: 'pdf'

        dpi: int
            Dots-per-inch for the png and pdf.
            Default: 150

        support_unicode: bool
            Whether to allow unicode to be encoded in the PDF.
            Default: False
        """
        temp = get_tempfile(suffix='.svg')
        self.save_content(temp.name)

        file_type = kwargs.get('file_type', 'pdf')
        dpi = kwargs.get('dpi', 150)
        try:
            if file_type == 'svg':
                shutil.copyfile(temp.name, file_path)
            elif file_type == 'png':
                svg2png(temp.name, file_path, dpi=dpi)
            elif file_type == 'pdf':
                svg2pdf(temp.name, file_path, dpi=dpi, support_unicode=support_unicode)
        except:
            log.exception(
                'Error exporting file {} to {}'.format(file_path, file_type)
            )
            raise


class LateXDocument(TextDocument):
    """ A .tex template document model. See GenericDocument. """

    _render_function = staticmethod(tex2pdf)

    def render(self, file_path, **kwargs):
        """ Save the content of the .text file in the PDF.

        Parameters
        ----------
        file_path: str
            Path to the output file.
        """
        temp = get_tempfile(suffix='.tex')
        self.save_content(temp.name)

        try:
            self._render_function(temp.name, file_path, output_format='pdf')
        except:
            log.exception('Error exporting file {} to PDF.'.format(file_path))
            raise


class PDFLateXDocument(LateXDocument):
    pass


class XeLateXDocument(LateXDocument):
    _render_function = staticmethod(xetex2pdf)
