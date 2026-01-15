"""
Addon Preferences - Centralized preference management for SKLUM Tools
"""

import bpy
from bpy.types import AddonPreferences
from bpy.props import StringProperty


class SKLUMToolsPreferences(AddonPreferences):
    """Addon preferences for SKLUM Tools"""
    
    # This bl_idname must match the addon's package name
    # Blender will automatically use __package__ when registering
    bl_idname = __package__.split('.')[0]
    
    # License Key
    license_key: StringProperty(
        name="License Key",
        description="SKLUM Tools license key for activation",
        default="",
        options={'HIDDEN', 'SKIP_SAVE'}  # Don't show in UI, handled by panels
    )
    
    # CSV File Path for Auto Rename feature
    csv_filepath: StringProperty(
        name="CSV File Path",
        description="Path to CSV file containing IDP data for auto-rename",
        default="",
        subtype='FILE_PATH'
    )
    
    def draw(self, context):
        """Draw the preferences panel"""
        layout = self.layout
        
        # License Section
        box = layout.box()
        box.label(text="License Settings", icon='KEY_HLT')
        
        if self.license_key:
            row = box.row()
            row.label(text="License Status: Activated", icon='CHECKMARK')
        else:
            row = box.row()
            row.label(text="License Status: Not Activated", icon='ERROR')
            row = box.row()
            row.label(text="Activate your license in the 3D Viewport > SKLUM Tools panel")
        
        # CSV Path Section
        box = layout.box()
        box.label(text="Auto Rename Settings", icon='FILE_TEXT')
        box.prop(self, "csv_filepath", text="IDP CSV File")


# Classes to register
classes = (
    SKLUMToolsPreferences,
)


def register():
    """Register addon preferences"""
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    """Unregister addon preferences"""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
