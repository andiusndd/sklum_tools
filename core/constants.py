"""
Constants - Các hằng số dùng chung trong addon
"""

# Addon info
ADDON_NAME = "SKLUM Tools"
ADDON_VERSION = (2, 5, 1)
ADDON_CATEGORY = "SKLUM Tools"

# Tolerance values
ORIGIN_TOLERANCE = 0.0001

# Default values
DEFAULT_HARD_EDGE_ANGLE = 30.0
DEFAULT_UVMAP_NAME = "UVMap"

# Color space standards
COLOR_SPACE_SRGB = "sRGB"
COLOR_SPACE_NON_COLOR = "Non-Color"

# Base Color texture keywords (case-insensitive)
BASE_COLOR_KEYWORDS = [
    "base", "basecolor", "base_color", "diffuse", 
    "albedo", "color", "col"
]

# Texture type mapping dùng chung cho color space và auto rename
TEXTURE_TYPE_MAPPING = {
    "Base Color": ("_Diffuse", COLOR_SPACE_SRGB, ["diffuse", "albedo", "base_color"]),
    "Metallic": ("_RMA", COLOR_SPACE_NON_COLOR, ["metallic", "rma"]),
    "Roughness": ("_RMA", COLOR_SPACE_NON_COLOR, ["roughness"]),
    "Alpha": ("_Alpha", COLOR_SPACE_SRGB, ["alpha"]),
}

NORMAL_MAP_CONFIG = ("_Normal", COLOR_SPACE_NON_COLOR, ["normal"])

# Grid check modes
GRID_MODE_TRIANGLE = 'TRIANGLE'
GRID_MODE_NGON = 'N-GON'

# Export settings
EXPORT_FBX_SETTINGS = {
    'use_selection': True,
    'global_scale': 1.0,
    'apply_unit_scale': True,
    'apply_scale_options': 'FBX_SCALE_NONE',
    'bake_space_transform': False,
    'object_types': {'MESH'},
    'use_mesh_modifiers': True,
    'mesh_smooth_type': 'OFF',
    'use_tspace': False,
    'use_custom_props': False,
    'path_mode': 'AUTO',
}

EXPORT_GLB_SETTINGS = {
    'use_selection': True,
    'export_format': 'GLB',
    'export_apply': True,
}
