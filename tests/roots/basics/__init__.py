
FOO = 1

zone['bar'] = 'root-bar'

COUNT = 1
zone['count'] += 1


view = zone.view({'test:basics': 'baz'})
view['foo'] = 'baz-view-foo'

