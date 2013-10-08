# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Person.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='Person.proto',
  package='test',
  serialized_pb='\n\x0cPerson.proto\x12\x04test\"0\n\x04\x44\x61te\x12\x0c\n\x04year\x18\x01 \x02(\r\x12\r\n\x05month\x18\x02 \x02(\r\x12\x0b\n\x03\x64\x61y\x18\x03 \x02(\r\"\x8f\x04\n\x06Person\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\x0b\n\x03\x61ge\x18\x02 \x01(\r\x12\x0e\n\x06\x65mails\x18\x03 \x03(\t\x12\x18\n\nis_married\x18\x04 \x01(\x08:\x04true\x12#\n\x06gender\x18\x05 \x01(\x0e\x32\x13.test.Person.Gender\x12-\n\x0bnationality\x18\x06 \x01(\x0e\x32\x18.test.Person.Nationality\x12\x1c\n\x08\x62irthday\x18\x07 \x02(\x0b\x32\n.test.Date\x12\x1e\n\x08\x63hildren\x18\x08 \x03(\x0b\x32\x0c.test.Person\x12\x0c\n\x04\x66lag\x18\t \x01(\x08\x12\x0c\n\x04text\x18\n \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x0b \x01(\x0c\x12\t\n\x01\x64\x18\x0c \x01(\x01\x12\t\n\x01\x66\x18\r \x01(\x02\x12\x0b\n\x03i32\x18\x0e \x01(\x05\x12\x0b\n\x03i64\x18\x0f \x01(\x03\x12\x0b\n\x03u32\x18\x10 \x01(\r\x12\x0b\n\x03u64\x18\x11 \x01(\x04\x12\x0b\n\x03s32\x18\x12 \x01(\x11\x12\x0b\n\x03s64\x18\x13 \x01(\x12\x12\x0b\n\x03\x66\x33\x32\x18\x14 \x01(\x07\x12\x0b\n\x03\x66\x36\x34\x18\x15 \x01(\x06\x12\x0c\n\x04sf32\x18\x16 \x01(\x0f\x12\x0c\n\x04sf64\x18\x17 \x01(\x10\"1\n\x06Gender\x12\x11\n\rHERMAPHRODITE\x10\x00\x12\n\n\x06\x46\x45MALE\x10\x01\x12\x08\n\x04MALE\x10\x02\"7\n\x0bNationality\x12\x0c\n\x08\x44OMESTIC\x10\x00\x12\x0b\n\x07\x46OREIGN\x10\x01\x12\t\n\x05\x41LIEN\x10\x01\x1a\x02\x10\x01')



_PERSON_GENDER = _descriptor.EnumDescriptor(
  name='Gender',
  full_name='test.Person.Gender',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='HERMAPHRODITE', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FEMALE', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MALE', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=494,
  serialized_end=543,
)

_PERSON_NATIONALITY = _descriptor.EnumDescriptor(
  name='Nationality',
  full_name='test.Person.Nationality',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='DOMESTIC', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FOREIGN', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ALIEN', index=2, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=_descriptor._ParseOptions(descriptor_pb2.EnumOptions(), '\020\001'),
  serialized_start=545,
  serialized_end=600,
)


_DATE = _descriptor.Descriptor(
  name='Date',
  full_name='test.Date',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='year', full_name='test.Date.year', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='month', full_name='test.Date.month', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='day', full_name='test.Date.day', index=2,
      number=3, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=22,
  serialized_end=70,
)


_PERSON = _descriptor.Descriptor(
  name='Person',
  full_name='test.Person',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='test.Person.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='age', full_name='test.Person.age', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='emails', full_name='test.Person.emails', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='is_married', full_name='test.Person.is_married', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=True,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='gender', full_name='test.Person.gender', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='nationality', full_name='test.Person.nationality', index=5,
      number=6, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='birthday', full_name='test.Person.birthday', index=6,
      number=7, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='children', full_name='test.Person.children', index=7,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='flag', full_name='test.Person.flag', index=8,
      number=9, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='text', full_name='test.Person.text', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='data', full_name='test.Person.data', index=10,
      number=11, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='d', full_name='test.Person.d', index=11,
      number=12, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='f', full_name='test.Person.f', index=12,
      number=13, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='i32', full_name='test.Person.i32', index=13,
      number=14, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='i64', full_name='test.Person.i64', index=14,
      number=15, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='u32', full_name='test.Person.u32', index=15,
      number=16, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='u64', full_name='test.Person.u64', index=16,
      number=17, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='s32', full_name='test.Person.s32', index=17,
      number=18, type=17, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='s64', full_name='test.Person.s64', index=18,
      number=19, type=18, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='f32', full_name='test.Person.f32', index=19,
      number=20, type=7, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='f64', full_name='test.Person.f64', index=20,
      number=21, type=6, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sf32', full_name='test.Person.sf32', index=21,
      number=22, type=15, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sf64', full_name='test.Person.sf64', index=22,
      number=23, type=16, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _PERSON_GENDER,
    _PERSON_NATIONALITY,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=73,
  serialized_end=600,
)

_PERSON.fields_by_name['gender'].enum_type = _PERSON_GENDER
_PERSON.fields_by_name['nationality'].enum_type = _PERSON_NATIONALITY
_PERSON.fields_by_name['birthday'].message_type = _DATE
_PERSON.fields_by_name['children'].message_type = _PERSON
_PERSON_GENDER.containing_type = _PERSON;
_PERSON_NATIONALITY.containing_type = _PERSON;
DESCRIPTOR.message_types_by_name['Date'] = _DATE
DESCRIPTOR.message_types_by_name['Person'] = _PERSON

class Date(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _DATE

  # @@protoc_insertion_point(class_scope:test.Date)

class Person(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PERSON

  # @@protoc_insertion_point(class_scope:test.Person)


_PERSON_NATIONALITY.has_options = True
_PERSON_NATIONALITY._options = _descriptor._ParseOptions(descriptor_pb2.EnumOptions(), '\020\001')
# @@protoc_insertion_point(module_scope)
