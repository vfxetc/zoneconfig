
project = u'zoneconfig'
copyright = u'2018, Mike Boers'
author = u'Mike Boers'

version = u'1.0'
release = u'1.0.0.dev0'


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
]


source_suffix = '.rst'
master_doc = 'index'

exclude_patterns = [u'_build', 'Thumbs.db', '.DS_Store']

html_theme = 'nature'
html_static_path = ['_static']

intersphinx_mapping = {'https://docs.python.org/': None}
