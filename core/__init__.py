"""
Core module - Chứa các utilities, constants và configurations dùng chung
"""

import importlib

submodules = [
    'logger',
    'constants',
    'utils',
    'preferences',
    'properties',
]

def register():
    for name in submodules:
        try:
            module = importlib.import_module(f".{name}", __package__)
            if hasattr(module, 'register'):
                module.register()
        except Exception as e:
            print(f"[SKLUM] [Core] Error registering {name}: {e}")

def unregister():
    for name in reversed(submodules):
        try:
            module = importlib.import_module(f".{name}", __package__)
            if hasattr(module, 'unregister'):
                module.unregister()
        except Exception as e:
            print(f"[SKLUM] [Core] Error unregistering {name}: {e}")
