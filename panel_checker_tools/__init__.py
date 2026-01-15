"""
Panel: SKLUM - Checker & Tools
Panel chính chứa các công cụ kiểm tra và tiện ích
"""

from . import properties
from . import panel
from . import check_all
from . import rename_uvmap
from . import hard_edges
from . import color_space
from . import active_point
from . import seam_sharp
from . import grid_checker
from . import license_manager # New


modules = [
    properties,
    check_all,
    rename_uvmap,
    hard_edges,
    color_space,
    active_point,
    seam_sharp,
    grid_checker,
    license_manager, # New
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
