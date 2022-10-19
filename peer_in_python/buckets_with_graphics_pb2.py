# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: buckets_with_graphics.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='buckets_with_graphics.proto',
  package='transfers_graphics_protocol',
  syntax='proto3',
  serialized_options=b'\n)cz.it4i.ulman.transfers.graphics.protocol',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1b\x62uckets_with_graphics.proto\x12\x1btransfers_graphics_protocol\"\x07\n\x05\x45mpty\"*\n\x14\x43lientIdentification\x12\x12\n\nclientName\x18\x01 \x01(\t\"e\n\x0b\x43lientHello\x12\x43\n\x08\x63lientID\x18\x01 \x01(\x0b\x32\x31.transfers_graphics_protocol.ClientIdentification\x12\x11\n\treturnURL\x18\x02 \x01(\t\"\xc5\x01\n\x0f\x42ucketOfSpheres\x12\x43\n\x08\x63lientID\x18\x01 \x01(\x0b\x32\x31.transfers_graphics_protocol.ClientIdentification\x12\x10\n\x08\x62ucketID\x18\x02 \x01(\x04\x12\r\n\x05label\x18\x03 \x01(\t\x12\x0c\n\x04time\x18\x04 \x01(\x04\x12>\n\x07spheres\x18\x05 \x03(\x0b\x32-.transfers_graphics_protocol.SphereParameters\"\xbf\x01\n\rBucketOfLines\x12\x43\n\x08\x63lientID\x18\x01 \x01(\x0b\x32\x31.transfers_graphics_protocol.ClientIdentification\x12\x10\n\x08\x62ucketID\x18\x02 \x01(\x04\x12\r\n\x05label\x18\x03 \x01(\t\x12\x0c\n\x04time\x18\x04 \x01(\x04\x12:\n\x05lines\x18\x05 \x03(\x0b\x32+.transfers_graphics_protocol.LineParameters\"\xc5\x01\n\x0f\x42ucketOfVectors\x12\x43\n\x08\x63lientID\x18\x01 \x01(\x0b\x32\x31.transfers_graphics_protocol.ClientIdentification\x12\x10\n\x08\x62ucketID\x18\x02 \x01(\x04\x12\r\n\x05label\x18\x03 \x01(\t\x12\x0c\n\x04time\x18\x04 \x01(\x04\x12>\n\x07vectors\x18\x05 \x03(\x0b\x32-.transfers_graphics_protocol.VectorParameters\"+\n\x08Vector3D\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02\x12\t\n\x01z\x18\x03 \x01(\x02\"l\n\x10SphereParameters\x12\x35\n\x06\x63\x65ntre\x18\x01 \x01(\x0b\x32%.transfers_graphics_protocol.Vector3D\x12\x0e\n\x06radius\x18\x03 \x01(\x02\x12\x11\n\tcolorXRGB\x18\x04 \x01(\r\"\xa3\x01\n\x0eLineParameters\x12\x37\n\x08startPos\x18\x01 \x01(\x0b\x32%.transfers_graphics_protocol.Vector3D\x12\x35\n\x06\x65ndPos\x18\x02 \x01(\x0b\x32%.transfers_graphics_protocol.Vector3D\x12\x0e\n\x06radius\x18\x03 \x01(\x02\x12\x11\n\tcolorXRGB\x18\x04 \x01(\r\"\xa5\x01\n\x10VectorParameters\x12\x37\n\x08startPos\x18\x01 \x01(\x0b\x32%.transfers_graphics_protocol.Vector3D\x12\x35\n\x06\x65ndPos\x18\x02 \x01(\x0b\x32%.transfers_graphics_protocol.Vector3D\x12\x0e\n\x06radius\x18\x03 \x01(\x02\x12\x11\n\tcolorXRGB\x18\x04 \x01(\r\"\x1a\n\x0bTextMessage\x12\x0b\n\x03msg\x18\x01 \x01(\t\"\x99\x01\n\x11SignedTextMessage\x12\x43\n\x08\x63lientID\x18\x01 \x01(\x0b\x32\x31.transfers_graphics_protocol.ClientIdentification\x12?\n\rclientMessage\x18\x02 \x01(\x0b\x32(.transfers_graphics_protocol.TextMessage\"\x1c\n\nClickedIDs\x12\x0e\n\x06objIDs\x18\x01 \x03(\x04\"\x9a\x01\n\x10SignedClickedIDs\x12\x43\n\x08\x63lientID\x18\x01 \x01(\x0b\x32\x31.transfers_graphics_protocol.ClientIdentification\x12\x41\n\x10\x63lientClickedIDs\x18\x02 \x01(\x0b\x32\'.transfers_graphics_protocol.ClickedIDs2\x96\x07\n\x0e\x43lientToServer\x12\x61\n\x0fintroduceClient\x12(.transfers_graphics_protocol.ClientHello\x1a\".transfers_graphics_protocol.Empty\"\x00\x12\x62\n\naddSpheres\x12,.transfers_graphics_protocol.BucketOfSpheres\x1a\".transfers_graphics_protocol.Empty\"\x00(\x01\x12^\n\x08\x61\x64\x64Lines\x12*.transfers_graphics_protocol.BucketOfLines\x1a\".transfers_graphics_protocol.Empty\"\x00(\x01\x12\x62\n\naddVectors\x12,.transfers_graphics_protocol.BucketOfVectors\x1a\".transfers_graphics_protocol.Empty\"\x00(\x01\x12\x63\n\x0bshowMessage\x12..transfers_graphics_protocol.SignedTextMessage\x1a\".transfers_graphics_protocol.Empty\"\x00\x12\x61\n\nfocusEvent\x12-.transfers_graphics_protocol.SignedClickedIDs\x1a\".transfers_graphics_protocol.Empty\"\x00\x12g\n\x0cunfocusEvent\x12\x31.transfers_graphics_protocol.ClientIdentification\x1a\".transfers_graphics_protocol.Empty\"\x00\x12\x62\n\x0bselectEvent\x12-.transfers_graphics_protocol.SignedClickedIDs\x1a\".transfers_graphics_protocol.Empty\"\x00\x12\x64\n\runselectEvent\x12-.transfers_graphics_protocol.SignedClickedIDs\x1a\".transfers_graphics_protocol.Empty\"\x00\x32\xe4\x03\n\x0eServerToClient\x12]\n\x0bshowMessage\x12(.transfers_graphics_protocol.TextMessage\x1a\".transfers_graphics_protocol.Empty\"\x00\x12[\n\nfocusEvent\x12\'.transfers_graphics_protocol.ClickedIDs\x1a\".transfers_graphics_protocol.Empty\"\x00\x12X\n\x0cunfocusEvent\x12\".transfers_graphics_protocol.Empty\x1a\".transfers_graphics_protocol.Empty\"\x00\x12\\\n\x0bselectEvent\x12\'.transfers_graphics_protocol.ClickedIDs\x1a\".transfers_graphics_protocol.Empty\"\x00\x12^\n\runselectEvent\x12\'.transfers_graphics_protocol.ClickedIDs\x1a\".transfers_graphics_protocol.Empty\"\x00\x42+\n)cz.it4i.ulman.transfers.graphics.protocolb\x06proto3'
)




_EMPTY = _descriptor.Descriptor(
  name='Empty',
  full_name='transfers_graphics_protocol.Empty',
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
  serialized_start=60,
  serialized_end=67,
)


_CLIENTIDENTIFICATION = _descriptor.Descriptor(
  name='ClientIdentification',
  full_name='transfers_graphics_protocol.ClientIdentification',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='clientName', full_name='transfers_graphics_protocol.ClientIdentification.clientName', index=0,
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
  serialized_start=69,
  serialized_end=111,
)


_CLIENTHELLO = _descriptor.Descriptor(
  name='ClientHello',
  full_name='transfers_graphics_protocol.ClientHello',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='clientID', full_name='transfers_graphics_protocol.ClientHello.clientID', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='returnURL', full_name='transfers_graphics_protocol.ClientHello.returnURL', index=1,
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
  serialized_start=113,
  serialized_end=214,
)


_BUCKETOFSPHERES = _descriptor.Descriptor(
  name='BucketOfSpheres',
  full_name='transfers_graphics_protocol.BucketOfSpheres',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='clientID', full_name='transfers_graphics_protocol.BucketOfSpheres.clientID', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bucketID', full_name='transfers_graphics_protocol.BucketOfSpheres.bucketID', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='label', full_name='transfers_graphics_protocol.BucketOfSpheres.label', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='time', full_name='transfers_graphics_protocol.BucketOfSpheres.time', index=3,
      number=4, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='spheres', full_name='transfers_graphics_protocol.BucketOfSpheres.spheres', index=4,
      number=5, type=11, cpp_type=10, label=3,
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
  serialized_start=217,
  serialized_end=414,
)


_BUCKETOFLINES = _descriptor.Descriptor(
  name='BucketOfLines',
  full_name='transfers_graphics_protocol.BucketOfLines',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='clientID', full_name='transfers_graphics_protocol.BucketOfLines.clientID', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bucketID', full_name='transfers_graphics_protocol.BucketOfLines.bucketID', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='label', full_name='transfers_graphics_protocol.BucketOfLines.label', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='time', full_name='transfers_graphics_protocol.BucketOfLines.time', index=3,
      number=4, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='lines', full_name='transfers_graphics_protocol.BucketOfLines.lines', index=4,
      number=5, type=11, cpp_type=10, label=3,
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
  serialized_start=417,
  serialized_end=608,
)


_BUCKETOFVECTORS = _descriptor.Descriptor(
  name='BucketOfVectors',
  full_name='transfers_graphics_protocol.BucketOfVectors',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='clientID', full_name='transfers_graphics_protocol.BucketOfVectors.clientID', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bucketID', full_name='transfers_graphics_protocol.BucketOfVectors.bucketID', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='label', full_name='transfers_graphics_protocol.BucketOfVectors.label', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='time', full_name='transfers_graphics_protocol.BucketOfVectors.time', index=3,
      number=4, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='vectors', full_name='transfers_graphics_protocol.BucketOfVectors.vectors', index=4,
      number=5, type=11, cpp_type=10, label=3,
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
  serialized_start=611,
  serialized_end=808,
)


_VECTOR3D = _descriptor.Descriptor(
  name='Vector3D',
  full_name='transfers_graphics_protocol.Vector3D',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='transfers_graphics_protocol.Vector3D.x', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='y', full_name='transfers_graphics_protocol.Vector3D.y', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='z', full_name='transfers_graphics_protocol.Vector3D.z', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=810,
  serialized_end=853,
)


_SPHEREPARAMETERS = _descriptor.Descriptor(
  name='SphereParameters',
  full_name='transfers_graphics_protocol.SphereParameters',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='centre', full_name='transfers_graphics_protocol.SphereParameters.centre', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='radius', full_name='transfers_graphics_protocol.SphereParameters.radius', index=1,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='colorXRGB', full_name='transfers_graphics_protocol.SphereParameters.colorXRGB', index=2,
      number=4, type=13, cpp_type=3, label=1,
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
  serialized_start=855,
  serialized_end=963,
)


_LINEPARAMETERS = _descriptor.Descriptor(
  name='LineParameters',
  full_name='transfers_graphics_protocol.LineParameters',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='startPos', full_name='transfers_graphics_protocol.LineParameters.startPos', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='endPos', full_name='transfers_graphics_protocol.LineParameters.endPos', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='radius', full_name='transfers_graphics_protocol.LineParameters.radius', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='colorXRGB', full_name='transfers_graphics_protocol.LineParameters.colorXRGB', index=3,
      number=4, type=13, cpp_type=3, label=1,
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
  serialized_start=966,
  serialized_end=1129,
)


_VECTORPARAMETERS = _descriptor.Descriptor(
  name='VectorParameters',
  full_name='transfers_graphics_protocol.VectorParameters',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='startPos', full_name='transfers_graphics_protocol.VectorParameters.startPos', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='endPos', full_name='transfers_graphics_protocol.VectorParameters.endPos', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='radius', full_name='transfers_graphics_protocol.VectorParameters.radius', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='colorXRGB', full_name='transfers_graphics_protocol.VectorParameters.colorXRGB', index=3,
      number=4, type=13, cpp_type=3, label=1,
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
  serialized_start=1132,
  serialized_end=1297,
)


_TEXTMESSAGE = _descriptor.Descriptor(
  name='TextMessage',
  full_name='transfers_graphics_protocol.TextMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='msg', full_name='transfers_graphics_protocol.TextMessage.msg', index=0,
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
  serialized_start=1299,
  serialized_end=1325,
)


_SIGNEDTEXTMESSAGE = _descriptor.Descriptor(
  name='SignedTextMessage',
  full_name='transfers_graphics_protocol.SignedTextMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='clientID', full_name='transfers_graphics_protocol.SignedTextMessage.clientID', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='clientMessage', full_name='transfers_graphics_protocol.SignedTextMessage.clientMessage', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=1328,
  serialized_end=1481,
)


_CLICKEDIDS = _descriptor.Descriptor(
  name='ClickedIDs',
  full_name='transfers_graphics_protocol.ClickedIDs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='objIDs', full_name='transfers_graphics_protocol.ClickedIDs.objIDs', index=0,
      number=1, type=4, cpp_type=4, label=3,
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
  serialized_start=1483,
  serialized_end=1511,
)


_SIGNEDCLICKEDIDS = _descriptor.Descriptor(
  name='SignedClickedIDs',
  full_name='transfers_graphics_protocol.SignedClickedIDs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='clientID', full_name='transfers_graphics_protocol.SignedClickedIDs.clientID', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='clientClickedIDs', full_name='transfers_graphics_protocol.SignedClickedIDs.clientClickedIDs', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=1514,
  serialized_end=1668,
)

_CLIENTHELLO.fields_by_name['clientID'].message_type = _CLIENTIDENTIFICATION
_BUCKETOFSPHERES.fields_by_name['clientID'].message_type = _CLIENTIDENTIFICATION
_BUCKETOFSPHERES.fields_by_name['spheres'].message_type = _SPHEREPARAMETERS
_BUCKETOFLINES.fields_by_name['clientID'].message_type = _CLIENTIDENTIFICATION
_BUCKETOFLINES.fields_by_name['lines'].message_type = _LINEPARAMETERS
_BUCKETOFVECTORS.fields_by_name['clientID'].message_type = _CLIENTIDENTIFICATION
_BUCKETOFVECTORS.fields_by_name['vectors'].message_type = _VECTORPARAMETERS
_SPHEREPARAMETERS.fields_by_name['centre'].message_type = _VECTOR3D
_LINEPARAMETERS.fields_by_name['startPos'].message_type = _VECTOR3D
_LINEPARAMETERS.fields_by_name['endPos'].message_type = _VECTOR3D
_VECTORPARAMETERS.fields_by_name['startPos'].message_type = _VECTOR3D
_VECTORPARAMETERS.fields_by_name['endPos'].message_type = _VECTOR3D
_SIGNEDTEXTMESSAGE.fields_by_name['clientID'].message_type = _CLIENTIDENTIFICATION
_SIGNEDTEXTMESSAGE.fields_by_name['clientMessage'].message_type = _TEXTMESSAGE
_SIGNEDCLICKEDIDS.fields_by_name['clientID'].message_type = _CLIENTIDENTIFICATION
_SIGNEDCLICKEDIDS.fields_by_name['clientClickedIDs'].message_type = _CLICKEDIDS
DESCRIPTOR.message_types_by_name['Empty'] = _EMPTY
DESCRIPTOR.message_types_by_name['ClientIdentification'] = _CLIENTIDENTIFICATION
DESCRIPTOR.message_types_by_name['ClientHello'] = _CLIENTHELLO
DESCRIPTOR.message_types_by_name['BucketOfSpheres'] = _BUCKETOFSPHERES
DESCRIPTOR.message_types_by_name['BucketOfLines'] = _BUCKETOFLINES
DESCRIPTOR.message_types_by_name['BucketOfVectors'] = _BUCKETOFVECTORS
DESCRIPTOR.message_types_by_name['Vector3D'] = _VECTOR3D
DESCRIPTOR.message_types_by_name['SphereParameters'] = _SPHEREPARAMETERS
DESCRIPTOR.message_types_by_name['LineParameters'] = _LINEPARAMETERS
DESCRIPTOR.message_types_by_name['VectorParameters'] = _VECTORPARAMETERS
DESCRIPTOR.message_types_by_name['TextMessage'] = _TEXTMESSAGE
DESCRIPTOR.message_types_by_name['SignedTextMessage'] = _SIGNEDTEXTMESSAGE
DESCRIPTOR.message_types_by_name['ClickedIDs'] = _CLICKEDIDS
DESCRIPTOR.message_types_by_name['SignedClickedIDs'] = _SIGNEDCLICKEDIDS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), {
  'DESCRIPTOR' : _EMPTY,
  '__module__' : 'buckets_with_graphics_pb2'
  # @@protoc_insertion_point(class_scope:transfers_graphics_protocol.Empty)
  })
_sym_db.RegisterMessage(Empty)

ClientIdentification = _reflection.GeneratedProtocolMessageType('ClientIdentification', (_message.Message,), {
  'DESCRIPTOR' : _CLIENTIDENTIFICATION,
  '__module__' : 'buckets_with_graphics_pb2'
  # @@protoc_insertion_point(class_scope:transfers_graphics_protocol.ClientIdentification)
  })
_sym_db.RegisterMessage(ClientIdentification)

ClientHello = _reflection.GeneratedProtocolMessageType('ClientHello', (_message.Message,), {
  'DESCRIPTOR' : _CLIENTHELLO,
  '__module__' : 'buckets_with_graphics_pb2'
  # @@protoc_insertion_point(class_scope:transfers_graphics_protocol.ClientHello)
  })
_sym_db.RegisterMessage(ClientHello)

BucketOfSpheres = _reflection.GeneratedProtocolMessageType('BucketOfSpheres', (_message.Message,), {
  'DESCRIPTOR' : _BUCKETOFSPHERES,
  '__module__' : 'buckets_with_graphics_pb2'
  # @@protoc_insertion_point(class_scope:transfers_graphics_protocol.BucketOfSpheres)
  })
_sym_db.RegisterMessage(BucketOfSpheres)

BucketOfLines = _reflection.GeneratedProtocolMessageType('BucketOfLines', (_message.Message,), {
  'DESCRIPTOR' : _BUCKETOFLINES,
  '__module__' : 'buckets_with_graphics_pb2'
  # @@protoc_insertion_point(class_scope:transfers_graphics_protocol.BucketOfLines)
  })
_sym_db.RegisterMessage(BucketOfLines)

BucketOfVectors = _reflection.GeneratedProtocolMessageType('BucketOfVectors', (_message.Message,), {
  'DESCRIPTOR' : _BUCKETOFVECTORS,
  '__module__' : 'buckets_with_graphics_pb2'
  # @@protoc_insertion_point(class_scope:transfers_graphics_protocol.BucketOfVectors)
  })
_sym_db.RegisterMessage(BucketOfVectors)

Vector3D = _reflection.GeneratedProtocolMessageType('Vector3D', (_message.Message,), {
  'DESCRIPTOR' : _VECTOR3D,
  '__module__' : 'buckets_with_graphics_pb2'
  # @@protoc_insertion_point(class_scope:transfers_graphics_protocol.Vector3D)
  })
_sym_db.RegisterMessage(Vector3D)

SphereParameters = _reflection.GeneratedProtocolMessageType('SphereParameters', (_message.Message,), {
  'DESCRIPTOR' : _SPHEREPARAMETERS,
  '__module__' : 'buckets_with_graphics_pb2'
  # @@protoc_insertion_point(class_scope:transfers_graphics_protocol.SphereParameters)
  })
_sym_db.RegisterMessage(SphereParameters)

LineParameters = _reflection.GeneratedProtocolMessageType('LineParameters', (_message.Message,), {
  'DESCRIPTOR' : _LINEPARAMETERS,
  '__module__' : 'buckets_with_graphics_pb2'
  # @@protoc_insertion_point(class_scope:transfers_graphics_protocol.LineParameters)
  })
_sym_db.RegisterMessage(LineParameters)

VectorParameters = _reflection.GeneratedProtocolMessageType('VectorParameters', (_message.Message,), {
  'DESCRIPTOR' : _VECTORPARAMETERS,
  '__module__' : 'buckets_with_graphics_pb2'
  # @@protoc_insertion_point(class_scope:transfers_graphics_protocol.VectorParameters)
  })
_sym_db.RegisterMessage(VectorParameters)

TextMessage = _reflection.GeneratedProtocolMessageType('TextMessage', (_message.Message,), {
  'DESCRIPTOR' : _TEXTMESSAGE,
  '__module__' : 'buckets_with_graphics_pb2'
  # @@protoc_insertion_point(class_scope:transfers_graphics_protocol.TextMessage)
  })
_sym_db.RegisterMessage(TextMessage)

SignedTextMessage = _reflection.GeneratedProtocolMessageType('SignedTextMessage', (_message.Message,), {
  'DESCRIPTOR' : _SIGNEDTEXTMESSAGE,
  '__module__' : 'buckets_with_graphics_pb2'
  # @@protoc_insertion_point(class_scope:transfers_graphics_protocol.SignedTextMessage)
  })
_sym_db.RegisterMessage(SignedTextMessage)

ClickedIDs = _reflection.GeneratedProtocolMessageType('ClickedIDs', (_message.Message,), {
  'DESCRIPTOR' : _CLICKEDIDS,
  '__module__' : 'buckets_with_graphics_pb2'
  # @@protoc_insertion_point(class_scope:transfers_graphics_protocol.ClickedIDs)
  })
_sym_db.RegisterMessage(ClickedIDs)

SignedClickedIDs = _reflection.GeneratedProtocolMessageType('SignedClickedIDs', (_message.Message,), {
  'DESCRIPTOR' : _SIGNEDCLICKEDIDS,
  '__module__' : 'buckets_with_graphics_pb2'
  # @@protoc_insertion_point(class_scope:transfers_graphics_protocol.SignedClickedIDs)
  })
_sym_db.RegisterMessage(SignedClickedIDs)


DESCRIPTOR._options = None

_CLIENTTOSERVER = _descriptor.ServiceDescriptor(
  name='ClientToServer',
  full_name='transfers_graphics_protocol.ClientToServer',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=1671,
  serialized_end=2589,
  methods=[
  _descriptor.MethodDescriptor(
    name='introduceClient',
    full_name='transfers_graphics_protocol.ClientToServer.introduceClient',
    index=0,
    containing_service=None,
    input_type=_CLIENTHELLO,
    output_type=_EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='addSpheres',
    full_name='transfers_graphics_protocol.ClientToServer.addSpheres',
    index=1,
    containing_service=None,
    input_type=_BUCKETOFSPHERES,
    output_type=_EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='addLines',
    full_name='transfers_graphics_protocol.ClientToServer.addLines',
    index=2,
    containing_service=None,
    input_type=_BUCKETOFLINES,
    output_type=_EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='addVectors',
    full_name='transfers_graphics_protocol.ClientToServer.addVectors',
    index=3,
    containing_service=None,
    input_type=_BUCKETOFVECTORS,
    output_type=_EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='showMessage',
    full_name='transfers_graphics_protocol.ClientToServer.showMessage',
    index=4,
    containing_service=None,
    input_type=_SIGNEDTEXTMESSAGE,
    output_type=_EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='focusEvent',
    full_name='transfers_graphics_protocol.ClientToServer.focusEvent',
    index=5,
    containing_service=None,
    input_type=_SIGNEDCLICKEDIDS,
    output_type=_EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='unfocusEvent',
    full_name='transfers_graphics_protocol.ClientToServer.unfocusEvent',
    index=6,
    containing_service=None,
    input_type=_CLIENTIDENTIFICATION,
    output_type=_EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='selectEvent',
    full_name='transfers_graphics_protocol.ClientToServer.selectEvent',
    index=7,
    containing_service=None,
    input_type=_SIGNEDCLICKEDIDS,
    output_type=_EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='unselectEvent',
    full_name='transfers_graphics_protocol.ClientToServer.unselectEvent',
    index=8,
    containing_service=None,
    input_type=_SIGNEDCLICKEDIDS,
    output_type=_EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_CLIENTTOSERVER)

DESCRIPTOR.services_by_name['ClientToServer'] = _CLIENTTOSERVER


_SERVERTOCLIENT = _descriptor.ServiceDescriptor(
  name='ServerToClient',
  full_name='transfers_graphics_protocol.ServerToClient',
  file=DESCRIPTOR,
  index=1,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=2592,
  serialized_end=3076,
  methods=[
  _descriptor.MethodDescriptor(
    name='showMessage',
    full_name='transfers_graphics_protocol.ServerToClient.showMessage',
    index=0,
    containing_service=None,
    input_type=_TEXTMESSAGE,
    output_type=_EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='focusEvent',
    full_name='transfers_graphics_protocol.ServerToClient.focusEvent',
    index=1,
    containing_service=None,
    input_type=_CLICKEDIDS,
    output_type=_EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='unfocusEvent',
    full_name='transfers_graphics_protocol.ServerToClient.unfocusEvent',
    index=2,
    containing_service=None,
    input_type=_EMPTY,
    output_type=_EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='selectEvent',
    full_name='transfers_graphics_protocol.ServerToClient.selectEvent',
    index=3,
    containing_service=None,
    input_type=_CLICKEDIDS,
    output_type=_EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='unselectEvent',
    full_name='transfers_graphics_protocol.ServerToClient.unselectEvent',
    index=4,
    containing_service=None,
    input_type=_CLICKEDIDS,
    output_type=_EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_SERVERTOCLIENT)

DESCRIPTOR.services_by_name['ServerToClient'] = _SERVERTOCLIENT

# @@protoc_insertion_point(module_scope)
