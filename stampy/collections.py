# -*- coding: utf-8 -*-


import logging

log = logging.getLogger(__name__)


class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError


class ItemSet(object):

    def __iter__(self):
        return self.items.__iter__()

    def __next__(self):
        return self.items.__next__()

    def next(self):
        return self.items.next()

    def __getitem__(self, item):
        if hasattr(self.items, '__getitem__'):
            return self.items[item]
        else:
            raise log.exception('Item set has no __getitem__ implemented.')

    def __len__(self):
        return len(self.items)

    def save(self, file_path):
        import pickle
        try:
            with open(file_path, 'wb'):
                pickle.dump(self.__dict__, file_path, pickle.HIGHEST_PROTOCOL)
        except Exception as exc:
            log.exception('Error pickling itemset into {}.'.format(file_path))
            raise

    def load_from_pickle(self, file_path):
        import pickle
        try:
            with open(file_path, 'rb'):
                adict = pickle.load(file_path)
                pickle.dump(self.__dict__, file_path, pickle.HIGHEST_PROTOCOL)

            self.__dict__.update(adict)
        except Exception as exc:
            log.exception('Error loading pickle itemset '
                          'from {}.'.format(file_path))
            raise
