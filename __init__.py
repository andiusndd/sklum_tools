bl_info = {
    "name": "SKLUM Tools",
    "version": (2, 8, 0),
    "blender": (4, 2, 0),
    "location": "3D Viewport > Sidebar > SKLUM Tools",
    "description": "Toolkit for mesh, material checking and automation.",
    "category": "3D View",
    "doc_url": "https://github.com/andius/SKLUM_Tools",
}

import bpy
from bpy.app.handlers import persistent
from .core.license_logic import validate_license

from . import core
from . import preferences  # New
from . import panel_checker_tools
from . import panel_import_export
from . import panel_jpg_converter
from . import panel_auto_rename
from . import panel_object_setting
from . import panel_version_info


modules = [
    core,
    preferences,  # New
    panel_checker_tools,
    panel_import_export,
    panel_jpg_converter,
    panel_auto_rename,
    panel_object_setting,
    panel_version_info,
]

@persistent
def auto_activate_license(dummy):
    """Checks for stored license key and validates it on startup."""
    try:
        # Get addon preferences
        # Note: __package__ might be 'SKLUMToolz' or 'SKLUMToolz.something'
        package_name = __name__.split('.')[0]
        prefs = bpy.context.preferences.addons.get(package_name)
        
        if prefs and prefs.preferences.license_key:
            # Validate quietly
            is_valid, message = validate_license(prefs.preferences.license_key)
            if is_valid:
                bpy.context.scene.sklum_license_active = True
                bpy.context.scene.sklum_license_message = message
                print(f"[SKLUM] Auto-activated license: {message}")
            else:
                bpy.context.scene.sklum_license_active = False
                # Silent fail on startup, user will see locked panel
                print(f"[SKLUM] Auto-activation failed: {message}")
    except Exception as e:
        print(f"[SKLUM] Auto-activation error: {e}")


def register():
    for module in modules:
        if hasattr(module, "register"):
            module.register()
    
    if auto_activate_license not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(auto_activate_license)


def unregister():
    if auto_activate_license in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(auto_activate_license)

    for module in reversed(modules):
        if hasattr(module, "unregister"):
            module.unregister()


if __name__ == "__main__":
    register()
