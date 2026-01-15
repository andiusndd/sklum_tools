
import bpy
from bpy.types import Operator
from ...core import license_logic

class SKLUM_OT_activate_license(Operator):
    """Activate SKLUM Tools License"""
    bl_idname = "sklum.activate_license"
    bl_label = "Kích Hoạt License"
    bl_description = "Kích hoạt bản quyền Addon"
    
    def execute(self, context):
        scene = context.scene
        key = scene.sklum_license_key
        
        is_valid, msg = license_logic.validate_license(key)
        
        scene.sklum_license_message = msg
        scene.sklum_license_active = is_valid
        
        if is_valid:
            # Save key to preferences
            try:
                package_name = __package__.split('.')[0]
                prefs = context.preferences.addons[package_name].preferences
                prefs.license_key = key
            except Exception as e:
                print(f"Failed to save license key: {e}")

            self.report({'INFO'}, "License Activated!")
        else:
            self.report({'ERROR'}, msg)
            
        return {'FINISHED'}

class SKLUM_OT_deactivate_license(Operator):
    """Deactivate License (Logout)"""
    bl_idname = "sklum.deactivate_license"
    bl_label = "Gỡ License"
    bl_description = "Gỡ bản quyền khỏi máy này"
    
    def execute(self, context):
        scene = context.scene
        # For mock phase, just clear locally
        scene.sklum_license_active = False
        scene.sklum_license_key = ""
        scene.sklum_license_message = "Đã gỡ license thành công."
        
        # Clear key from preferences
        try:
            package_name = __package__.split('.')[0]
            prefs = context.preferences.addons[package_name].preferences
            prefs.license_key = ""
        except Exception as e:
            print(f"Failed to clear license key: {e}")

        return {'FINISHED'}

classes = (
    SKLUM_OT_activate_license,
    SKLUM_OT_deactivate_license,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
