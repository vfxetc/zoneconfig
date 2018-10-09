import os

from unittest import TestCase

from zoneconfig import Zone


def root_path(name):
    return os.path.abspath(os.path.join(__file__, '..', 'roots', name))
