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
import importlib
import time
from bpy.app.handlers import persistent

# Sub-packages to manage
sub_packages = [
    'core',
    'panel_checker_tools',
    'panel_import_export',
    'panel_jpg_converter',
    'panel_auto_rename',
    'panel_object_setting',
    'panel_version_info',
]

def _check_validation_timer():
    """Polls for background validation results without blocking the UI."""
    from .core.license_logic import get_async_result
    from .core.logger import logger
    
    result = get_async_result()
    if result is None:
        return 0.5  # Check again in 0.5s
    
    is_valid, message, timestamp = result
    
    # Update all active scenes (or just current)
    for scene in bpy.data.scenes:
        if hasattr(scene, "sklum"):
            scene.sklum.license_active = is_valid
            scene.sklum.license_message = message
    
    # Update persistent cache
    package_name = __package__.split('.')[0]
    prefs = bpy.context.preferences.addons.get(package_name)
    if prefs:
        prefs.preferences.license_is_valid_cache = is_valid
        prefs.preferences.license_last_validated = timestamp
    
    if is_valid:
        logger.info(f"Background validation successful: {message}")
    else:
        logger.warning(f"Background validation failed: {message}")
        
    return None  # Stop timer

@persistent
def auto_activate_license(dummy):
    """Checks for stored license key and validates it asynchronously."""
    try:
        from .core.license_logic import validate_license_async
        from .core.logger import logger
        
        package_name = __package__.split('.')[0]
        prefs = bpy.context.preferences.addons.get(package_name)
        
        if prefs and prefs.preferences.license_key:
            # CHECK CACHE FIRST (TTL: 24 Hours)
            now = time.time()
            last_val = prefs.preferences.license_last_validated
            is_valid_cache = prefs.preferences.license_is_valid_cache
            
            # If validated within last 24h and was valid, use cache immediately
            if is_valid_cache and (now - last_val < 86400):
                if hasattr(bpy.context.scene, "sklum"):
                    bpy.context.scene.sklum.license_active = True
                    bpy.context.scene.sklum.license_message = "Validated from Cache"
                logger.info("License validated from 24h cache.")
                return 

            # Otherwise, start background validation
            logger.info("Starting background license validation...")
            if hasattr(bpy.context.scene, "sklum"):
                 bpy.context.scene.sklum.license_message = "Validating..."
            
            if validate_license_async(prefs.preferences.license_key):
                # Start polling timer
                if not bpy.app.timers.is_registered(_check_validation_timer):
                    bpy.app.timers.register(_check_validation_timer)
                    
    except Exception as e:
        print(f"[SKLUM] Auto-activation error: {e}")


def register():
    # Register sub-packages
    for name in sub_packages:
        try:
            module = importlib.import_module(f".{name}", __package__)
            if hasattr(module, "register"):
                module.register()
        except Exception as e:
            print(f"[SKLUM] [Root] Error registering {name}: {e}")
    
    if auto_activate_license not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(auto_activate_license)


def unregister():
    if auto_activate_license in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(auto_activate_license)
    
    if bpy.app.timers.is_registered(_check_validation_timer):
        bpy.app.timers.unregister(_check_validation_timer)

    # Unregister in reverse order
    for name in reversed(sub_packages):
        try:
            full_name = f"{__package__}.{name}"
            module = importlib.import_module(f".{name}", __package__)
            if hasattr(module, "unregister"):
                module.unregister()
        except Exception as e:
            print(f"[SKLUM] [Root] Error unregistering {name}: {e}")


if __name__ == "__main__":
    register()
