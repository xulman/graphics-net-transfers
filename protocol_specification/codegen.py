# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Runs protoc with the gRPC plugin to generate messages and gRPC stubs."""

from grpc_tools import protoc # type: ignore

protoc.main((
    '',
    '-Iprotocol_specification',
    '--python_out=peer_in_python/',
    '--grpc_python_out=peer_in_python/',
    'buckets_with_graphics.proto',
))


# copy the stub files also into another folder
# and fix one import to allow it to work within Blender
pb_file  = 'buckets_with_graphics_pb2.py'
rpc_file = 'buckets_with_graphics_pb2_grpc.py'
src_fldr = 'peer_in_python'
tgt_fldr = 'display_server_addon'

def fix_import_statement(file: str):
    content = ""
    with open(file, "r") as f:
        content = f.readlines()

    search_str = "import buckets_with_graphics_pb2 as"
    import_line = -1
    import_found = False
    while not import_found and import_line < 50 and import_line < len(content):
        import_line += 1
        import_found = ( content[import_line].find(search_str) == 0 )

    if not import_found:
        print("Warning: failed to find the import line to fix it...")
        return

    # the fix!
    content[import_line] = "from . " + content[import_line]

    with open(file, "w") as f:
        f.writelines(content)


import shutil
shutil.copyfile(f"{src_fldr}/{pb_file}",  f"{tgt_fldr}/{pb_file}")
shutil.copyfile(f"{src_fldr}/{rpc_file}", f"{tgt_fldr}/{rpc_file}")
fix_import_statement(f"{tgt_fldr}/{rpc_file}")
