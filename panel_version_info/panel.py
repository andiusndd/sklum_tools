import bpy
import sys
from bpy.types import Panel

class VIEW3D_PT_sklum_version_info(Panel):
    """Panel hiển thị thông tin phiên bản Addon"""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SKLUM Tools'
    bl_label = "SKLUM Tools Info"
    bl_options = {'HIDE_HEADER'} # Hide standard header to make it look like a banner
    bl_order = 0 # Attempt to place strictly at top

    def draw(self, context):
        layout = self.layout
        
        # Get version from main package
        version_str = "v?.?.?"
        try:
            from .. import bl_info
            version = bl_info.get("version", (0, 0, 0))
            version_str = f"v{version[0]}.{version[1]}.{version[2]}"
        except Exception as e:
            print(f"Version extraction error: {e}")
            # Fallback if import fails
            version_str = "v2.7.2"

        # Custom Box for Info
        box = layout.box()
        row = box.row()
        row.alignment = 'CENTER'
        # Heart icon requested
        row.label(text=f"SKLUM Tools {version_str}", icon='HEART')


classes = (
    VIEW3D_PT_sklum_version_info,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
