"""Panel: SKLUM - Auto Rename"""

from . import utils
from . import properties
from . import ui_list
from . import menus
from . import operators
from . import handlers
from . import panel

modules = [utils, properties, ui_list, menus, operators, handlers, panel]


def register():
    for module in modules:
        module.register()


def unregister():
    for module in reversed(modules):
        module.unregister()
