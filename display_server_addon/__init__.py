bl_info = {
    "name": "Mastodon Blender View",
    "author": "VU after Matthias Arzt",
    "version": (0, 1, 1),
    "blender": (3, 1, 2),
    "location": "View3D > Mastodon",
    "warning": "",
    "wiki_url": "",
    "category": "3D View"
}

from . import blender_server_addon


def register():
    blender_server_addon.register()


def unregister():
    blender_server_addon.unregister()
