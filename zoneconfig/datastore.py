import collections


class DataStore(dict):

    def __init__(self, tags):
        self.tags = dict(tags)
