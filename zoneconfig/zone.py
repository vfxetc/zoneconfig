import os
import collections
import re

from . import datastore
from . import finders
from ._compat import string_types


class Zone(collections.MutableMapping):

    def __init__(self, path=None, _parent=None, _name=None):
        
        #: The ``str`` name of this zone, or ``None`` if this is a root.
        self.name = _name

        #: Our parent zone, or ``None`` if this is a root.
        self.parent = _parent

        #: A ``dict`` mapping names to child zones.
        self.children = {}

        if isinstance(path, string_types):
            #: A ``list`` of URLs that will be searched by a :class:`Finder`
            #: for sub-zones.
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

    def zone(self, name):
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
            source = loader.load()
            self.sources.append(source)

        self.loaded = True

    def eval(self):

        if self.evaled:
            return

        self.load()
        if self.parent is not None:
            self.parent.eval()

        for source in self.sources:
            source.eval(self)

        self.evaled = True

    def view(self, tags, chain=True):

        if chain:
            raise NotImplementedError()

        if not isinstance(tags, dict):
            tags = dict(tags or ())

        for store in self.stores:
            if store.tags == tags:
                return store
        store = datastore.DataStore(tags)
        self.stores.append(store)
        return store

    # === Mapping API ===

    def get(self, name, default=None):
        try:
            return self[name]
        except KeyError:
            return default

    def __getitem__(self, name):
        self.eval()
        if isinstance(name, (tuple, list)):
            context = name[1:]
            name = name[0]
            view = self.view(context)
        else:
            view = self.view(None, chain=False)
        return view[name]

    def __setitem__(self, name, value):
        raise NotImplementedError()
    def __delitem__(self, name):
        raise NotImplementedError()
    def __iter__(self):
        raise NotImplementedError()
    def __len__(self):
        raise NotImplementedError()




