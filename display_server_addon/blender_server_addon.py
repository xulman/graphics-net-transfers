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
"""The Python implementation of the GRPC helloworld.ViewService server."""


from concurrent import futures
import grpc
import bpy
import display_server_addon.buckets_with_graphics_pb2_grpc as Gbuckets_with_graphics_pb2_grpc
from . import blender_server_service

serverName = "Blender DisplayServer"
serverPort = 9083


class BlenderServerAddon:
    def __init__(self):
        # running the server's listening service
        self.server = grpc.server( futures.ThreadPoolExecutor(2,serverName) )
        Gbuckets_with_graphics_pb2_grpc.add_ClientToServerServicer_to_server(blender_server_service.BlenderServerService(),self.server)
        self.server.add_insecure_port('[::]:%d'%serverPort)
        self.server.start()
        print(f"'{serverName}' is ready and listening")

    def stop(self):
        print(f"'{serverName}' is stopping")
        self.server.stop(None)


# -----------------------------------------------------------------
blender_server_addon = None


def register():
    bpy.app.timers.register(delayed_start_server, first_interval=1)

def delayed_start_server():
    global blender_server_addon
    blender_server_addon = BlenderServerAddon()


def unregister():
    global blender_server_addon
    if blender_server_addon is not None:
        blender_server_addon.stop()
        blender_server_addon = None
