"""
Preferences - Addon preferences và settings
"""

import bpy
from bpy.types import AddonPreferences
from bpy.props import StringProperty


class SKLUM_AddonPreferences(AddonPreferences):
    bl_idname = "SKLUMToolz"  # Phải khớp với tên package

    csv_filepath: StringProperty(
        name="IDP CSV File",
        description="Path to the CSV file containing IDP data",
        subtype='FILE_PATH',
        default=""
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "csv_filepath")


# Classes để register
classes = (
    SKLUM_AddonPreferences,
)


def register():
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except ValueError:
            bpy.utils.unregister_class(cls)
            bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
