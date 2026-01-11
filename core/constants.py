"""
Constants - Các hằng số dùng chung trong addon
"""

# Addon info
ADDON_NAME = "SKLUM Tools"
ADDON_VERSION = (2, 5, 2)
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
# Format: "Socket Name": (suffix, colorspace, [keywords])
TEXTURE_TYPE_MAPPING = {
    # ===== Main Inputs =====
    "Base Color": ("_Diffuse", COLOR_SPACE_SRGB, ["diffuse", "albedo", "base_color", "basecolor"]),
    "Metallic": ("_RMA", COLOR_SPACE_NON_COLOR, ["metallic", "metal"]),
    "Roughness": ("_RMA", COLOR_SPACE_NON_COLOR, ["roughness", "rough"]),
    "Ambient Occlusion": ("_RMA", COLOR_SPACE_NON_COLOR, ["occlusion", "ao", "ambient_occlusion"]),
    "Alpha": ("_Alpha", COLOR_SPACE_SRGB, ["alpha", "opacity"]),
    "IOR": ("_IOR", COLOR_SPACE_NON_COLOR, ["ior"]),
    "Normal": ("_Normal", COLOR_SPACE_NON_COLOR, ["normal"]),
    
    # ===== Subsurface =====
    "Subsurface Weight": ("_Subsurface", COLOR_SPACE_NON_COLOR, ["subsurface", "sss"]),
    "Subsurface Radius": ("_SubsurfaceRadius", COLOR_SPACE_SRGB, ["subsurface_radius"]),
    "Subsurface Scale": ("_SubsurfaceScale", COLOR_SPACE_NON_COLOR, ["subsurface_scale"]),
    
    # ===== Specular =====
    "Specular IOR Level": ("_Specular", COLOR_SPACE_NON_COLOR, ["specular", "spec"]),
    "Specular Tint": ("_SpecularTint", COLOR_SPACE_SRGB, ["specular_tint"]),
    "Anisotropic": ("_Anisotropic", COLOR_SPACE_NON_COLOR, ["anisotropic", "aniso"]),
    "Anisotropic Rotation": ("_AnisotropicRotation", COLOR_SPACE_NON_COLOR, ["anisotropic_rotation"]),
    
    # ===== Transmission =====
    "Transmission Weight": ("_Transmission", COLOR_SPACE_NON_COLOR, ["transmission", "trans"]),
    
    # ===== Coat =====
    "Coat Weight": ("_Coat", COLOR_SPACE_NON_COLOR, ["coat", "clearcoat"]),
    "Coat Roughness": ("_CoatRoughness", COLOR_SPACE_NON_COLOR, ["coat_roughness"]),
    "Coat IOR": ("_CoatIOR", COLOR_SPACE_NON_COLOR, ["coat_ior"]),
    "Coat Tint": ("_CoatTint", COLOR_SPACE_SRGB, ["coat_tint"]),
    "Coat Normal": ("_CoatNormal", COLOR_SPACE_NON_COLOR, ["coat_normal"]),
    
    # ===== Sheen =====
    "Sheen Weight": ("_Sheen", COLOR_SPACE_NON_COLOR, ["sheen"]),
    "Sheen Roughness": ("_SheenRoughness", COLOR_SPACE_NON_COLOR, ["sheen_roughness"]),
    "Sheen Tint": ("_SheenTint", COLOR_SPACE_SRGB, ["sheen_tint"]),
    
    # ===== Emission =====
    "Emission Color": ("_Emission", COLOR_SPACE_SRGB, ["emission", "emissive", "glow"]),
    "Emission Strength": ("_EmissionStrength", COLOR_SPACE_NON_COLOR, ["emission_strength"]),
    
    # ===== Thin Film =====
    "Thin Film Thickness": ("_ThinFilm", COLOR_SPACE_NON_COLOR, ["thin_film"]),
    "Thin Film IOR": ("_ThinFilmIOR", COLOR_SPACE_NON_COLOR, ["thin_film_ior"]),
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
