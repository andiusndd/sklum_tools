import bpy
from . import properties
from . import op_basic
from . import op_advanced
from . import panel

modules = [
    properties,
    op_basic,
    op_advanced,
    panel,
]

def register():
    for module in modules:
        if hasattr(module, 'register'):
            module.register()

def unregister():
    for module in reversed(modules):
        if hasattr(module, 'unregister'):
            module.unregister()
