"""Panel: SKLUM - Import/Export"""

from . import operators
from . import panel
from . import properties

modules = [properties, operators, panel]


def register():
    for module in modules:
        module.register()


def unregister():
    for module in reversed(modules):
        module.unregister()
