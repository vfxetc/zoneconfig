

class BaseSource(object):

    def __init__(self, url, content):
        self.url = url
        self.content = content

    def __repr__(self):
        return '<{}.{} {!r} at 0x{:x}>'.format(__name__, self.__class__.__name__, self.url, id(self))



from .python import PythonSource

def make_source(url, content):
    return PythonSource(url, content)

