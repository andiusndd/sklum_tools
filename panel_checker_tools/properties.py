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
    "sklum_seam_check_result",
    "sklum_color_space_check_result",
    "sklum_active_point_check_result",
    "sklum_uvmap_check_result",
    "sklum_uv_outside_check_result",
    "sklum_texture_pack_check_result",
    "sklum_edge_sharp_crease_check_result",
    "sklum_vertex_group_check_result",
    "sklum_modifier_check_result",
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
)


def register():
    Scene = bpy.types.Scene

    Scene.sklum_sharpness_angle = FloatProperty(
        name="Angle Threshold",
        description="Minimum angle để xem là cạnh cứng",
        default=30.0,
        min=0.0,
        max=180.0,
    )

    Scene.sklum_check_all_result = StringProperty(name="Check All Result", default="")
    Scene.sklum_check_all_collapsed = BoolProperty(name="Collapse Check All", default=False)

    Scene.sklum_seam_check_result = StringProperty(default="")
    Scene.sklum_color_space_check_result = StringProperty(default="")
    Scene.sklum_active_point_check_result = StringProperty(default="")
    Scene.sklum_uvmap_check_result = StringProperty(default="")
    Scene.sklum_uv_outside_check_result = StringProperty(default="")
    Scene.sklum_texture_pack_check_result = StringProperty(default="")
    Scene.sklum_edge_sharp_crease_check_result = StringProperty(default="")
    Scene.sklum_vertex_group_check_result = StringProperty(default="")
    Scene.sklum_modifier_check_result = StringProperty(default="")

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
