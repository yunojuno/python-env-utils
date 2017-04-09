# -*- coding: utf-8 -*-
"""Setup file for env_utils."""
import os
from os.path import join, normpath, abspath
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(normpath(join(abspath(__file__), os.pardir)))

setup(
    name="python-env-utils",
    version="0.4",
    packages=find_packages(),
    include_package_data=True,
    install_requires=['python-dateutil>=2.6'],
    license='MIT',
    description="Utility functions to make it easier to work with os.environ",
    long_description=README,
    url='https://github.com/yunojuno/python-env-utils',
    author="Hugo Rodger-Brown",
    author_email='hugo@yunojuno.com',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ],
)
