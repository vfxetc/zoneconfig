import os
import collections


class Zone(object):

    def __init__(self, _parent=None, _name=None):
        
        self.parent = _parent
        self.name = _name

        self.children = {}

        #: :param list: List of URLs to check for subzones.
        self.path = []

        # Register against the parent. We do this instead of them so that
        # it is harder for the user to do it.
        if self.parent:
            self.parent.children[self.name] = self

        self.loaded = False
        self.sources = []
        self.stores = []

    def load_environ(self, prefix):
        path = os.environ.get(prefix + '_PATH')
        if path: # This purposefully filters out empty strings too.
            self.path.extend(
                os.path.abspath(x)
                for x in path.split(os.path.pathsep)
            )

    def get_zone(self, name):
        """Get a child zone.

        :param str name: A dot-delimited name of a sub-zone.
        :returns: Zone

        """
        parts = name.split('.')
        zone = self
        for part in parts:
            try:
                zone = zone.children[path]
            except KeyError:
                zone = Zone(self, part)
        return zone

    # === Mapping API ===

    def get(self, name, default=None):
        raise NotImplementedError()




