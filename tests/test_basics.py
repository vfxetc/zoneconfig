from . import *


class TestBasics(TestCase):

    def test_find(self):

        path = root_path('basics')
        root = Zone(path=path)

        self.assertFalse(root.found)
        root.find()
        self.assertTrue(root.found)
        self.assertEqual(root.path, [path])
        self.assertEqual(len(root.loaders), 1)
        self.assertEqual(root.loaders[0].url, os.path.join(path, '__init__.py'))

        module = root.zone('module')

        self.assertFalse(module.found)
        module.find()
        self.assertTrue(module.found)
        self.assertEqual(module.path, [])
        self.assertEqual(len(module.loaders), 1)
        self.assertEqual(module.loaders[0].url, os.path.join(path, 'module.py'))

        package = root.zone('package')

        self.assertFalse(package.found)
        package.find()
        self.assertTrue(package.found)
        self.assertEqual(package.path, [os.path.join(path, 'package')])
        self.assertEqual(len(package.loaders), 1)
        self.assertEqual(package.loaders[0].url, os.path.join(path, 'package', '__init__.py'))

        submod = package.zone('submodule')
        mod2 = root.zone('package.submodule')
        self.assertIs(submod, mod2)

        self.assertFalse(submod.found)
        submod.find()
        self.assertTrue(submod.found)
        self.assertEqual(len(submod.loaders), 1)
        self.assertEqual(submod.loaders[0].url, os.path.join(path, 'package', 'submodule.py'))

    def test_load(self):

        path = root_path('basics')
        root = Zone(path=path)

        submod = root.zone('package.submodule')
        package = root.zone('package') # Out of order on purpose.
        module = root.zone('module') # Out of order on purpose.

        self.assertFalse(root.loaded)
        self.assertFalse(submod.loaded)
        
        submod.load()

        self.assertTrue(root.loaded)
        self.assertEqual(len(root.sources), 1)
        self.assertEqual(root.sources[0].url, os.path.join(path, '__init__.py'))
        self.assertIn('FOO = 1', root.sources[0].content)

        self.assertTrue(package.loaded)
        self.assertEqual(len(package.sources), 1)
        self.assertEqual(package.sources[0].url, os.path.join(path, 'package', '__init__.py'))
        self.assertIn('FOO = 3', package.sources[0].content)

        self.assertTrue(submod.loaded)
        self.assertEqual(len(submod.sources), 1)
        self.assertEqual(submod.sources[0].url, os.path.join(path, 'package', 'submodule.py'))
        self.assertIn('FOO = 4', submod.sources[0].content)

    def test_eval(self):

        path = root_path('basics')
        root = Zone(path=path)

        submod = root.zone('package.submodule')
        package = root.zone('package')

        self.assertFalse(submod.evaled)
        submod.eval()
        self.assertTrue(submod.evaled)
        self.assertEqual(len(submod.stores), 1)
        self.assertEqual(submod.stores[()].tags, ())
        self.assertEqual(submod.stores[()]['foo'], 4)

        self.assertEqual(root['foo'], 1)
        self.assertEqual(package['foo'], 3)
        self.assertEqual(submod['foo'], 4)

        self.assertEqual(root['bar'], 'root-bar')
        self.assertEqual(root['count'], 2)

        self.assertEqual(root.view({'test:basics': 'baz'})['foo'], 'baz-view-foo')


