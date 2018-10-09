import collections


class DataStore(dict):

    def __init__(self, tags):
        self.tags = tags


class Chain(collections.MutableMapping):

    def __init__(self, stores):
        self.stores = stores

    def __getitem__(self, key):
        for store in self.stores:
            try:
                return store[key]
            except KeyError:
                pass
        raise KeyError(key)

    def __setitem__(self, key, value):
        self.stores[0][key] = value

    def __delitem__(self, key):
        found = False
        for store in self.stores:
            try:
                del store[key]
                found = True
            except KeyError:
                pass
        if not found:
            raise KeyError(key)

    def __iter__(self):
        seen = set()
        for store in self.stores:
            for key in store:
                if key in seen:
                    continue
                seen.add(key)
                yield key

    def __len__(self):
        keys = set()
        for store in self.stores:
            keys.update(store)
        return len(keys)
    

