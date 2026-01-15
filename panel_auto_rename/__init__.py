"""Panel: SKLUM - Auto Rename"""

import importlib

submodules = [
    'utils',
    'properties',
    'ui_list',
    'menus',
    'operators',
    'handlers',
    'panel',
]

def register():
    for name in submodules:
        try:
            module = importlib.import_module(f".{name}", __package__)
            if hasattr(module, 'register'):
                module.register()
        except Exception as e:
            print(f"[SKLUM] [AutoRename] Error registering {name}: {e}")

def unregister():
    for name in reversed(submodules):
        try:
            module = importlib.import_module(f".{name}", __package__)
            if hasattr(module, 'unregister'):
                module.unregister()
        except Exception as e:
            print(f"[SKLUM] [AutoRename] Error unregistering {name}: {e}")
