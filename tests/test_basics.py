from . import *


class TestBasics(TestCase):

    def test_find(self):

        path = root_path('basics')
        root = Zone(path=path)


        self.assertFalse(root.found)

        root.find()

        self.assertTrue(root.found)
        self.assertEqual(root.path, [os.path.join(path)])
        self.assertEqual(len(root.sources), 1)
        self.assertEqual(root.sources[0].path, os.path.join(path, '__init__.py'))

        pkg = root.get_zone('package')
        self.assertFalse(pkg.found)

        pkg.find()

        self.assertTrue(pkg.found)
        self.assertEqual(pkg.path, [os.path.join(path, 'package')])
        self.assertEqual(len(pkg.sources), 1)
        self.assertEqual(pkg.sources[0].path, os.path.join(path, 'package', '__init__.py'))

        mod = pkg.get_zone('submodule')
        mod.find()

        self.assertEqual(len(mod.sources), 1)
        self.assertEqual(mod.sources[0].path, os.path.join(path, 'package', 'submodule.py'))


