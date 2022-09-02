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

from . import mb_server


def register():
    mb_server.register()


def unregister():
    mb_server.unregister()
