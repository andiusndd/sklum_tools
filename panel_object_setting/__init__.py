"""Panel: SKLUM - Object Setting"""

from . import properties
from . import operators
from . import ui

modules = [properties, operators, ui]

def register():
    for module in modules:
        module.register()

def unregister():
    for module in reversed(modules):
        module.unregister()
