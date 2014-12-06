#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import socket_server

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = socket_server.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-socket-server',
    version=version,
    description="""Django Socket Server""",
    long_description=readme + '\n\n' + history,
    author='Ashley Wilson',
    author_email='scifilem@gmail.com',
    url='https://github.com/CptLemming/django-socket-server',
    packages=[
        'socket_server',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.6.1',
        'wheel==0.23.0',
        'autobahn',
        'twisted',
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-socket-server',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
