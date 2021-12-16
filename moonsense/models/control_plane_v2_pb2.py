# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: control_plane_v2.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import validate_pb2 as validate_dot_validate__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='control_plane_v2.proto',
  package='v2.controlplane',
  syntax='proto3',
  serialized_options=b'\n#io.moonsense.models.v2.controlplaneB\024ControlPlaneV2ProtosZ\'moonsense.io/pkg/pb/v2/control-plane;v2',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x16\x63ontrol_plane_v2.proto\x12\x0fv2.controlplane\x1a\x17validate/validate.proto\"\xa7\x01\n\x0f\x44\x61taPlaneRegion\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0b\n\x03url\x18\x02 \x01(\t\x12\x0b\n\x03lat\x18\x03 \x01(\x01\x12\x0b\n\x03lon\x18\x04 \x01(\x01\x12\x0e\n\x06region\x18\x05 \x01(\t\x12\x0e\n\x06labels\x18\x06 \x03(\t\x12\x17\n\x0f\x64\x65\x66\x61ult_primary\x18\x07 \x01(\x08\x12\x16\n\x0e\x64\x65\x66\x61ult_backup\x18\x08 \x01(\x08\x12\x0e\n\x06status\x18\t \x01(\t\"D\n\x19\x44\x61taRegionsLocateResponse\x12\x13\n\x0bprimary_url\x18\x01 \x01(\t\x12\x12\n\nbackup_url\x18\x02 \x01(\t\"L\n\x17\x44\x61taRegionsListResponse\x12\x31\n\x07regions\x18\x01 \x03(\x0b\x32 .v2.controlplane.DataPlaneRegion\"\x80\x01\n\x13TokenUpgradeRequest\x12\x1d\n\x0cpublic_token\x18\x01 \x01(\tB\x07\xfa\x42\x04r\x02 \x01\x12\x0f\n\x07user_id\x18\x02 \x01(\t\x12\x1a\n\x12\x65xpires_in_seconds\x18\x03 \x01(\x05\x12\x1d\n\x15max_idle_time_minutes\x18\x04 \x01(\x05\"0\n\x14TokenUpgradeResponse\x12\x18\n\x10\x61pp_access_token\x18\x01 \x01(\t\"1\n\x15RevokeAppTokenRequest\x12\x18\n\x07user_id\x18\x01 \x01(\tB\x07\xfa\x42\x04r\x02 \x01\x42\x64\n#io.moonsense.models.v2.controlplaneB\x14\x43ontrolPlaneV2ProtosZ\'moonsense.io/pkg/pb/v2/control-plane;v2b\x06proto3'
  ,
  dependencies=[validate_dot_validate__pb2.DESCRIPTOR,])




_DATAPLANEREGION = _descriptor.Descriptor(
  name='DataPlaneRegion',
  full_name='v2.controlplane.DataPlaneRegion',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='v2.controlplane.DataPlaneRegion.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='url', full_name='v2.controlplane.DataPlaneRegion.url', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='lat', full_name='v2.controlplane.DataPlaneRegion.lat', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='lon', full_name='v2.controlplane.DataPlaneRegion.lon', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='region', full_name='v2.controlplane.DataPlaneRegion.region', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='labels', full_name='v2.controlplane.DataPlaneRegion.labels', index=5,
      number=6, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='default_primary', full_name='v2.controlplane.DataPlaneRegion.default_primary', index=6,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='default_backup', full_name='v2.controlplane.DataPlaneRegion.default_backup', index=7,
      number=8, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='status', full_name='v2.controlplane.DataPlaneRegion.status', index=8,
      number=9, type=9, cpp_type=9, label=1,
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
  serialized_start=69,
  serialized_end=236,
)


_DATAREGIONSLOCATERESPONSE = _descriptor.Descriptor(
  name='DataRegionsLocateResponse',
  full_name='v2.controlplane.DataRegionsLocateResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='primary_url', full_name='v2.controlplane.DataRegionsLocateResponse.primary_url', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='backup_url', full_name='v2.controlplane.DataRegionsLocateResponse.backup_url', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_start=238,
  serialized_end=306,
)


_DATAREGIONSLISTRESPONSE = _descriptor.Descriptor(
  name='DataRegionsListResponse',
  full_name='v2.controlplane.DataRegionsListResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='regions', full_name='v2.controlplane.DataRegionsListResponse.regions', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=308,
  serialized_end=384,
)


_TOKENUPGRADEREQUEST = _descriptor.Descriptor(
  name='TokenUpgradeRequest',
  full_name='v2.controlplane.TokenUpgradeRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='public_token', full_name='v2.controlplane.TokenUpgradeRequest.public_token', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\372B\004r\002 \001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='user_id', full_name='v2.controlplane.TokenUpgradeRequest.user_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='expires_in_seconds', full_name='v2.controlplane.TokenUpgradeRequest.expires_in_seconds', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='max_idle_time_minutes', full_name='v2.controlplane.TokenUpgradeRequest.max_idle_time_minutes', index=3,
      number=4, type=5, cpp_type=1, label=1,
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
  serialized_start=387,
  serialized_end=515,
)


_TOKENUPGRADERESPONSE = _descriptor.Descriptor(
  name='TokenUpgradeResponse',
  full_name='v2.controlplane.TokenUpgradeResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='app_access_token', full_name='v2.controlplane.TokenUpgradeResponse.app_access_token', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=517,
  serialized_end=565,
)


_REVOKEAPPTOKENREQUEST = _descriptor.Descriptor(
  name='RevokeAppTokenRequest',
  full_name='v2.controlplane.RevokeAppTokenRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='user_id', full_name='v2.controlplane.RevokeAppTokenRequest.user_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\372B\004r\002 \001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=567,
  serialized_end=616,
)

_DATAREGIONSLISTRESPONSE.fields_by_name['regions'].message_type = _DATAPLANEREGION
DESCRIPTOR.message_types_by_name['DataPlaneRegion'] = _DATAPLANEREGION
DESCRIPTOR.message_types_by_name['DataRegionsLocateResponse'] = _DATAREGIONSLOCATERESPONSE
DESCRIPTOR.message_types_by_name['DataRegionsListResponse'] = _DATAREGIONSLISTRESPONSE
DESCRIPTOR.message_types_by_name['TokenUpgradeRequest'] = _TOKENUPGRADEREQUEST
DESCRIPTOR.message_types_by_name['TokenUpgradeResponse'] = _TOKENUPGRADERESPONSE
DESCRIPTOR.message_types_by_name['RevokeAppTokenRequest'] = _REVOKEAPPTOKENREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DataPlaneRegion = _reflection.GeneratedProtocolMessageType('DataPlaneRegion', (_message.Message,), {
  'DESCRIPTOR' : _DATAPLANEREGION,
  '__module__' : 'control_plane_v2_pb2'
  # @@protoc_insertion_point(class_scope:v2.controlplane.DataPlaneRegion)
  })
_sym_db.RegisterMessage(DataPlaneRegion)

DataRegionsLocateResponse = _reflection.GeneratedProtocolMessageType('DataRegionsLocateResponse', (_message.Message,), {
  'DESCRIPTOR' : _DATAREGIONSLOCATERESPONSE,
  '__module__' : 'control_plane_v2_pb2'
  # @@protoc_insertion_point(class_scope:v2.controlplane.DataRegionsLocateResponse)
  })
_sym_db.RegisterMessage(DataRegionsLocateResponse)

DataRegionsListResponse = _reflection.GeneratedProtocolMessageType('DataRegionsListResponse', (_message.Message,), {
  'DESCRIPTOR' : _DATAREGIONSLISTRESPONSE,
  '__module__' : 'control_plane_v2_pb2'
  # @@protoc_insertion_point(class_scope:v2.controlplane.DataRegionsListResponse)
  })
_sym_db.RegisterMessage(DataRegionsListResponse)

TokenUpgradeRequest = _reflection.GeneratedProtocolMessageType('TokenUpgradeRequest', (_message.Message,), {
  'DESCRIPTOR' : _TOKENUPGRADEREQUEST,
  '__module__' : 'control_plane_v2_pb2'
  # @@protoc_insertion_point(class_scope:v2.controlplane.TokenUpgradeRequest)
  })
_sym_db.RegisterMessage(TokenUpgradeRequest)

TokenUpgradeResponse = _reflection.GeneratedProtocolMessageType('TokenUpgradeResponse', (_message.Message,), {
  'DESCRIPTOR' : _TOKENUPGRADERESPONSE,
  '__module__' : 'control_plane_v2_pb2'
  # @@protoc_insertion_point(class_scope:v2.controlplane.TokenUpgradeResponse)
  })
_sym_db.RegisterMessage(TokenUpgradeResponse)

RevokeAppTokenRequest = _reflection.GeneratedProtocolMessageType('RevokeAppTokenRequest', (_message.Message,), {
  'DESCRIPTOR' : _REVOKEAPPTOKENREQUEST,
  '__module__' : 'control_plane_v2_pb2'
  # @@protoc_insertion_point(class_scope:v2.controlplane.RevokeAppTokenRequest)
  })
_sym_db.RegisterMessage(RevokeAppTokenRequest)


DESCRIPTOR._options = None
_TOKENUPGRADEREQUEST.fields_by_name['public_token']._options = None
_REVOKEAPPTOKENREQUEST.fields_by_name['user_id']._options = None
# @@protoc_insertion_point(module_scope)
