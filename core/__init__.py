"""
Core module - Chứa các utilities, constants và configurations dùng chung
"""

from . import constants
from . import utils
from . import preferences
from . import properties

__all__ = ['constants', 'utils', 'preferences', 'properties']


modules = [
    constants,
    utils,
    preferences,
    properties,
]


def register():
    for module in modules:
        if hasattr(module, 'register'):
            module.register()


def unregister():
    for module in reversed(modules):
        if hasattr(module, 'unregister'):
            module.unregister()
