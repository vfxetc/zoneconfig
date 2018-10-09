import os
import collections
import re

from .source import Source


class Zone(collections.MutableMapping):

    def __init__(self, path=None, _parent=None, _name=None):
        
        self.parent = _parent
        self.name = _name

        self.children = {}

        if isinstance(path, basestring):
            self.path = path.split(os.path.pathsep)
        elif path:
            self.path = list(path)
        else:
            self.path = []

        # Register against the parent. We do this instead of them so that
        # it is harder for the user to do it.
        if self.parent is not None:
            self.parent.children[self.name] = self

        self.found = False
        self.sources = []

        self.loaded = False
        self.stores = []

    def get_zone(self, name):
        """Get a child zone.

        :param str name: A dot-delimited name of a sub-zone.
        :returns: Zone

        """
        parts = name.split('.')
        zone = self
        for part in parts:
            try:
                zone = zone.children[part]
            except KeyError:
                zone = Zone(_parent=self, _name=part)
        return zone

    def find(self):
        """Look for data sources for this zone on it's path."""

        if self.found:
            return

        if self.parent is not None:

            self.parent.find()

            name_pattern = r'{}(?:(?:\.(\d+)[^\.]*)?(\.py))?$'.format(self.name)

            for dir_ in self.parent.path:
                for name in os.listdir(dir_):

                    m = re.match(name_pattern, name)
                    if not m:
                        continue
                    path = os.path.join(dir_, name)
                    isdir = os.path.isdir(path)

                    raw_order, ext = m.groups()
                    order = int(raw_order or 500)

                    if ext:
                        # We only accept files with extensions.
                        if isdir:
                            continue
                        self.sources.append(Source(path, order))
                    else:
                        # We only accept directories without extensions.
                        if not isdir:
                            continue
                        self.path.append(path)

        for dir_ in self.path:
            for name in os.listdir(dir_):
                m = re.match(r'^__init__(?:\.(\d+)[^\.]*)?\.py$', name)
                if not m:
                    continue

                path = os.path.join(dir_, name)
                order = int(m.group(1) or 50)

                source = Source(path, order)
                self.sources.append(source)

        self.sources.sort(key=lambda s: s.order)
        self.found = True

    def load(self):

        if self.loaded:
            return

        self.find()

    # === Mapping API ===

    def get(self, name, default=None):
        try:
            return self[name]
        except KeyError:
            return default

    def __getitem__(self, name):
        self.load()
        if isinstance(name, (tuple, list)):
            context = name[1:]
            name = name[0]
        else:
            context = []
        view = self.view(context)
        return view[name]

    def __setitem__(self, name, value):
        raise NotImplementedError()
    def __delitem__(self, name):
        raise NotImplementedError()
    def __iter__(self):
        raise NotImplementedError()
    def __len__(self):
        raise NotImplementedError()




