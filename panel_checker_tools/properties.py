"""Scene properties dành riêng cho panel Checker & Tools và các module dùng chung"""

import bpy
from bpy.props import (
    FloatProperty,
    StringProperty,
    BoolProperty,
    EnumProperty,
    IntProperty,
    CollectionProperty,
    PointerProperty,
)


class SKLUM_CheckResultItem(bpy.types.PropertyGroup):
    """Stores result of a single check"""
    label: StringProperty(name="Label")
    status: BoolProperty(name="Status") # True=OK
    message: StringProperty(name="Message")
    failed_count: IntProperty(default=0)


class SKLUM_SceneSettings(bpy.types.PropertyGroup):
    """Bản ghi các cài đặt Scene của SKLUM Tools để gom nhóm thuộc tính."""
    
    # License State (Runtime/Scene)
    license_key: StringProperty(
        name="License Key",
        description="Nhập License Key để kích hoạt Addon",
        subtype='PASSWORD'
    )
    license_active: BoolProperty(
        name="License Active",
        default=False
    )
    license_message: StringProperty(default="")

    # Checker Tools Settings
    sharpness_angle: FloatProperty(
        name="Angle Threshold",
        description="Minimum angle để xem là cạnh cứng",
        default=30.0,
        min=0.0,
        max=180.0,
    )

    # Checker Tools Results
    check_all_result: StringProperty(name="Check All Result", default="")
    check_all_collapsed: BoolProperty(name="Collapse Check All", default=False)
    
    check_results_data: CollectionProperty(type=SKLUM_CheckResultItem)
    
    seam_check_result: StringProperty(default="")
    color_space_check_result: StringProperty(default="")
    active_point_check_result: StringProperty(default="")
    
    seam_needs_mark: BoolProperty(default=False)
    color_space_needs_fix: BoolProperty(default=False)
    active_point_needs_fix: BoolProperty(default=False)

    # Grid Checker
    grid3_mode: EnumProperty(
        name="Grid Check Mode",
        items=[
            ('TRIANGLE', 'Triangle', 'Kiểm tra tam giác'),
            ('N-GON', 'N-gon', 'Kiểm tra đa giác > 4 cạnh'),
        ],
        default='TRIANGLE',
    )
    grid3_check_result: StringProperty(default="")

    # UI State (Expands)
    ui_rename_expand: BoolProperty(default=False)
    ui_hard_edges_expand: BoolProperty(default=False)
    ui_color_space_expand: BoolProperty(default=False)
    ui_active_point_expand: BoolProperty(default=False)
    ui_seam_sharp_expand: BoolProperty(default=False)
    ui_grid3_expand: BoolProperty(default=False)


def register():
    bpy.utils.register_class(SKLUM_CheckResultItem)
    bpy.utils.register_class(SKLUM_SceneSettings)
    
    bpy.types.Scene.sklum = PointerProperty(type=SKLUM_SceneSettings)


def unregister():
    if hasattr(bpy.types.Scene, 'sklum'):
        del bpy.types.Scene.sklum
        
    bpy.utils.unregister_class(SKLUM_SceneSettings)
    bpy.utils.unregister_class(SKLUM_CheckResultItem)
