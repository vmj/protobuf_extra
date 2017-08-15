#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
import protobuf_extra
import unittest


def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('test', 'unittests.py')
    return test_suite

setup(
    name='protobuf-extra',
    version=protobuf_extra.__version__,
    author='Mikko Värri',
    author_email='vmj@linuxbox.fi',
    maintainer='Mikko Värri',
    maintainer_email='vmj@linuxbox.fi',
    packages=['protobuf_extra', ],
    entry_points={
        'console_scripts': [
            'pb = protobuf_extra:main'
        ]
    },
    url='http://pypi.python.org/pypi/protobuf-extra/',
    license='GNU GPLv3',
    description=protobuf_extra.__doc__,
    long_description=''.join([
            open('README.rst').read(),
            '\n\n',
            open('CHANGES.rst').read()
            ]),
    install_requires=['protobuf', ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
        ],
    keywords='protobuf dict template',
    test_suite='setup.my_test_suite'
    )
