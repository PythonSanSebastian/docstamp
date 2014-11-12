# -*- coding: utf-8 -*-

import os
from pydger.certificate import Certificate
from pydger.people import ConferenceParticipant


class TestCertificate:

    def test_certificate_creation(self):
        """

        :return:
        """
        partic_json_str = '{"type": "ConferenceParticipant",' \
                          '"name": "Ludwig", "surname": "Van Beethoven",' \
                          '"affiliation": "K.K. Theater an der Burg, Vienna",' \
                          '"email": "ludwig.beethoven@gmail.com",' \
                          '"participation_type": "Speaker",' \
                          '"hashtags": "#modern_music, #piano, #composition"}'
        part = ConferenceParticipant.from_json_str(partic_json_str)

        cert = Certificate(part)
        file_path = '{}.svg'.format('_'.join(part.surname.split(' ') +
                                             part.name.split(' ')))
        try:
            cert.save(file_path)
        except Exception as exc:
            return False

        assert(os.path.exists(file_path))
        #os.remove(file_path)
