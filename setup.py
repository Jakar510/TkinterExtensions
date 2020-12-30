# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier.
#  Property of TrueLogic Company.
#  Copyright (c) 2020.
# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
import importlib
import os

from setuptools import setup

from BaseExtensions.Setup import GetRequirements, ReadFromFile
from src.TkinterExtensions import __author__, __classifiers__, __email__, __license__, __maintainer__, __maintainer_email__, __name__, __short_description__, __url__, __version__




long_description = ReadFromFile(os.path.abspath("PyPiReadme.md"))

install_requires = GetRequirements(os.path.abspath('./requirements.txt'))

setup(name=__name__,
      version=__version__,
      packages=[__name__, f'{__name__}.Widgets', ],
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
              f'{__name__}':         ['*.py'],
              f'{__name__}.Events':  [f'{__name__}.Events/*.py'],
              },
      )
