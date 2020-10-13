# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------
import os

from setuptools import setup


def GetVesion():
      from src.TkinterExtensions.__version__ import version
      return version


with open(os.path.abspath("PyPiReadme.md"), "r") as f:
    long_description = f.read()

package = 'TkinterExtensions'
data_files = [
        f'{package}/*.py'
        ]

setup(name=package,
      version=GetVesion(),
      packages=[package],
      url=f'https://github.com/Jakar510/{package}',
      # download_url=f'https://github.com/Jakar510/PyDebug/TkinterExtensions/releases/tag/{version}',
      license='MIT',
      author='Tyler Stegmaier',
      author_email='tyler.stegmaier.510@gmail.com',
      description='Strongly typed widgets and event with multiple built in helper functions to speed up development.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      install_requires=[
              'pillow', 'tk_html_widgets',
              ],
      classifiers=[
              # How mature is this project? Common values are
              #   3 - Alpha
              #   4 - Beta
              #   5 - Production/Stable
              'Development Status :: 4 - Beta',

              # Indicate who your project is intended for
              'Intended Audience :: Developers',
              'Topic :: Software Development :: Build Tools',

              # Pick your license as you wish
              'License :: Free To Use But Restricted',

              # Support platforms
              'Operating System :: MacOS',
              'Operating System :: Microsoft :: Windows',
              'Operating System :: POSIX',

              'Programming Language :: Python :: 3',
              ],
      keywords=f'{package} Tkinter Extensions tk ttk tkinter',
      package_dir={ package: f'src/{package}' },
      package_data={
              package: data_files,
              },
      )
