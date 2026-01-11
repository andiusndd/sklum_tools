"""Properties for Object Setting panel"""

import bpy
from bpy.types import PropertyGroup
from bpy.props import (
    StringProperty,
    EnumProperty,
    FloatProperty,
    PointerProperty,
)

class SKLUM_PG_ObjectSettings(PropertyGroup):
    # Rename
    rename_name: StringProperty(
        name="Rename",
        default="model",
        description="Tên mới cho các đối tượng đang chọn"
    )

    # Custom Origin
    # Custom Origin
    origin_align_x: EnumProperty(
        name="X Align",
        items=[
            ('MIN', "Min (-)", "Align to Left/Min X"),
            ('CENTER', "Center", "Align to Center X"),
            ('MAX', "Max (+)", "Align to Right/Max X"),
        ],
        default='CENTER'
    )
    origin_align_y: EnumProperty(
        name="Y Align",
        items=[
            ('MIN', "Min (-)", "Align to Front/Min Y"),
            ('CENTER', "Center", "Align to Center Y"),
            ('MAX', "Max (+)", "Align to Back/Max Y"),
        ],
        default='CENTER'
    )
    origin_align_z: EnumProperty(
        name="Z Align",
        items=[
            ('MIN', "Min (-)", "Align to Bottom/Min Z"),
            ('CENTER', "Center", "Align to Center Z"),
            ('MAX', "Max (+)", "Align to Top/Max Z"),
        ],
        default='MIN'
    )
    # Deprecated: origin_target_mode, origin_target_z, origin_target_xy

    # Set Location
    location_axis: EnumProperty(
        name="Axis",
        items=[
            ('X', "X", "X Axis"),
            ('Y', "Y", "Y Axis"),
            ('Z', "Z", "Z Axis"),
            ('ALL', "All", "All Axes"),
        ],
        default='Z'
    )
    location_value: FloatProperty(
        name="Value",
        default=0.0,
        description="Giá trị vị trí"
    )

classes = (
    SKLUM_PG_ObjectSettings,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.sklum_object_settings = PointerProperty(type=SKLUM_PG_ObjectSettings)

def unregister():
    del bpy.types.Scene.sklum_object_settings
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
