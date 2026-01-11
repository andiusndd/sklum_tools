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
    origin_target_z: EnumProperty(
        name="Z Alignment",
        items=[
            ('BOTTOM', "Bottom", "Align origin to bottom"),
            ('CENTER', "Center", "Align origin to center"),
            ('TOP', "Top", "Align origin to top"),
        ],
        default='BOTTOM'
    )
    origin_target_xy: EnumProperty(
        name="XY Alignment",
        items=[
            ('CENTER', "Center", "Align origin to center on XY"),
            ('ORIGIN', "Origin", "Align origin to zero on XY"),
        ],
        default='CENTER'
    )
    origin_target_mode: EnumProperty(
        name="Mode",
        items=[
            ('MIDDLE', "Middle", "Middle alignment"),
            # Add more if needed based on further requirements
        ],
        default='MIDDLE'
    )

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
