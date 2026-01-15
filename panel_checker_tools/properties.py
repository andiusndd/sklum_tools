"""Scene properties dành riêng cho panel Checker & Tools"""

import bpy
from bpy.props import (
    FloatProperty,
    StringProperty,
    BoolProperty,
    EnumProperty,
)


PROPERTY_NAMES = (
    "sklum_sharpness_angle",
    "sklum_check_all_result",
    "sklum_check_all_collapsed",
    "sklum_license_key",
    "sklum_license_active",
    "sklum_license_message",
    "sklum_seam_check_result",
    "sklum_color_space_check_result",
    "sklum_active_point_check_result",
    "sklum_ui_rename_expand",
    "sklum_ui_hard_edges_expand",
    "sklum_ui_color_space_expand",
    "sklum_ui_active_point_expand",
    "sklum_ui_seam_sharp_expand",
    "sklum_ui_grid3_expand",
    "sklum_seam_needs_mark",
    "sklum_color_space_needs_fix",
    "sklum_active_point_needs_fix",
    "sklum_grid3_mode",
    "sklum_grid3_check_result",
    "sklum_check_results_data", # New
)


class SKLUM_CheckResultItem(bpy.types.PropertyGroup):
    """Stores result of a single check"""
    # Name is automatic in CollectionProperty but we can have a explicit ID
    label: StringProperty(name="Label")
    status: BoolProperty(name="Status") # True=OK
    message: StringProperty(name="Message")
    # Store list of objects as a simplified string for now, or detailed list later
    failed_count: bpy.props.IntProperty(default=0)


def register():
    bpy.utils.register_class(SKLUM_CheckResultItem)
    Scene = bpy.types.Scene

    Scene.sklum_check_results_data = bpy.props.CollectionProperty(type=SKLUM_CheckResultItem)

    Scene.sklum_sharpness_angle = FloatProperty(
        name="Angle Threshold",
        description="Minimum angle để xem là cạnh cứng",
        default=30.0,
        min=0.0,
        max=180.0,
    )

    Scene.sklum_check_all_result = StringProperty(name="Check All Result", default="")
    Scene.sklum_check_all_collapsed = BoolProperty(name="Collapse Check All", default=False)
    
    # License Properties
    Scene.sklum_license_key = StringProperty(
        name="License Key",
        description="Nhập License Key để kích hoạt Addon",
        subtype='PASSWORD'
    )
    Scene.sklum_license_active = BoolProperty(
        name="License Active",
        default=False
    )
    Scene.sklum_license_message = StringProperty(default="")

    Scene.sklum_seam_check_result = StringProperty(default="")
    Scene.sklum_color_space_check_result = StringProperty(default="")
    Scene.sklum_active_point_check_result = StringProperty(default="")
    # Migrated properties removed
    
    Scene.sklum_ui_rename_expand = BoolProperty(default=False)
    Scene.sklum_ui_hard_edges_expand = BoolProperty(default=False)
    Scene.sklum_ui_color_space_expand = BoolProperty(default=False)
    Scene.sklum_ui_active_point_expand = BoolProperty(default=False)
    Scene.sklum_ui_seam_sharp_expand = BoolProperty(default=False)
    Scene.sklum_ui_grid3_expand = BoolProperty(default=False)

    Scene.sklum_seam_needs_mark = BoolProperty(default=False)
    Scene.sklum_color_space_needs_fix = BoolProperty(default=False)
    Scene.sklum_active_point_needs_fix = BoolProperty(default=False)

    Scene.sklum_grid3_mode = EnumProperty(
        name="Grid Check Mode",
        items=[
            ('TRIANGLE', 'Triangle', 'Kiểm tra tam giác'),
            ('N-GON', 'N-gon', 'Kiểm tra đa giác > 4 cạnh'),
        ],
        default='TRIANGLE',
    )
    Scene.sklum_grid3_check_result = StringProperty(default="")


def unregister():
    Scene = bpy.types.Scene

    for name in PROPERTY_NAMES:
        if hasattr(Scene, name):
            delattr(Scene, name)
            
    bpy.utils.unregister_class(SKLUM_CheckResultItem)
