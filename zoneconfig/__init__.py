import os

from .zone import Zone


default_root = Zone()
default_root.load_environ('ZONECONFIG')

# Expose many attributes of the root zone, to pretend that we are the root zone.
get_zone = default_root.get_zone
path = default_root.path

# Parts of Mapping API.
get = default_root.get
