#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Extra tools for Protobuf and Python"""
from __future__ import print_function

__version__ = '0.5.2'

try:
    str = unicode
except NameError:
    pass  # Forward compatibility with py3k (unicode is not defined)
try:
    long
except NameError:
    long = int  # Forward compatibility with py3k (long is not defined)

def DictionaryToString(d, **kwargs):
    r"""Encodes a Python dictionary to a Google Protocol Buffer ASCII
    representation.

    This method does not validate the resulting ASCII representation
    against any particular Message type.

    Keys must be strings and are used verbatim.

    Supported value types are bytes, str (unicode), bool, int, float, long,
    dict, list, and tuple.

    See unit tests, and the documentation of @converter decorator,
    for how to add support for additional value types.

    :para d: A Python dict instance.
    :return: Google Protocol Buffer ASCII representation compatible string.
    """
    import codecs, sys

    def byte_to_oct_error(e):
        if isinstance(e, UnicodeDecodeError):
            if sys.version_info[0]<3:
                return u"\\%o" % ord(e.object[e.start]), e.end
            else:
                return u"\\%o" % e.object[e.start], e.end
        return codecs.strict_error(e)
    codecs.register_error("byte_to_oct", byte_to_oct_error)

    converters = [
        (dict,               lambda prefix, name, value, **kwargs: u'%s%s {\n%s%s}\n' % (prefix, name, DictionaryToString(value, **kwargs), prefix)),
        (bytes,              lambda prefix, name, value, **kwargs: u'%s%s: "%s"\n' % (prefix, name, value.decode("utf8", "byte_to_oct"))),
        (str,                lambda prefix, name, value, **kwargs: u'%s%s: "%s"\n' % (prefix, name, value)),
        (bool,               lambda prefix, name, value, **kwargs: u'%s%s: %s\n' % (prefix, name, 'true' if value else 'false')),
        ((int, float, long), lambda prefix, name, value, **kwargs: u'%s%s: %s\n' % (prefix, name, value))
    ]

    if 'depth' not in kwargs: kwargs['depth'] = 0
    if 'indent' not in kwargs: kwargs['indent'] = 4

    s = u""
    prefix = u" " * kwargs['indent'] * kwargs['depth']

    kwargs['depth'] = kwargs['depth'] + 1
    for name in sorted(d.keys()):
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
            # TODO: When support for protobuf 2.5 is dropped, following "normalization" can be removed since 2.6.0 does
            #       it for us.
            #elif field.label != FieldDescriptor.LABEL_REPEATED:
            elif field.type == FieldDescriptor.TYPE_STRING:
                if field.label == FieldDescriptor.LABEL_REPEATED:
                    value = [str(v) for v in value]
                else:
                    value = str(value)
            elif field.type in (FieldDescriptor.TYPE_INT64, FieldDescriptor.TYPE_SINT64, FieldDescriptor.TYPE_UINT64,
                                FieldDescriptor.TYPE_FIXED64, FieldDescriptor.TYPE_SFIXED64):
                if field.label == FieldDescriptor.LABEL_REPEATED:
                    value = [long(v) for v in value]
                else:
                    value = long(value)
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
                dictionary[field.name] = value
            elif field.type == FieldDescriptor.TYPE_MESSAGE:
                if field.label == FieldDescriptor.LABEL_REPEATED:
                    dictionary[field.name] = []
            else:  # simple values
                if field.label == FieldDescriptor.LABEL_REPEATED:
                    dictionary[field.name] = []
                else:
                    dictionary[field.name] = field.default_value
        # TODO: Override dictionary values from properties
        return dictionary


def MessageToBinary(message, partial=False):
    """Translates a Google Protocol Buffer Message into its binary
    representation.

    :para message: 
    :para partial: 
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

                                       For more details, see the module documentation ('pydoc protobuf_extra').
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
        stdin = fdopen(0, "rb")
        message = MessageFromBinary(MessageClass, stdin.read())

    if args.output_format == 'ascii':
        print(MessageToString(message))
    elif args.output_format == 'dict':
        print(MessageToDictionary(message))
    elif args.output_format == 'bin':
        # Reopen stdout (fd=1) in binary mode. Also, use write()
        # instead of print.  These together should bypass the Python's
        # helpful universal newline feature.
        stdout = fdopen(1, "wb")
        stdout.write(MessageToBinary(message, partial=args.partial))
