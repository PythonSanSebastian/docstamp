# coding=utf-8
# -------------------------------------------------------------------------------
# Author: Alexandre Manhaes Savio <alexsavio@gmail.com>
# Grupo de Inteligencia Computational <www.ehu.es/ccwintco>
# Universidad del Pais Vasco UPV/EHU
#
# 2015, Alexandre Manhaes Savio
# Use this at your own risk!
# -------------------------------------------------------------------------------
import json


def translate_key_values(adict, translations, default=''):
    """Modify the keys in adict to the ones in translations.
    Be careful, this will modify your input dictionary.
    The keys not present in translations will be left intact.

    Parameters
    ----------
    adict: a dictionary

    translations: iterable of 2-tuples
    Each 2-tuple must have the following format:
    (<adict existing key>, <desired key name for the existing key>)

    Returns
    -------
    Translated adict
    """
    for src_key, dst_key in translations:
        adict[dst_key] = adict.pop(src_key, default)
    return adict


def json_to_dict(json_str):
    """Convert json string into dict"""
    return json.JSONDecoder().decode(json_str)


class JSONMixin(object):
    """Simple, stateless json utilities mixin.

    Requires class to implement two methods:
      to_json(self): convert data to json-compatible datastructure (dict,
        list, strings, numbers)
      @classmethod from_json(cls, json): load data from json-compatible structure.
    """

    @classmethod
    def from_json_str(cls, json_str):
        """Convert json string representation into class instance.

        Args:
          json_str: json representation as string.

        Returns:
          New instance of the class with data loaded from json string.
        """
        dct = json_to_dict(json_str)
        return cls(**dct)

    def to_json_str(self):
        """Convert data to json string representation.

        Returns:
          json representation as string.
        """
        adict = dict(vars(self), sort_keys=True)
        adict['type'] = self.__class__.__name__
        return json.dumps(adict)

    def __repr__(self):
        return self.to_json_str()

    def __str__(self):
        return self.to_json_str()
