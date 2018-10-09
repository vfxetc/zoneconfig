import os
import collections
import re

from . import finders


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
        self._finders = {}
        self.loaders = []

        self.loaded = False
        self.sources = []

        self.evaled = False
        self.stores = []

    def get_zone(self, name):
        """Get a child zone.

        :param str name: A dot-delimited name of a sub-zone.
        :returns: Zone

        """
        zone = self
        for part in name.split('.'):
            try:
                zone = zone.children[part]
            except KeyError:
                zone = Zone(_parent=zone, _name=part)
        return zone

    def _get_finder(self, url):
        try:
            return self._finders[url]
        except KeyError:
            finder = finders.make_finder(url)
            self._finders[url] = finder
            return finder

    def find(self):
        """Look for data sources for this zone on it's path."""

        if self.found:
            return

        if self.name is not None:

            self.parent.find()

            for url in self.parent.path:
                finder = self._get_finder(url)
                finder.find(self.name)
                self.path.extend(finder.subpath)
                self.loaders.extend(finder.loaders)

        for url in self.path:
            finder = self._get_finder(url)
            finder.find('__init__')
            # We don't respect __init__ as a subpath.
            self.loaders.extend(finder.loaders)

        self.loaders.sort(key=lambda s: s.order)
        self.found = True

    def load(self):

        if self.loaded:
            return

        self.find()

        if self.parent is not None:
            self.parent.load()

        for loader in self.loaders:
            print 'HERE', self.name, loader
            source = loader.load()
            self.sources.append(source)

        self.loaded = True

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




