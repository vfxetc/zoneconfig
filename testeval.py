from __future__ import print_function


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
        print('__getitem__', key)
        space, key = self.resolve(key)
        return space[key]

    def __setitem__(self, key, value):
        print('__setitem__', key, value)
        space, key = self.resolve(key)
        space[key] = value


config = {}
others = {}
locals_ = Proxy(config, others)

code = compile('''

foo = 123
print(foo)

FOO = 234
print(FOO)

''', '<string>', 'exec')

eval(code, globals(), locals_)

print('config:', config)
print('others:', others)
