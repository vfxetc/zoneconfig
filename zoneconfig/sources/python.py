
from . import BaseSource


class Proxy(object):

    def __init__(self, upper, lower):
        self.upper = upper
        self.lower = lower

    def resolve(self, key):
        if key.isupper():
            space = self.upper
            key = key.lower()
        else:
            space = self.lower
        return space, key

    def __getitem__(self, key):
        space, key = self.resolve(key)
        return space[key]

    def __setitem__(self, key, value):
        space, key = self.resolve(key)
        space[key] = value


class PythonSource(BaseSource):

    def eval(self, zone):

        store = zone.view(None, chain=False)
        locals_ = Proxy(store, {})
        globals_ = {'zone': zone}

        code = compile(self.content, self.url, 'exec')
        eval(code, globals_, locals_)
