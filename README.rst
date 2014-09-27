protobuf-extra -- Extra tools to deal with Protocol Buffers
***********************************************************

protobuf-extra provides a program and a library to convert between
ASCII, Python dictionary, and binary Protocol Buffer message
representations.

| Download: http://pypi.python.org/pypi/protobuf-extra
| Source code: http://github.com/vmj/protobuf-extra

.. contents::


Basic usage
===========

Typical usage of the program looks like this::

    $ pb --type test.Person.Person --in bin --out ascii <person.gbp
    name: "John Doe"
    birthday {
        year: 1970
	month: 1
	day: 1
    }
    $ pb --type test.Person.Person --in bin --out dict <person.gpb
    {"name": "John Doe", "birthday": {"year": 1970, "month": 1, "day": 1}}


The included Python library provides the ability to make, for example,
protobuf Message instances from a Python dictionary::

    #!/usr/bin/env python
    from test.Person_pb2 import Person
    from protobuf_extra import MessageFromDictionary

    person = MessageFromDictionary(Person, {
        "name": "John Doe",
	"birthday": {"year": 1970, "month": 1, "day": 1}
    })

See 'pydoc protobuf_extra' for a lot more documentation.


Requirements
============

In addition to Python (2.6.* or 2.7.*), `protobuf
<https://pypi.python.org/pypi/protobuf/>`_ (either 2.5.0 or 2.6.0) is required.


Installation
============

Use either ``pip install protobut-extra`` or download the source
archive and use ``python setup.py install``.

The source code is available at `Python Package Index (PyPI)
<http://pypi.python.org/pypi/protobuf-extra>`_ or, if you want the
unreleased version, from `Github
<https://github.com/vmj/protobuf-extra>`_ git repository.


Authors
=======

Original author and current maintainer is Mikko Värri
(vmj@linuxbox.fi).


License
=======

protobuf-extra is Free Software, licensed under GNU General Public
License (GPL), version 3 or later.  See LICENSE.txt file for details.
