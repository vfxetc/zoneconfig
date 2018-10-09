import os
import re


class FileFinder(object):

    def __init__(self, url):
        self.url = os.path.abspath(url)
        self.subpath = []
        self.loaders = []
        self.found = False

    def find(self, name, default_order=500):

        if self.found:
            return

        pattern = re.compile(r'{}(?:(?:\.(\d+)[^\.]*)?(\.py))?$'.format(name))

        for name in os.listdir(self.url):

            m = pattern.match(name)
            if not m:
                continue
            raw_order, ext = m.groups()
            order = int(raw_order or default_order)

            path = os.path.join(self.url, name)
            isdir = os.path.isdir(path)

            if isdir and not ext:
                self.subpath.append(path)
            elif ext and not isdir:
                self.loaders.append(FileLoader(path, order))

        self.found = True


class FileLoader(object):

    def __init__(self, url, order):
        self.url = url
        self.order = order



