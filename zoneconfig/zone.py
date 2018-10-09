import os
import collections
import re

from . import datastore
from . import finders
from ._compat import string_types


class Zone(collections.MutableMapping):

    def __init__(self, path=None, _name=None, _parent=None):
        
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

        self.context_processors = []

        self.found = False
        self._finders = {}
        self.loaders = []

        self.loaded = False
        self.sources = []

        self.evaled = False
        self.stores = {}

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
                subz = Zone(_name=part, _parent=zone)
                zone.children[part] = subz
                zone = subz
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
        self.found = True

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

    def load(self):

        if self.loaded:
            return
        self.loaded = True

        self.find()
        if self.parent is not None:
            self.parent.load()

        for loader in self.loaders:
            source = loader.load()
            self.sources.append(source)


    def eval(self):

        if self.evaled:
            return
        self.evaled = True

        self.load()
        if self.parent is not None:
            self.parent.eval()

        for source in self.sources:
            source.eval(self)


    def resolve_tags(self, context):
        context = dict(context or ())
        for func in self.context_processors:
            func(context)
        tags = []
        for k, v in context.items():
            if not isinstance(k, string_types):
                continue
            if not (isinstance(k, string_types) or isinstance(k, int)):
                continue
            tags.append((k, v))
        return tuple(sorted(tags))

    def get_store(self, context=None, **kwargs):
        if context and kwargs:
            raise ValueError("Please provide only args or kwargs.")
        tags = self.resolve_tags(context or kwargs)
        try:
            return self.stores[tags]
        except KeyError:
            store = self.stores[tags] = datastore.DataStore(tags)
            return store

    def view(self, *contexts, **context):

        if context and contexts:
            raise ValueError("Please provide only args or kwargs.")

        contexts = list(contexts) or [context]
        contexts.append(())

        stores = [self.get_store(context) for context in contexts]
        return datastore.Chain(stores)

    # === Mapping API ===

    def __getitem__(self, name):
        self.eval()
        store = self.get_store()
        return store[name]

    def __setitem__(self, name, value):
        self.eval()
        store = self.get_store()
        store[name] = value

    def __delitem__(self, name):
        self.eval()
        store = self.get_store()
        del store[name]

    def __iter__(self):
        self.eval()
        store = self.get_store()
        return iter(store)

    def __len__(self):
        self.eval()
        store = self.get_store()
        return len(store)




