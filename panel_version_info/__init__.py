from . import panel

def register():
    if hasattr(panel, "register"):
        panel.register()

def unregister():
    if hasattr(panel, "unregister"):
        panel.unregister()
