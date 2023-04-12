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
from . import buckets_with_graphics_pb2_grpc
from . import blender_server_service

defaultServerName = "Blender DisplayServer"
defaultServerBind = '[::]'
defaultServerPort = 9083


class BlenderServerAddon:
    def __init__(self):
        # record the references on these objects
        bpy.types.Scene.BlenderServerAddon = self
        bpy.types.Scene.BlenderServerService = blender_server_service.BlenderServerService()
        self.restart()

    def restart(self, bind = defaultServerBind, port = defaultServerPort):
        # running the server's listening service at a limited parallelism:
        # this setting enables up to 2 simultaneously processed incoming messages,
        # while the system allows to have 3 more (5 in total) pending in the incoming
        # ring, any 6th message will be refused and returned to the sender with
        # RPC status saying "resource is busy"; it doesn't bring any advantage to
        # allow more messages to be simultaneously processed because their processing
        # must inevitably serialize because Blender works in one thread, consequently
        # we want to warn early (and thus keep the number of pending messages low) any
        # future senders when the system (this server) is lacking behind the processing
        # of incoming traffic
        self.server = grpc.server( futures.ThreadPoolExecutor(2,defaultServerName), maximum_concurrent_rpcs=5 )
        buckets_with_graphics_pb2_grpc.add_ClientToServerServicer_to_server(bpy.types.Scene.BlenderServerService,self.server)
        url = f"{bind}:{port}"
        self.server.add_insecure_port(url)
        self.server.start()
        print(f"'{defaultServerName}' is ready and listening at {url}")

    def restart_with_new_service(self, bind = defaultServerBind, port = defaultServerPort):
        bpy.types.Scene.BlenderServerService = blender_server_service.BlenderServerService()
        self.restart(bind, port)

    def stop(self):
        print(f"'{defaultServerName}' is stopping")
        self.server.stop(None)


# -----------------------------------------------------------------
blender_server_addon = None


def register():
    if bpy.app.version[0] < 3 or bpy.app.version[1] < 3:
        print(f"WARNING: DisplayServer needs at least v3.3, hosted now in {bpy.app.version_string}")
    bpy.app.timers.register(delayed_start_server, first_interval=1)

def delayed_start_server():
    global blender_server_addon
    blender_server_addon = BlenderServerAddon()


def unregister():
    global blender_server_addon
    if blender_server_addon is not None:
        blender_server_addon.stop()
        blender_server_addon = None
