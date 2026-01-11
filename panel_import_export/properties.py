"""Properties for SKLUM - Import/Export panel"""

import bpy
from bpy.props import PointerProperty, FloatProperty, PropertyGroup


class SKLUM_BoxSettings(PropertyGroup):
    box_x: FloatProperty(name="X", default=2.0, unit='LENGTH', description="Chiều rộng (X)")
    box_y: FloatProperty(name="Y", default=1.0, unit='LENGTH', description="Chiều sâu (Y)")
    box_z: FloatProperty(name="Z", default=0.1, unit='LENGTH', description="Chiều cao (Z)")


classes = (
    SKLUM_BoxSettings,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.sklum_box_settings = PointerProperty(type=SKLUM_BoxSettings)


def unregister():
    if hasattr(bpy.types.Scene, 'sklum_box_settings'):
        del bpy.types.Scene.sklum_box_settings
    
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
