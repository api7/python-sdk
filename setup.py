#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os
import sys
import re


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

with open('apisix/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name='apisix',
    version=version,
    description='Apache APISIX SDK for Python',
    platforms='Platform Independent',
    author='Ming Wen',
    packages=['apisix'],
    keywords=['apisix', 'python', 'sdk'],
    install_requires=['requests>=2.18.4'],
    classifiers=[
        'Development Status :: 1 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
