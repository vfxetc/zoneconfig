from . import *


class TestBasics(TestCase):

    def test_find(self):

        path = root_path('basics')
        root = Zone(path=path)


        self.assertFalse(root.found)

        root.find()

        self.assertTrue(root.found)
        self.assertEqual(root.path, [os.path.join(path)])
        self.assertEqual(len(root.loaders), 1)
        self.assertEqual(root.loaders[0].url, os.path.join(path, '__init__.py'))

        pkg = root.get_zone('package')
        self.assertFalse(pkg.found)

        pkg.find()

        self.assertTrue(pkg.found)
        self.assertEqual(pkg.path, [os.path.join(path, 'package')])
        self.assertEqual(len(pkg.loaders), 1)
        self.assertEqual(pkg.loaders[0].url, os.path.join(path, 'package', '__init__.py'))

        mod = pkg.get_zone('submodule')
        mod.find()

        self.assertEqual(len(mod.loaders), 1)
        self.assertEqual(mod.loaders[0].url, os.path.join(path, 'package', 'submodule.py'))


