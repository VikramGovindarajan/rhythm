#!/usr/bin/env python

import glob
import sys
import numpy as np

from setuptools import setup, find_packages
from Cython.Build import cythonize


kwargs = {
    'name': 'rhythm',
    'version': 0.1,
    # 'packages': find_packages(exclude=['tests*']),

    # Metadata
    'author': 'VikramGovindarajan',
    'author_email': 'vickymailbuddy@gmail.com',
    'description': 'Rhythm',
    # 'url': 'https://openmc.org',
    # 'download_url': 'https://github.com/VikramGovindarajan/opensd/releases',
    'project_urls': {
        # 'Issue Tracker': 'https://github.com/openmc-dev/openmc/issues',
        # 'Documentation': 'https://docs.openmc.org',
        'Source Code': 'https://github.com/VikramGovindarajan/rhythm',
    },

    # Dependencies
    'python_requires': '>=3.10',
    'install_requires': [
        'numpy', 'scipy', 'ipython',
    ],
    'extras_require': {
        'docs': ['sphinx', 'jupyter',
                 'sphinx-rtd-theme'],
        'test': ['pytest','Colorama',   
                 'PDSim'],
    },
    # # Cython is used to add resonance reconstruction and fast float_endf
    # 'ext_modules': cythonize('openmc/data/*.pyx'),
    # 'include_dirs': [np.get_include()]
}

setup(**kwargs)
