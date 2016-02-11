"""
Function helpers to manage contact lists and vcard formats.
"""
from   collections import namedtuple
from   copy        import copy


CONTACT_FIELDS = ("Name", "Surname", "Tagline", "Affiliation", "Python_experience",
                  "Email", "Phone", "Company_homepage", "Personal_homepage")

Contact = namedtuple('Contact', CONTACT_FIELDS)


# vCard helpers
def create_contact(person_info):
    """ Return a Contact from the dict `person_info`.

    Parameters
    ----------
    person_info: dict[str] -> str

    Returns
    -------
    contact: Contact
    """
    person = copy(person_info)
    person['Personal_homepage'] = person['Personal_homepage'].replace('http://', '')
    person['Company_homepage']  = person['Company_homepage'].replace('http://', '')
    if not person['Affiliation']:
        person['Affiliation'] = person['Company_homepage']

    return Contact(**person)


def create_vcard3_str(name, surname, displayname, email='', org='', url='', note=''):
    """ Create a vCard3.0 string with the given parameters.
    Reference: http://www.evenx.com/vcard-3-0-format-specification
    """
    vcard  = []
    vcard += ['BEGIN:VCARD']
    vcard += ['VERSION:3.0']

    if name and surname:
        name = name.strip()
        vcard += ['N:{};{}'.format(name, surname)]

    if not displayname:
        displayname = '{} {}'.format(name, surname)

    vcard += ['FN:{}'.format(displayname)]

    if email:
        vcard += ['EMAIL:{}'.format(email)]

    if org:
        vcard += ['ORG:{}'.format(org)]

    if url:
        vcard += ['URL:{}'.format(url.replace('http://', ''))]

    if note:
        vcard += ['NOTE:{}'.format(note)]

    vcard += ['END:VCARD']

    return '\n'.join([field.strip() for field in vcard])
