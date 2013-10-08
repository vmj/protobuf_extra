#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup
import protobuf_extra
setup(
    name='protobuf-extra',
    version=protobuf_extra.__version__,
    author='Mikko Värri',
    author_email='vmj@linuxbox.fi',
    maintainer='Mikko Värri',
    maintainer_email='vmj@linuxbox.fi',
    packages=['protobuf_extra',],
    scripts=['bin/pb'],
    url='http://pypi.python.org/pypi/protobuf-extra/',
    license='GNU GPLv3',
    description=protobuf_extra.__doc__,
    long_description=''.join([
            open('README.rst').read(),
            '\n\n',
            open('CHANGES.rst').read()
            ]),
    install_requires=['protobuf',],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
        ],
    )
