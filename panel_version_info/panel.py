import bpy
import sys
from bpy.types import Panel, Operator
from ..core.utils import check_for_update, download_and_install_update

# GitHub Repo URL
REPO_URL = "https://github.com/andiusndd/sklum_tools.git"

class SKLUM_UpdateSettings(bpy.types.PropertyGroup):
    is_update_available: bpy.props.BoolProperty(default=False)
    latest_version: bpy.props.StringProperty(default="")
    last_error: bpy.props.StringProperty(default="")
    status_message: bpy.props.StringProperty(default="Click to check for updates")
    is_checking: bpy.props.BoolProperty(default=False)


class SKLUM_OT_check_update(Operator):
    """Kiểm tra bản cập nhật mới từ GitHub"""
    bl_idname = "sklum.check_update"
    bl_label = "Check for Update"
    
    def execute(self, context):
        settings = context.scene.sklum_update_settings
        settings.is_checking = True
        settings.status_message = "Checking..."
        
        # Check update
        available, version, error = check_for_update(REPO_URL)
        
        settings.is_checking = False
        if error:
            settings.last_error = error
            settings.status_message = f"Error: {error}"
            settings.is_update_available = False
        elif available:
            settings.is_update_available = True
            settings.latest_version = version
            settings.status_message = f"New version {version} available!"
        else:
            settings.is_update_available = False
            settings.status_message = "Addon is up to date"
            
        return {'FINISHED'}


class SKLUM_OT_install_update(Operator):
    """Tải và cài đặt bản cập nhật mới"""
    bl_idname = "sklum.install_update"
    bl_label = "Update Now"
    
    def execute(self, context):
        settings = context.scene.sklum_update_settings
        settings.status_message = "Downloading and installing..."
        
        success, message = download_and_install_update(REPO_URL)
        
        if success:
            settings.status_message = message
            self.report({'INFO'}, message)
        else:
            settings.status_message = f"Install failed: {message}"
            self.report({'ERROR'}, message)
            
        return {'FINISHED'}


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

        # Update section
        settings = context.scene.sklum_update_settings
        
        update_box = layout.box()
        update_row = update_box.row(align=True)
        update_row.label(text=settings.status_message, icon='INFO')
        
        if not settings.is_checking:
            update_row.operator("sklum.check_update", text="", icon='FILE_REFRESH')
            
        if settings.is_update_available:
            install_row = update_box.row()
            install_row.operator("sklum.install_update", text="Update Now", icon='IMPORT')


classes = (
    SKLUM_UpdateSettings,
    SKLUM_OT_check_update,
    SKLUM_OT_install_update,
    VIEW3D_PT_sklum_version_info,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.sklum_update_settings = bpy.props.PointerProperty(type=SKLUM_UpdateSettings)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.sklum_update_settings
