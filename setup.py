from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup(
  options = {
    'py2exe': {
      'optimize': 2,
      'bundle_files': 3,
      'compressed': 2
    }
  },
  console = [
    {
      'script': 'gta-eenzaam.py',
      'icon_resources': [(1, "icon.ico")]
    }
  ],
  zipfile = None
)