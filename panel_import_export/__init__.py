"""Panel: SKLUM - Import/Export"""

import importlib

submodules = [
    'properties',
    'operators',
    'panel',
]

def register():
    for name in submodules:
        try:
            module = importlib.import_module(f".{name}", __package__)
            if hasattr(module, 'register'):
                module.register()
        except Exception as e:
            print(f"[SKLUM] [ImportExport] Error registering {name}: {e}")

def unregister():
    for name in reversed(submodules):
        try:
            module = importlib.import_module(f".{name}", __package__)
            if hasattr(module, 'unregister'):
                module.unregister()
        except Exception as e:
            print(f"[SKLUM] [ImportExport] Error unregistering {name}: {e}")
