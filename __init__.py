import bpy
import importlib
import sys
import os
from bpy.app.handlers import persistent

# --- Constants ---
ADDON_PACKAGE = __package__
SUB_PACKAGES = [
    "core",
    "panel_checker_tools",
    "panel_auto_rename",
    "panel_import_export",
    "panel_jpg_converter",
    "panel_object_setting",
    "panel_version_info",
]

def _get_all_submodules():
    """Returns a list of all sub-packages that need (un)registration."""
    return [f"{ADDON_PACKAGE}.{pkg}" for pkg in SUB_PACKAGES]

def register():
    """Registers all sub-modules dynamically."""
    # Ensure current directory is in path for relative imports during registration
    addon_dir = os.path.dirname(__file__)
    if addon_dir not in sys.path:
        sys.path.append(addon_dir)

    for sub_pkg_name in _get_all_submodules():
        try:
            # Dynamic lazy loading
            module = importlib.import_module(sub_pkg_name)
            if hasattr(module, "register"):
                module.register()
        except Exception as e:
            print(f"SKLUM Tools: Error registering {sub_pkg_name}: {e}")

    # Auto-activate license on startup
    from .core.license_logic import auto_activate_license
    
    # 1. Run once on startup
    bpy.app.timers.register(auto_activate_license, first_interval=1.0)
    
    # 2. Register handler for File > Open (to persist across file loads)
    @persistent
    def load_post_handler(dummy):
        """Re-run activation after loading a file."""
        # Use a small delay to let Blender fully stabilize context
        bpy.app.timers.register(auto_activate_license, first_interval=1.0)
        
    bpy.app.handlers.load_post.append(load_post_handler)

def unregister():
    """Unregisters all sub-modules in reverse order."""
    for sub_pkg_name in reversed(_get_all_submodules()):
        try:
            if sub_pkg_name in sys.modules:
                module = sys.modules[sub_pkg_name]
                if hasattr(module, "unregister"):
                    module.unregister()
        except Exception as e:
            print(f"SKLUM Tools: Error unregistering {sub_pkg_name}: {e}")
            
    # Shutdown logger to release file locks
    try:
        from .core.logger import logger
        logger.shutdown()
    except Exception as e:
        print(f"SKLUM Tools: Error shutting down logger: {e}")

if __name__ == "__main__":
    register()
