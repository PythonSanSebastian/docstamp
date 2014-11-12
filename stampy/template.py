# -*- coding: utf-8 -*-

import shutil
import logging
import tempfile

from .config import JINJA_ENV
from .inkscape import svg2pdf, svg2png

log = logging.getLogger(__name__)


class Document(object):

    TEMPLATE_FILE = 'badge_template.svg'

    def __init__(self, template_file_path=None):
        if template_file_path is None:
            template_file_path = self.TEMPLATE_FILE

        self.template = JINJA_ENV.get_template(template_file_path)
        self.file_content_ = None

    def fill(self):
        raise NotImplementedError

    def save_as_svg(self, file_path):
        """
        :param file_path:
        :return:
        """
        if self.file_content_ is None:
            msg = 'Template content has not been updated.'
            log.exception(msg)
            raise ValueError(msg)

        try:
            with open(file_path, "w") as f:
                f.write(self.file_content_)#.encode('utf8'))
        except Exception as exc:
            log.exception('Error saving {} '
                          'file in {}'.format(str(self.__class__), file_path))
            raise

    def save_as(self, file_path, file_type, dpi=150):
        """Save document in file_path

        Parameters
        ----------
        file_path: str

        file_type: str
            Choices: 'png', 'pdf', 'svg'

        dpi: int

        Returns
        -------
        """
        temp = tempfile.NamedTemporaryFile(suffix='.svg')
        self.save_as_svg(temp.name)

        try:
            if file_type == 'svg':
                shutil.copyfile(temp.name, file_path)
            if file_type == 'png':
                svg2png(temp.name, file_path, dpi=dpi)
            elif file_type == 'pdf':
                svg2pdf(temp.name, file_path, dpi=dpi)
        except Exception as exc:
            log.exception('Error exporting file {} to {}'.format(file_path,
                                                                 file_type))
            raise


class GenericDocument(Document):

    def __init__(self, jinja_env, template_file_path, doc_contents):
        self.template = jinja_env.get_template(template_file_path)
        self.file_content_ = self.fill(doc_contents)

    def fill(self, doc_contents):
        try:
            filled = self.template.render(**doc_contents)
            return filled
        except Exception as exc:
            log.exception('Error rendering Document '
                          'for {}.'.format(doc_contents))
            raise




