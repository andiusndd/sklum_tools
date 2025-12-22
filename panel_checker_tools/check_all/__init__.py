"""
Check All section - Operators và utils cho tính năng Check All
"""

from . import operator

modules = [operator]


def register():
    for module in modules:
        module.register()


def unregister():
    for module in reversed(modules):
        module.unregister()
