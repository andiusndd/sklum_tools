"""Rename & UVMap section"""

from . import ui_list
from . import operators

modules = [ui_list, operators]


def register():
    for module in modules:
        module.register()


def unregister():
    for module in reversed(modules):
        module.unregister()
