"""
Function helpers to create vcard formats.
"""


def create_vcard3_str(name, surname, displayname, email='', org='', title='', url='', note=''):
    """ Create a vCard3.0 string with the given parameters.
    Reference: http://www.evenx.com/vcard-3-0-format-specification
    """
    vcard = []
    vcard += ['BEGIN:VCARD']
    vcard += ['VERSION:3.0']

    if name and surname:
        name = name.strip()
        vcard += ['N:{};{};;;'.format(name, surname)]

    if not displayname:
        displayname = '{} {}'.format(name, surname)

    vcard += ['FN:{}'.format(displayname)]

    if email:
        vcard += ['EMAIL:{}'.format(email)]

    if org:
        vcard += ['ORG:{}'.format(org)]

    if title:
        vcard += ['TITLE:{}'.format(title)]

    if url:
        vcard += ['URL:{}'.format(url)]

    if note:
        vcard += ['NOTE:{}'.format(note)]

    vcard += ['END:VCARD']

    return '\n'.join([field.strip() for field in vcard])
