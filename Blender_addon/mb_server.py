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
import demo_ng.buckets_with_graphics_pb2_grpc as Gbuckets_with_graphics_pb2_grpc
from . import blender_server_listens

serverName = "Blender server"
serverPort = 9083


class MastodonBlenderServer:
    def __init__(self):
        # running the server's listening service
        self.server = grpc.server( futures.ThreadPoolExecutor(2,serverName) )
        Gbuckets_with_graphics_pb2_grpc.add_ClientToServerServicer_to_server(blender_server_listens.BlenderServerService(),self.server)
        self.server.add_insecure_port('[::]:%d'%serverPort)
        self.server.start()
        print(f"Server '{serverName}' ready and listening")

    def stop(self):
        print(f"Server '{serverName}' is stopping")
        self.server.stop(None)

mastodon_blender_server = None


def register():
    bpy.app.timers.register(delayed_start_server, first_interval=1)


def delayed_start_server():
    global mastodon_blender_server
    mastodon_blender_server = MastodonBlenderServer()


def unregister():
    global mastodon_blender_server
    if mastodon_blender_server is not None:
        mastodon_blender_server.stop()
        mastodon_blender_server = None
