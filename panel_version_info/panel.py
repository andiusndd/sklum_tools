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

def get_local_version():
    """Lấy phiên bản hiện tại từ blender_manifest.toml."""
    try:
        import os
        import tomllib
        addon_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        manifest_path = os.path.join(addon_dir, "blender_manifest.toml")
        with open(manifest_path, "rb") as f:
            data = tomllib.load(f)
        return data.get("version", "0.0.0")
    except Exception as e:
        print(f"Error reading manifest: {e}")
        return "?.?.?"


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
        settings = context.scene.sklum_update_settings
        
        # Get version from local manifest
        version_str = f"v{get_local_version()}"

        # Row 1: Version (Left, faint) + Buttons (Right)
        row1 = layout.row(align=True)
        
        # Left: Version string (Greyed out/faint)
        left = row1.row()
        left.alignment = 'LEFT'
        left.enabled = False
        left.label(text=version_str)
        
        # Right: Buttons clump
        right = row1.row(align=True)
        right.alignment = 'RIGHT'
        
        if settings.is_checking:
            right.label(text="", icon='UI_STATS')
        else:
            # Check/Refresh button
            right.operator("sklum.check_update", text="", icon='FILE_REFRESH')
            
            # Update button only if version is available
            if settings.is_update_available:
                right.operator("sklum.install_update", text="Update", icon='IMPORT')

        # Row 2: Status Message
        row2 = layout.row(align=True)
        # Using a small separator to give it some air if needed, otherwise just label
        row2.label(text=settings.status_message, icon='NONE')
        
        # Separator before License section
        layout.separator()
        
        # LICENSE SECTION
        scene = context.scene
        license_box = layout.box()
        
        if not scene.sklum_license_active:
            # Not activated - show activation form
            license_box.alert = True
            license_box.label(text="⚠️ CHƯA KÍCH HOẠT LICENSE", icon='LOCKED')
            
            license_box.prop(scene, "sklum_license_key", text="License Key")
            
            row = license_box.row(align=True)
            row.operator("sklum.activate_license", text="Kích Hoạt", icon='KEY_HLT')
            
            if scene.sklum_license_message:
                license_box.label(text=scene.sklum_license_message, icon='INFO')
                
            license_box.separator()
            license_box.label(text="Vui lòng kích hoạt để sử dụng các công cụ.")
        else:
            # Activated - show status
            row = license_box.row()
            row.label(text="✅ License Active", icon='UNLOCKED')
            row.operator("sklum.deactivate_license", text="", icon='X')


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
