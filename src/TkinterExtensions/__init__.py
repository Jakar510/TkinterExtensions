# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier.
#  Property of TrueLogic Company.
#  Copyright (c) 2020.
# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------

from .Enumerations import *
from .Events import *
from .HID_BUFFER import *
from .Widgets import *
from .__version__ import *




__name__ = 'TkinterExtensions'
__author__ = "Tyler Stegmaier"
__email__ = "tyler.stegmaier.510@gmail.com"
__copyright__ = "Copyright 2020"
__credits__ = [
        "Tkinter library authors"
        "Copyright (c) 2020 Tyler Stegmaier",
        "Copyright (c) 2018 Pete Mojeiko for [Keyboard](src/TkinterExtensions/Widgets/KeyBoard.py)",
        "Copyright (c) 2017 Ole Jakob Skjelten for [AnimatedGIF](src/TkinterExtensions/Widgets/Custom.py)",
        "Copyright (c) 2018 paolo-gurisatti for [Html Widgets](src/TkinterExtensions/Widgets/HTML.py)",
        ]
__license__ = "MIT"
__version__ = version
__maintainer__ = __author__
__maintainer_email__ = __email__

# How mature is this project? Common values are
#   3 - Alpha
#   4 - Beta
#   5 - Production/Stable
__status__ = 'Development Status :: 4 - Beta'

__url__ = r'https://github.com/Jakar510/TkinterExtensions'
# download_url=f'https://github.com/Jakar510/PyDebug/TkinterExtensions/releases/tag/{version}'
__classifiers__ = [
        __status__,

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
        ]

__short_description__ = 'Strongly typed widgets and event with multiple built in helper functions to speed up development.'
