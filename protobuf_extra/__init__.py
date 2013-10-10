#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
__version__='0.1'

def DictionaryToString(d, **kwargs):
    r"""Encodes a Python dictionary to a Google Protocol Buffer ASCII
    representation.

    This method does not validate the resulting ASCII representation
    against any particular Message type.

    Keys must be strings and are used verbatim.

    Supported value types are str, unicode, bool, int, float, long,
    dict, list, and tuple.

    See examples below, and the documentation of @converter decorator,
    for how to add support for additional value types.

    :para d: A Python dict instance.
    :return: Google Protocol Buffer ASCII representation compatible string.

    Numeric data types (except complex):

    >>> print DictionaryToString({"int": 8})
    int: 8
    <BLANKLINE>
    >>> print DictionaryToString({"float": 3.2})
    float: 3.2
    <BLANKLINE>
    >>> print DictionaryToString({"long": 1L})
    long: 1
    <BLANKLINE>

    For protobuf string type, you can use both Python str and unicode:

    >>> print DictionaryToString({"str": "foo"})
    str: "foo"
    <BLANKLINE>
    >>> print DictionaryToString({"unicode": u"bar"})
    unicode: "bar"
    <BLANKLINE>

    For protobuf bytes, only Python str works (escape the non-ASCII
    bytes):

    >>> print DictionaryToString({"bytes": "A\x95B"})
    bytes: "A\225B"
    <BLANKLINE>

    Booleans:

    >>> print DictionaryToString({"bool": True})
    bool: true
    <BLANKLINE>

    Repeated fields can be represented with a list or a tuple:

    >>> print DictionaryToString({"list": [ 1, 2, 3 ]})
    list: 1
    list: 2
    list: 3
    <BLANKLINE>
    >>> print DictionaryToString({"tuple": ( True, False )})
    tuple: true
    tuple: false
    <BLANKLINE>

    Nested messages are represented as nested dictionaries:

    >>> print DictionaryToString({"dict": { "foo": "bar" }})
    dict {
        foo: "bar"
    }
    <BLANKLINE>

    Protobuf enumerations are just numbers in Python, but in code you
    can use the symbolic constants generated by the proto compiler:

    >>> from test.Person_pb2 import Person
    >>> print DictionaryToString({"enum": Person.MALE})
    enum: 2
    <BLANKLINE>

    Note that the ASCII representation still works for round-trip,
    regardless of the numeric enums:

    >>> asciiRepresentation = DictionaryToString({"gender": Person.MALE})
    >>> print asciiRepresentation
    gender: 2
    <BLANKLINE>
    >>> message = MessageFromString(Person, asciiRepresentation)
    >>> binaryRepresentation = MessageToBinary(message, partial=True)
    >>> message = MessageFromBinary(Person, binaryRepresentation)
    >>> print MessageToString(message)
    gender: MALE
    <BLANKLINE>

    Support for additional Python datatypes:

    >>> from datetime import date
    >>> @converter(date)
    ... def date_to_dict(d):
    ...     '''A function that takes a datetime.date instance, and returns
    ...        a test.Person_pb2.Date compatible Python dictionary.'''
    ...     return {"year": d.year, "month": d.month, "day": d.day}
    ...
    >>> print DictionaryToString({'birthday': date(2013, 10, 5)})
    birthday {
        day: 5
        month: 10
        year: 2013
    }
    <BLANKLINE>

    Ignore the following example.  These examples are actually test
    code, and this clears the state so that the tests do not interfere
    each other.

    >>> del fromPythonConverters[0]
    """
    import codecs
    def byte_to_oct_error(e):
        if isinstance(e, UnicodeDecodeError):
            return (u"\\%o" % ord(e.object[e.start]), e.end)
        return codecs.strict_error(e)
    codecs.register_error("byte_to_oct", byte_to_oct_error)

    converters = [
        (dict,               lambda prefix, name, value, **kwargs: u'%s%s {\n%s%s}\n' % (prefix, name, DictionaryToString(value, **kwargs), prefix)),
        (str,                lambda prefix, name, value, **kwargs: u'%s%s: "%s"\n' % (prefix, name, value.decode("utf8", "byte_to_oct"))),
        (unicode,            lambda prefix, name, value, **kwargs: u'%s%s: "%s"\n' % (prefix, name, value)),
        (bool,               lambda prefix, name, value, **kwargs: u'%s%s: %s\n' % (prefix, name, 'true' if value else 'false')),
        ((int, float, long), lambda prefix, name, value, **kwargs: u'%s%s: %s\n' % (prefix, name, value))
    ]

    if 'depth' not in kwargs: kwargs['depth'] = 0
    if 'indent' not in kwargs: kwargs['indent'] = 4

    s = u""
    prefix = u" " * kwargs['indent'] * kwargs['depth']

    kwargs['depth'] = kwargs['depth'] + 1
    for name in sorted(d.iterkeys()):
        value = d[name]
        if isinstance(value, (list, tuple)):
            values = value            
        else:
            values = [value]

        for value in values:
            for converter in converters + fromPythonConverters:
                pythonType = converter[0]
                if isinstance(value, pythonType):
                    handler = converter[1]
                    try:
                        s += handler(prefix, name, value, **kwargs)
                    except Exception as e:
                        raise ValueError(u"%s: %s: %s" % (name, type(e), e))
                    break
    kwargs['depth'] = kwargs['depth'] - 1
    return s

def MessageFromString(messageClass, asciiRepresentation):
    """Builds a Google Protocol Buffer Message from its ASCII
    representation.

    This is the inverse of
    google.protobuf.text_format.MessageToString() function.
    """
    from google.protobuf.text_format import Merge

    message = messageClass()
    Merge(asciiRepresentation, message)
    # TODO: Override message instance fields from properties
    return message

def MessageFromDictionary(messageClass, dictionary, **kwargs):
    """Builds a Google Protocol Buffer Message from a Python dictionary
    representation.

    This is a shorthand for MessageFromString(messageClass,
    DictionaryToString(dictionary, **kwargs)).  See those functions
    for documentation.

    :para messageClass: Google Protocol Buffer Message class.
    :para dictionary: Python dictionary representation of the Message instance.
    """
    asciiRepresentation = DictionaryToString(dictionary, **kwargs)
    return MessageFromString(messageClass, asciiRepresentation)

def MessageFromBinary(messageClass, binaryRepresentation):
    """Builds a Google Protocol Buffer Message from binary representation.
    
    This is exactly same as
    messageClass().ParseFromString(binaryRepresentation), and provided
    here only for completeness.

    :para messageClass: Google Procol Buffer Message class.
    :para binaryRepresentation: Binary representation of the Message instance.
    """
    message = messageClass()
    message.ParseFromString(binaryRepresentation)
    return message

def MessageToString(message):
    """Translates the message into its ASCII representation.

    If message is an instance of a Message subclass, this is the same
    function as google.protobuf.text_format.MessageToString.

    If message is a Message subclass, this function returns an ASCII
    representation template for that Message type (with default
    values).

    :para message: A Message subclass or an instance of a Message
    subclass.

    :return: A str instance representing the message in its ASCII
    representation.

    Here are a couple of examples of genering ASCII representation of
    a message instance:

    >>> from test.Person_pb2 import Person
    >>> person = Person()
    >>> print MessageToString(person)
    <BLANKLINE>

    >>> from test.Person_pb2 import Person
    >>> person = Person()
    >>> person.name = "John Doe"
    >>> person.birthday.year = 1970
    >>> person.birthday.month = 1
    >>> person.birthday.day = 1
    >>> print MessageToString(person)
    name: "John Doe"
    birthday {
      year: 1970
      month: 1
      day: 1
    }
    <BLANKLINE>

    More interesting is the ability to create a template ASCII
    representation of a Message subclass:

    >>> from test.Person_pb2 import Person
    >>> print MessageToString(Person)
    age: 0
    birthday {
        day: 0
        month: 0
        year: 0
    }
    children {
        age: 0
        birthday {
            day: 0
            month: 0
            year: 0
        }
        d: 0
        data: ""
        f: 0
        f32: 0
        f64: 0
        flag: false
        gender: 0
        i32: 0
        i64: 0
        is_married: true
        name: ""
        nationality: 0
        s32: 0
        s64: 0
        sf32: 0
        sf64: 0
        text: ""
        u32: 0
        u64: 0
    }
    d: 0
    data: ""
    f: 0
    f32: 0
    f64: 0
    flag: false
    gender: 0
    i32: 0
    i64: 0
    is_married: true
    name: ""
    nationality: 0
    s32: 0
    s64: 0
    sf32: 0
    sf64: 0
    text: ""
    u32: 0
    u64: 0
    <BLANKLINE>

    Contrast that with the output of MessageToDictionary(Person).
    Scalar types have the emptyish default value, but repeated scalars
    don't appear at all since there is no ASCII representation for an
    empty list.

    """
    from google.protobuf.message import Message
    if isinstance(message, Message):
        # TODO: Override message instance fields from properties
        from google.protobuf.text_format import MessageToString as _MessageToString
        return _MessageToString(message)
    else:
        dictionary = MessageToDictionary(message)
        # TODO: Override dictionary values from properties
        return DictionaryToString(dictionary)

def MessageToDictionary(message, **kwargs):
    """Translates the message into its Python dictionary representation.

    If message is an instance of a Message subclass, the dictionary
    contains the fields that are set in the message.

    If message is a Message subclass, the dictionary contains all the
    fields with their default values.

    :para message: Message subclass or instance.

    For the dictionary representation, it does not matter whether the
    message is complete or not (required fields can be missing).

    >>> from test.Person_pb2 import Person
    >>> person = Person()
    >>> MessageToDictionary(person)
    {}

    >>> person = Person()
    >>> person.name = "John Doe"
    >>> MessageToDictionary(person)
    {'name': 'John Doe'}

    >>> person = Person()
    >>> person.age = 18
    >>> MessageToDictionary(person)
    {'age': 18}

    Enumerators in Python are just integers when printed.

    >>> person = Person()
    >>> person.gender = Person.MALE
    >>> MessageToDictionary(person)
    {'gender': 2}

    But you can use the symbolic constants, including enum aliases, in
    code:

    >>> person = Person()
    >>> person.nationality = Person.FOREIGN
    >>> d = MessageToDictionary(person)
    >>> assert d['nationality'] == Person.ALIEN

    Repeated fields are Python lists.

    >>> person = Person()
    >>> person.emails.append('john@doe.com')
    >>> person.emails.append('john@doe.net')
    >>> MessageToDictionary(person)
    {'emails': ['john@doe.com', 'john@doe.net']}

    >>> person = Person()
    >>> child = person.children.add()
    >>> child.name = "Tiivi"
    >>> child = person.children.add()
    >>> child.name = "Taavi"
    >>> MessageToDictionary(person)
    {'children': [{'name': 'Tiivi'}, {'name': 'Taavi'}]}

    Protobuf string types are always Python unicode:

    >>> person = Person()
    >>> person.text = u"äää"
    >>> d = MessageToDictionary(person)
    >>> assert isinstance(d['text'], unicode)

    Even when the it could be str:

    >>> person = Person()
    >>> person.text = u"aaa"
    >>> d = MessageToDictionary(person)
    >>> assert isinstance(d['text'], unicode)

    Protobuf bytes type is Python byte string (str).

    >>> person = Person()
    >>> person.data = "aaa"
    >>> d = MessageToDictionary(person)
    >>> assert isinstance(d['data'], str)

    Basic datatypes:

    >>> person = Person()
    >>> person.flag = True
    >>> MessageToDictionary(person)
    {'flag': True}

    >>> person = Person()
    >>> person.d = 3.2123
    >>> MessageToDictionary(person)
    {'d': 3.2123}

    >>> person = Person()
    >>> person.f = 3.2123
    >>> MessageToDictionary(person)
    {'f': 3.2123}

    >>> person = Person()
    >>> person.i32 = 32
    >>> MessageToDictionary(person)
    {'i32': 32}

    >>> person = Person()
    >>> person.i64 = 64
    >>> MessageToDictionary(person)
    {'i64': 64}

    >>> person = Person()
    >>> person.u32 = 32
    >>> MessageToDictionary(person)
    {'u32': 32}

    >>> person = Person()
    >>> person.u64 = 64
    >>> MessageToDictionary(person)
    {'u64': 64}

    >>> person = Person()
    >>> person.s32 = -32
    >>> MessageToDictionary(person)
    {'s32': -32}

    >>> person = Person()
    >>> person.s64 = -64
    >>> MessageToDictionary(person)
    {'s64': -64}

    >>> person = Person()
    >>> person.f32 = 32
    >>> MessageToDictionary(person)
    {'f32': 32}

    >>> person = Person()
    >>> person.f64 = 64
    >>> MessageToDictionary(person)
    {'f64': 64}

    >>> person = Person()
    >>> person.sf32 = -32
    >>> MessageToDictionary(person)
    {'sf32': -32}

    >>> person = Person()
    >>> person.sf64 = -64
    >>> MessageToDictionary(person)
    {'sf64': -64}

    Support for custom types:

    >>> from datetime import date
    >>> from test.Person_pb2 import Person, Date
    >>> @converter(Date)
    ... def dict_to_date(d):
    ...     '''A function that takes a test.Person_pb2.Date compatible
    ...        Python dictionary instance, and returns a datetime.date instance.'''
    ...     return date(d["year"], d["month"], d["day"])
    ... 
    >>> person = Person()
    >>> person.birthday.year = 1970
    >>> person.birthday.month = 1
    >>> person.birthday.day = 1
    >>> MessageToDictionary(person)
    {'birthday': datetime.date(1970, 1, 1)}

    Ignore the following example.  These examples are actually test
    code, and this clears the state so that the tests do not interfere
    each other.

    >>> del toPythonConverters[0]

    The message class can be used to build a template.  (The
    sorted(person_dict.items() is there to make the output
    predictable, otherwise the keys would be in random order.)
    
    >>> person_dict = MessageToDictionary(Person)
    >>> sorted(person_dict.items())
    [('age', 0), ('birthday', {'month': 0, 'day': 0, 'year': 0}), ('children', [{'text': u'', 'u64': 0, 'i64': 0, 'sf32': 0, 'children': [], 'u32': 0, 'is_married': True, 'f64': 0, 's32': 0, 'sf64': 0, 'flag': False, 'birthday': {'month': 0, 'day': 0, 'year': 0}, 'nationality': 0, 'data': '', 'emails': [], 'd': 0, 'name': u'', 'f': 0, 'i32': 0, 'age': 0, 'f32': 0, 'gender': 0, 's64': 0}]), ('d', 0), ('data', ''), ('emails', []), ('f', 0), ('f32', 0), ('f64', 0), ('flag', False), ('gender', 0), ('i32', 0), ('i64', 0), ('is_married', True), ('name', u''), ('nationality', 0), ('s32', 0), ('s64', 0), ('sf32', 0), ('sf64', 0), ('text', u''), ('u32', 0), ('u64', 0)]

    Some notes about the above dictionary:

      * all scalar types have an emptyish default value

      * nested messages have a nested dictionary (e.g. 'birthday'
        above)

      * repeated scalar types have an empty list, but repeated nested
        message types have one element list

      * recursive nested messages do not recurse more than one level
        deep (e.g. 'children' above)

    This functionality is only meant for generating a template from a
    Protobuf Message type.

    This also supports custom Python types.  Note that converters need
    to deal with any impedance mismatch between different types:

    >>> from datetime import date
    >>> from test.Person_pb2 import Person, Date
    >>> from exceptions import ValueError
    >>> @converter(Date)
    ... def dict_to_date(d):
    ...     '''A function that takes a test.Person_pb2.Date compatible
    ...        Python dictionary instance, and returns a datetime.date instance.'''
    ...     try:
    ...         return date(d["year"], d["month"], d["day"])
    ...     except ValueError:
    ...         # Our protobuf Date is more relaxed that Python datetime.date.
    ...         # In this example, the date constructor fails because default
    ...         # Date is all zeros, and that is not alright with Python date.
    ...         # Instead of doing any recovery (like a real app would), let's
    ...         # just waste space with this overly long comment and return
    ...         # a dummy date.
    ...         return date(1,1,1)
    ... 
    >>> person_dict = MessageToDictionary(Person)
    >>> person_dict["birthday"]
    datetime.date(1, 1, 1)

    Note how default (0,0,0) protobuf Date was translated to (1,1,1) Python date.

    Ignore the following example.  These examples are actually test
    code, and this clears the state so that the tests do not interfere
    each other.

    >>> del toPythonConverters[0]
    """
    from google.protobuf.message import Message
    from google.protobuf.descriptor import Descriptor, FieldDescriptor

    if isinstance(message, Message):
        dictionary = {}
        for (field, value) in message.ListFields():
            if field.label == FieldDescriptor.LABEL_REPEATED and field.type == FieldDescriptor.TYPE_MESSAGE:
                value = [MessageToDictionary(v, **kwargs) for v in value]
            elif isinstance(value, Message):
                for converter in toPythonConverters:
                    messageType = converter[0]
                    if isinstance(value, messageType):
                        handler = converter[1]
                        value = handler(MessageToDictionary(value), **kwargs)
                        break
                else:
                    value = MessageToDictionary(value, **kwargs)
            dictionary[field.name] = value
        # TODO: Override dictionary values from properties
        return dictionary
    else:
        dictionary = {}
        if isinstance(message, Descriptor):
            fields = message.fields
        else:
            fields = message.DESCRIPTOR.fields
        for field in fields:
            recursive_guard = "__recursive_guard_%s" % field.name
            kwargs[recursive_guard] = kwargs.get(recursive_guard, [])
            if field.type == FieldDescriptor.TYPE_MESSAGE and field.message_type not in kwargs[recursive_guard]:
                kwargs[recursive_guard].append(field.message_type)
                for converter in toPythonConverters:
                    messageType = converter[0]
                    # There doesn't seem to be a way to get from field
                    # descriptor to the generated Message subclass.
                    # So, let's compare the descriptors then.
                    if field.message_type == messageType.DESCRIPTOR:
                        handler = converter[1]
                        value = handler(MessageToDictionary(messageType), **kwargs)
                        break
                else:
                    value = MessageToDictionary(field.message_type, **kwargs)
                kwargs[recursive_guard].remove(field.message_type)
                if field.label == FieldDescriptor.LABEL_REPEATED:
                    value = [value]
            else:
                value = field.default_value
            dictionary[field.name] = value
        # TODO: Override dictionary values from properties
        return dictionary

def MessageToBinary(message, partial=False):
    """Translates a Google Protocol Buffer Message into its binary
    representation.

    :para message: 
    :para partial: 

    Building the binary representation of a Message, you can
    instantiate a Message and then call this function.
    
    >>> from test.Person_pb2 import Person
    >>> person = Person()
    >>> binaryJohnDoe = MessageToBinary(person)
    Traceback (most recent call last):
      ...
    EncodeError: Message test.Person is missing required fields: name,birthday

    Oops, there seems to be required fields.  You can fix that either
    by allowing partial serialization.

    >>> binaryJohnDoe = MessageToBinary(person, partial=True)

    Or setting that field to some value.

    >>> person.name = "John Doe"
    >>> person.birthday.year = 1970
    >>> person.birthday.month = 1
    >>> person.birthday.day = 1
    >>> binaryJohnDoe = MessageToBinary(person)

    As a short hand, you can also serialize the Message class itself.

    >>> binaryDefaults = MessageToBinary(Person)
    Traceback (most recent call last):
      ...
    EncodeError: Message test.Person is missing required fields: name,birthday
    >>> binaryRepresentation = MessageToBinary(Person, partial=True)

    """
    from google.protobuf.message import Message

    binaryRepresentation = None
    if isinstance(message, Message):
        if partial:
            binaryRepresentation = message.SerializePartialToString()
        else:
            binaryRepresentation = message.SerializeToString()
    else:
        #fields = message.DESCRIPTOR.fields
        message = message()
        #for field in fields:
        #    if field is required / fields has default / ...
        #        message.__setattr__(field.name, field.default_value)
        if partial:
            binaryRepresentation = message.SerializePartialToString()
        else:
            binaryRepresentation = message.SerializeToString()
    return binaryRepresentation

toPythonConverters = []
fromPythonConverters = []

def converter(t):
    """Decorator for converters."""
    from google.protobuf.message import Message
    if issubclass(t, Message):
        converters = toPythonConverters
    else:
        converters = fromPythonConverters
    def converterDecorator(implementation):
        """Function that does the actual decoration and registration."""
        def decoratedConverter(*args, **kwargs):
            """Function that calls the converter with right arguments."""
            if len(args) == 1:
                # args[0] is dicionary, and implementation is supposed
                # to be f(dict) -> object.
                return implementation(args[0])
            else:
                # args[2] is object, and implementation is supposed to
                # be f(object) -> dict.
                d = implementation(args[2])
                # args[0] is prefix, args[1] is name
                return u"%s%s {\n%s%s}\n" % (args[0], args[1], 
                                             DictionaryToString(d, **kwargs), args[0])
        converterDescriptor = (t, decoratedConverter)
        converters.append(converterDescriptor)
        return decoratedConverter
    return converterDecorator

def main(**kwargs):
    """
    Command Line Interface (CLI)
    ============================

    $ pb --type test.Person.Person --out ascii
    $ pb --type test.Person.Person --out dict
    $ pb --type test.Person.Person --out bin --partial >person.gpb

    $ pb --type test.Person.Person --in ascii --out ascii <person.txt
    $ pb --type test.Person.Person --in ascii --out dict <person.txt
    $ pb --type test.Person.Person --in ascii --out bin <person.txt >person.gpb

    $ pb --type test.Person.Person --in bin --out ascii <person.gpb
    $ pb --type test.Person.Person --in bin --out dict <person.gpb
    $ pb --type test.Person.Person --in bin --out bin --partial <person.gpg >person.gpb

    See 'pb --help' for more details.
    """
    from argparse import ArgumentParser, RawDescriptionHelpFormatter
    from textwrap import dedent as d
    from sys import stdin, stdout, stderr
    from os import fdopen

    cli = ArgumentParser(description=d('''
                                       Translates Google Protocol Buffer Messages into different representation.

                                       The '--type' (or '-t') is the only required option, and defines which
                                       message type to deal with.  The message type must be prefixed with the
                                       basename of the file where the message type is defined.
                                       '''),
                         epilog=d('''\
                                       Options and their arguments can be written with or without equals sign
                                       between them.  I.e. all of these are the same: '-i ascii', '-i=ascii',
                                       '--in ascii', '--in=ascii'.

                                       Input is read from standard input, and output goes to standard output.

                                       If no input format is specified, then input is ignored and the message
                                       type is used to generate the output.  This is useful for generating a
                                       template, for example.

                                       The default output format is 'ascii'.

                                       For more details, see the module documentation ('pydoc ./pb').
                                  '''),
                         formatter_class=RawDescriptionHelpFormatter)
    cli.add_argument('-t', '--type', metavar='TYPE', required=True,
                     help='Message type, e.g. act_samples.PbActivity.')
    cli.add_argument('-i', '--in', metavar='FORM', default=None, choices=('ascii','bin'), dest='input_format',
                     help='Input format. One of "ascii" or "bin".')
    cli.add_argument('-o', '--out', metavar='FORM', default='ascii', choices=('ascii','bin','dict'), dest='output_format',
                     help='Output format. One of "ascii", "bin", or "dict".')
    cli.add_argument('-p', '--partial', action='store_true',
                     help='Whether to allow incomplete binary output.')

    args = cli.parse_args()

    # args.type should be either 'my.package.file_pb2.MyMessage' or 'my.package.file.MyMessage'.
    moduleName = '.'.join([v for v in kwargs.get("modulePrefix","").split('.') if v]
                          + [v for v in args.type.split('.')[0:-1] if v])
    if not moduleName.endswith("_pb2"):
        moduleName += "_pb2"
    messageName = args.type.split('.')[-1]

    try:
        module = __import__(moduleName, globals(), locals(), [messageName])
    except ImportError:
        stderr.write("Unable to find module '%s'\n" % moduleName)
        exit(-1)
    try:
        MessageClass = getattr(module, messageName)
    except AttributeError:
        stderr.write("Module does not contain Message type '%s'\n" % messageName)
        exit(-1)

    if args.input_format is None:
        message = MessageClass
    elif args.input_format == 'ascii':
        message = MessageFromString(MessageClass, stdin.read())
    elif args.input_format == 'bin':
        message = MessageFromBinary(MessageClass, stdin.read())

    if args.output_format == 'ascii':
        print MessageToString(message)
    elif args.output_format == 'dict':
        print MessageToDictionary(message, **kwargs)
    elif args.output_format == 'bin':
        # Reopen stdout (fd=1) in binary mode. Also, use write()
        # instead of print.  These together should bypass the Python's
        # helpful universal newline feature.
        stdout = fdopen(1, "wb")
        stdout.write(MessageToBinary(message, partial=args.partial))
