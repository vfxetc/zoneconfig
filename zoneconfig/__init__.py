import os

from .zone import Zone


root = Zone(path=os.environ.get('ZONECONFIGPATH'))

# Expose many attributes of the root zone, to pretend that we are the root zone.
zone = root.zone
path = root.path

# Parts of Mapping API.
get = root.get
