import importlib

def register():
    try:
        module = importlib.import_module(".panel", __package__)
        if hasattr(module, "register"):
            module.register()
    except Exception as e:
        print(f"[SKLUM] [VersionInfo] Error registering panel: {e}")

def unregister():
    try:
        module = importlib.import_module(".panel", __package__)
        if hasattr(module, "unregister"):
            module.unregister()
    except Exception as e:
        print(f"[SKLUM] [VersionInfo] Error unregistering panel: {e}")
