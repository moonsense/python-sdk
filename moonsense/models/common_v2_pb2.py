# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: common_v2.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='common_v2.proto',
  package='v2.common',
  syntax='proto3',
  serialized_options=b'\n\026io.moonsense.models.v2B\014CommonProtosZ moonsense.io/pkg/pb/v2/common;v2',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0f\x63ommon_v2.proto\x12\tv2.common\"\x07\n\x05\x45mpty\"=\n\rErrorResponse\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\r\n\x05param\x18\x02 \x01(\t\x12\x0f\n\x07message\x18\x03 \x01(\t\"}\n\x11TokenSelfResponse\x12\x0e\n\x06\x61pp_id\x18\x01 \x01(\t\x12\x12\n\nproject_id\x18\x02 \x01(\t\x12\x0e\n\x06scopes\x18\x03 \x01(\t\x12\x0f\n\x07user_id\x18\x04 \x01(\t\x12\x15\n\rcredential_id\x18\x05 \x01(\t\x12\x0c\n\x04type\x18\x06 \x01(\x03*<\n\x0e\x44\x65vicePlatform\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x07\n\x03iOS\x10\x01\x12\x0b\n\x07\x41NDROID\x10\x02\x12\x07\n\x03WEB\x10\x03*\xd9\x02\n\nSensorType\x12\x12\n\x0eUNKNOWN_SENSOR\x10\x00\x12\x0c\n\x08LOCATION\x10\x01\x12\x11\n\rACCELEROMETER\x10\x02\x12\x18\n\x14LINEAR_ACCELEROMETER\x10\x03\x12\x10\n\x0cMAGNETOMETER\x10\x04\x12\r\n\tGYROSCOPE\x10\x05\x12\x0b\n\x07\x42\x41TTERY\x10\x06\x12\x0f\n\x0bORIENTATION\x10\x07\x12\x0f\n\x0bTEMPERATURE\x10\x08\x12\t\n\x05LIGHT\x10\t\x12\x0c\n\x08PRESSURE\x10\n\x12\x0c\n\x08HUMIDITY\x10\x0b\x12\t\n\x05STEPS\x10\x0c\x12\x0e\n\nHEART_RATE\x10\r\x12\x0b\n\x07POINTER\x10\x0e\x12\x0f\n\x0bTEXT_CHANGE\x10\x0f\x12\r\n\tKEY_PRESS\x10\x10\x12\x10\n\x0c\x46OCUS_CHANGE\x10\x11\x12\x0f\n\x0bVIEW_SCROLL\x10\x12\x12\x0f\n\x0bMOUSE_WHEEL\x10\x13\x12\t\n\x05\x43LICK\x10\x14\x42H\n\x16io.moonsense.models.v2B\x0c\x43ommonProtosZ moonsense.io/pkg/pb/v2/common;v2b\x06proto3'
)

_DEVICEPLATFORM = _descriptor.EnumDescriptor(
  name='DevicePlatform',
  full_name='v2.common.DevicePlatform',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='iOS', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ANDROID', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='WEB', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=229,
  serialized_end=289,
)
_sym_db.RegisterEnumDescriptor(_DEVICEPLATFORM)

DevicePlatform = enum_type_wrapper.EnumTypeWrapper(_DEVICEPLATFORM)
_SENSORTYPE = _descriptor.EnumDescriptor(
  name='SensorType',
  full_name='v2.common.SensorType',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN_SENSOR', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='LOCATION', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ACCELEROMETER', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='LINEAR_ACCELEROMETER', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MAGNETOMETER', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='GYROSCOPE', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BATTERY', index=6, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ORIENTATION', index=7, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TEMPERATURE', index=8, number=8,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='LIGHT', index=9, number=9,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PRESSURE', index=10, number=10,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='HUMIDITY', index=11, number=11,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='STEPS', index=12, number=12,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='HEART_RATE', index=13, number=13,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='POINTER', index=14, number=14,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TEXT_CHANGE', index=15, number=15,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='KEY_PRESS', index=16, number=16,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FOCUS_CHANGE', index=17, number=17,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='VIEW_SCROLL', index=18, number=18,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MOUSE_WHEEL', index=19, number=19,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CLICK', index=20, number=20,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=292,
  serialized_end=637,
)
_sym_db.RegisterEnumDescriptor(_SENSORTYPE)

SensorType = enum_type_wrapper.EnumTypeWrapper(_SENSORTYPE)
UNKNOWN = 0
iOS = 1
ANDROID = 2
WEB = 3
UNKNOWN_SENSOR = 0
LOCATION = 1
ACCELEROMETER = 2
LINEAR_ACCELEROMETER = 3
MAGNETOMETER = 4
GYROSCOPE = 5
BATTERY = 6
ORIENTATION = 7
TEMPERATURE = 8
LIGHT = 9
PRESSURE = 10
HUMIDITY = 11
STEPS = 12
HEART_RATE = 13
POINTER = 14
TEXT_CHANGE = 15
KEY_PRESS = 16
FOCUS_CHANGE = 17
VIEW_SCROLL = 18
MOUSE_WHEEL = 19
CLICK = 20



_EMPTY = _descriptor.Descriptor(
  name='Empty',
  full_name='v2.common.Empty',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=30,
  serialized_end=37,
)


_ERRORRESPONSE = _descriptor.Descriptor(
  name='ErrorResponse',
  full_name='v2.common.ErrorResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='v2.common.ErrorResponse.type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='param', full_name='v2.common.ErrorResponse.param', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='message', full_name='v2.common.ErrorResponse.message', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=39,
  serialized_end=100,
)


_TOKENSELFRESPONSE = _descriptor.Descriptor(
  name='TokenSelfResponse',
  full_name='v2.common.TokenSelfResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='app_id', full_name='v2.common.TokenSelfResponse.app_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='project_id', full_name='v2.common.TokenSelfResponse.project_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='scopes', full_name='v2.common.TokenSelfResponse.scopes', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='user_id', full_name='v2.common.TokenSelfResponse.user_id', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='credential_id', full_name='v2.common.TokenSelfResponse.credential_id', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='type', full_name='v2.common.TokenSelfResponse.type', index=5,
      number=6, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=102,
  serialized_end=227,
)

DESCRIPTOR.message_types_by_name['Empty'] = _EMPTY
DESCRIPTOR.message_types_by_name['ErrorResponse'] = _ERRORRESPONSE
DESCRIPTOR.message_types_by_name['TokenSelfResponse'] = _TOKENSELFRESPONSE
DESCRIPTOR.enum_types_by_name['DevicePlatform'] = _DEVICEPLATFORM
DESCRIPTOR.enum_types_by_name['SensorType'] = _SENSORTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), {
  'DESCRIPTOR' : _EMPTY,
  '__module__' : 'common_v2_pb2'
  # @@protoc_insertion_point(class_scope:v2.common.Empty)
  })
_sym_db.RegisterMessage(Empty)

ErrorResponse = _reflection.GeneratedProtocolMessageType('ErrorResponse', (_message.Message,), {
  'DESCRIPTOR' : _ERRORRESPONSE,
  '__module__' : 'common_v2_pb2'
  # @@protoc_insertion_point(class_scope:v2.common.ErrorResponse)
  })
_sym_db.RegisterMessage(ErrorResponse)

TokenSelfResponse = _reflection.GeneratedProtocolMessageType('TokenSelfResponse', (_message.Message,), {
  'DESCRIPTOR' : _TOKENSELFRESPONSE,
  '__module__' : 'common_v2_pb2'
  # @@protoc_insertion_point(class_scope:v2.common.TokenSelfResponse)
  })
_sym_db.RegisterMessage(TokenSelfResponse)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
