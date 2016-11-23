# -*- coding: utf-8 -*-
"""Setup file for env_utils."""
import os
from os.path import join, dirname, normpath, abspath
from setuptools import setup, find_packages

# allow setup.py to be run from any path
os.chdir(normpath(join(abspath(__file__), os.pardir)))

setup(
    name="env_utils",
    version="1.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=['python-dateutil>=2.6'],
    license=open(join(dirname(__file__), 'LICENCE.md')).read(),
    description="Utility functions to make it easier to work with os.environ",
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    url='https://github.com/yunojuno/python-env-utils',
    author="Hugo Rodger-Brown",
    author_email='hugo@yunojuno.com',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
)
