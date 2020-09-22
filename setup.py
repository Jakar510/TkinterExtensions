from setuptools import setup

from src.TkinterExtensions.__version__ import version




data_files = [
        'TkinterExtensions/*.py'
        ]

setup(
        name='TkinterExtensions',
        version=version,
        packages=['TkinterExtensions'],
        url='https://github.com/Jakar510/TkinterExtensions',
        download_url=f'https://github.com/Jakar510/PyDebug/TkinterExtensions/releases/tag/{version}',
        license='GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007',
        author='Tyler Stegmaier',
        author_email='tyler.stegmaier.510@gmail.com',
        description='Strongly typed widgets and event with multiple helper functions build in to speed up development.',
        install_requires=[],
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
        keywords='Tkinter Extensions tk ttk tkinter',
        package_dir={ 'TkinterExtensions': 'src/TkinterExtensions' },
        package_data={
                'PythonDebugTools': data_files,
                },
        )
