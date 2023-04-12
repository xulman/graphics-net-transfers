bl_info = {
    "name": "gRPC DisplayServer for Blender Viewing",
    "author": "Vladimir Ulman, Matthias Arzt",
    "version": (0, 2, 1),
    "blender": (3, 3, 0),
    "location": "View3D > DisplayServer",
    "warning": "",
    "wiki_url": "https://github.com/xulman/graphics-net-transfers",
    "category": "3D View"
}

from . import blender_server_addon


def register():
    blender_server_addon.register()


def unregister():
    blender_server_addon.unregister()
