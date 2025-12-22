"""Panel: SKLUM - JPG Converter"""

from . import utils
from . import properties
from . import ui_list
from . import operators
from . import panel

modules = [utils, properties, ui_list, operators, panel]


def register():
    for module in modules:
        if hasattr(module, 'register'):
            module.register()


def unregister():
    for module in reversed(modules):
        if hasattr(module, 'unregister'):
            module.unregister()
