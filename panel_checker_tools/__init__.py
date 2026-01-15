"""
Panel: SKLUM - Checker & Tools
Panel chính chứa các công cụ kiểm tra và tiện ích
"""

import importlib

# List of submodules to manage
submodules = [
    'properties',
    'check_all',
    'rename_uvmap',
    'hard_edges',
    'color_space',
    'active_point',
    'seam_sharp',
    'grid_checker',
    'license_manager',
    'panel',
]

def register():
    for name in submodules:
        try:
            # Import on demand to prevent top-level cycles
            module = importlib.import_module(f".{name}", __package__)
            if hasattr(module, 'register'):
                module.register()
        except Exception as e:
            print(f"[SKLUM] [CheckerTools] Error registering {name}: {e}")

def unregister():
    for name in reversed(submodules):
        try:
            # Check if module is still in memory
            full_name = f"{__package__}.{name}"
            module = importlib.import_module(f".{name}", __package__)
            if hasattr(module, 'unregister'):
                module.unregister()
        except Exception as e:
            print(f"[SKLUM] [CheckerTools] Error unregistering {name}: {e}")
