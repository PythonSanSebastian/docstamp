"""
Function helpers to create vcard formats.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class VCard3Data:
    """Data container for vCard3.0 data structure."""

    name: str
    surname: str
    displayname: str
    email: str = ""
    org: str = ""
    title: str = ""
    url: str = ""
    note: str = ""


def create_vcard3_str(data: VCard3Data) -> str:
    """Create a vCard3.0 string with the given parameters.
    Reference: http://www.evenx.com/vcard-3-0-format-specification
    """
    vcard = []
    vcard += ["BEGIN:VCARD"]
    vcard += ["VERSION:3.0"]

    if data.name and data.surname:
        name = data.name.strip()
        vcard += [f"N:{name};{data.surname};;;"]

    if not data.displayname:
        displayname = f"{name} {data.surname}"

    vcard += [f"FN:{displayname}"]

    if data.email:
        vcard += [f"EMAIL:{data.email}"]

    if data.org:
        vcard += [f"ORG:{data.org}"]

    if data.title:
        vcard += [f"TITLE:{data.title}"]

    if data.url:
        vcard += [f"URL:{data.url}"]

    if data.note:
        vcard += [f"NOTE:{data.note}"]

    vcard += ["END:VCARD"]

    return "\n".join([field.strip() for field in vcard])
