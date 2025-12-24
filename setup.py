#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
  name='rhythm',
  version='0.1',

  author='VikramGovindarajan',
  author_email='vickymailbuddy@gmail.com',
  description='Rhythm',

  project_urls={
    'Source Code': 'https://github.com/VikramGovindarajan/rhythm',
  },
  
  packages=find_packages(include=['rhythm']),
  
  python_requires='>=3.10',

  install_requires=[
    'numpy',
    'scipy',
    'ipython',
  ],

  extras_require={
    'docs': [
      'sphinx',
      'jupyter',
      'sphinx-rtd-theme',
    ],
    'test': [
      'pytest',
      'colorama',
      'PDSim',
    ],
  },
)
