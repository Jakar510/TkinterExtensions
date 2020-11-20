# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------
import os

from setuptools import setup

from src.TkinterExtensions import __author__, __classifiers__, __email__, __license__, __name__, __short_description__, __url__, __version__, __maintainer_email__, __maintainer__




with open(os.path.abspath("PyPiReadme.md"), "r") as f:
    long_description = f.read()

with open(os.path.abspath("requirements.txt"), "r") as f:
    install_requires = f.readlines()

setup(name=__name__,
      version=__version__,
      packages=[__name__, f'{__name__}.Widgets', f'{__name__}.Misc', f'{__name__}.Events'],
      url=__url__,
      license=__license__,
      author=__author__,
      author_email=__email__,
      maintainer=__maintainer__,
      maintainer_email=__maintainer_email__,
      description=__short_description__,
      long_description=long_description,
      long_description_content_type="text/markdown",
      install_requires=install_requires,
      classifiers=__classifiers__,
      keywords=f'{__name__} Tkinter Extensions tk ttk tkinter',
      package_dir={ f'{__name__}': f'src/{__name__}' },
      package_data={
              f'{__name__}':         ['__init__.py', '__version__.py', 'Mixins.py', 'examples.py'],
              f'{__name__}.Events':  [f'{__name__}.Events/*.py'],
              f'{__name__}.Widgets': [f'{__name__}.Widgets/*.py'],
              f'{__name__}.Misc':    [f'{__name__}.Misc/*.py'],
              },
      )
