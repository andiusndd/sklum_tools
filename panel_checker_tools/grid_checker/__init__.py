"""Grid Checker section"""

from . import operator

modules = [operator]


def register():
    for module in modules:
        module.register()


def unregister():
    for module in reversed(modules):
        module.unregister()
