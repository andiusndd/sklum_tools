import bpy
from bpy.types import AddonPreferences
from bpy.props import StringProperty

class SKLUM_Preferences(AddonPreferences):
    bl_idname = __package__

    license_key: StringProperty(
        name="License Key",
        description="License Key for SKLUM Tools",
        subtype='PASSWORD',
        default=""
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "license_key")
