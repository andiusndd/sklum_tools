bl_info = {
    "name": "SKLUM Tools",
    "version": (2, 6, 7),
    "blender": (4, 2, 0),
    "location": "3D Viewport > Sidebar > SKLUM Tools",
    "description": "Toolkit for mesh, material checking and automation.",
    "category": "3D View",
    "doc_url": "https://github.com/andius/SKLUM_Tools",
}

from . import core
from . import panel_checker_tools
from . import panel_import_export
from . import panel_jpg_converter
from . import panel_auto_rename
from . import panel_object_setting


modules = [
    core,
    panel_checker_tools,
    panel_import_export,
    panel_jpg_converter,
    panel_auto_rename,
    panel_object_setting,
]


def register():
    for module in modules:
        if hasattr(module, "register"):
            module.register()


def unregister():
    for module in reversed(modules):
        if hasattr(module, "unregister"):
            module.unregister()


if __name__ == "__main__":
    register()
