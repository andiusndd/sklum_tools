"""Operators for Object Setting panel"""

import bpy
import mathutils
from bpy.types import Operator
from bpy.props import StringProperty, FloatProperty, EnumProperty

class SKLUM_OT_ObjectRename(Operator):
    """Đổi tên tất cả các đối tượng đang chọn"""
    bl_idname = "sklum.object_rename"
    bl_label = "Rename Objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        settings = context.scene.sklum_object_settings
        new_name = settings.rename_name
        selected = context.selected_objects
        
        if not selected:
            self.report({'WARNING'}, "Không có đối tượng nào được chọn.")
            return {'CANCELLED'}
            
        for obj in selected:
            obj.name = new_name
            
        self.report({'INFO'}, f"Đã đổi tên {len(selected)} đối tượng thành '{new_name}'.")
        return {'FINISHED'}

class SKLUM_OT_SelectByType(Operator):
    """Chọn các đối tượng theo loại"""
    bl_idname = "sklum.select_by_type"
    bl_label = "Select By Type"
    bl_options = {'REGISTER', 'UNDO'}

    type_name: StringProperty()

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        found = False
        for obj in context.scene.objects:
            if obj.type == self.type_name:
                obj.select_set(True)
                context.view_layer.objects.active = obj
                found = True
        
        if not found:
            self.report({'INFO'}, f"Không tìm thấy đối tượng loại {self.type_name}.")
        return {'FINISHED'}

class SKLUM_OT_ApplyTransform(Operator):
    """Áp dụng biến đổi (Apply Transform)"""
    bl_idname = "sklum.apply_transform"
    bl_label = "Apply Transform"
    bl_options = {'REGISTER', 'UNDO'}

    mode: StringProperty() # 'SCALE', 'ROTATION', 'ALL'

    def execute(self, context):
        if not context.selected_objects:
            self.report({'WARNING'}, "Không có đối tượng nào được chọn.")
            return {'CANCELLED'}
            
        if self.mode == 'SCALE':
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        elif self.mode == 'ROTATION':
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        else: # ALL
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            
        return {'FINISHED'}

class SKLUM_OT_QuickOrigin(Operator):
    """Đặt nhanh trọng tâm (Origin)"""
    bl_idname = "sklum.quick_origin"
    bl_label = "Quick Origin"
    bl_options = {'REGISTER', 'UNDO'}

    type: StringProperty() # 'BOTTOM', 'CENTER', 'HEAD'

    def execute(self, context):
        selected = [obj for obj in context.selected_objects if obj.type == 'MESH']
        if not selected:
            return {'CANCELLED'}

        for obj in selected:
            context.view_layer.objects.active = obj
            
            if self.type == 'BOTTOM':
                # Move origin to bottom center of bounding box
                # Save current cursor location
                saved_cursor = context.scene.cursor.location.copy()
                
                # Get bounding box
                bbox_corners = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
                min_z = min(corner.z for corner in bbox_corners)
                center_x = sum(corner.x for corner in bbox_corners) / 8
                center_y = sum(corner.y for corner in bbox_corners) / 8
                
                # Set cursor to bottom center
                context.scene.cursor.location = (center_x, center_y, min_z)
                
                # Set origin to cursor
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
                
                # Restore cursor
                context.scene.cursor.location = saved_cursor
                
            elif self.type == 'CENTER':
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
                
            elif self.type == 'HEAD':
                # Move origin to top center of bounding box
                saved_cursor = context.scene.cursor.location.copy()
                
                bbox_corners = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
                max_z = max(corner.z for corner in bbox_corners)
                center_x = sum(corner.x for corner in bbox_corners) / 8
                center_y = sum(corner.y for corner in bbox_corners) / 8
                
                context.scene.cursor.location = (center_x, center_y, max_z)
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
                context.scene.cursor.location = saved_cursor
                
            elif self.type == 'CUSTOM':
                # Use custom settings from properties
                settings = context.scene.sklum_object_settings
                saved_cursor = context.scene.cursor.location.copy()
                
                # Get World Space BBox Corners
                bbox_corners = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
                
                min_x = min(c.x for c in bbox_corners)
                max_x = max(c.x for c in bbox_corners)
                center_x = (min_x + max_x) / 2.0
                
                min_y = min(c.y for c in bbox_corners)
                max_y = max(c.y for c in bbox_corners)
                center_y = (min_y + max_y) / 2.0
                
                min_z = min(c.z for c in bbox_corners)
                max_z = max(corner.z for corner in bbox_corners)
                center_z = (min_z + max_z) / 2.0

                # X
                if settings.origin_align_x == 'MIN': x_pos = min_x
                elif settings.origin_align_x == 'MAX': x_pos = max_x
                else: x_pos = center_x
                
                # Y
                if settings.origin_align_y == 'MIN': y_pos = min_y
                elif settings.origin_align_y == 'MAX': y_pos = max_y
                else: y_pos = center_y
                
                # Z
                if settings.origin_align_z == 'MIN': z_pos = min_z
                elif settings.origin_align_z == 'MAX': z_pos = max_z
                else: z_pos = center_z
                
                context.scene.cursor.location = (x_pos, y_pos, z_pos)
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
                context.scene.cursor.location = saved_cursor
                
        return {'FINISHED'}

class SKLUM_OT_ShadingUpdate(Operator):
    """Cập nhật Shading (Flip Normal, Auto Smooth, etc.)"""
    bl_idname = "sklum.shading_update"
    bl_label = "Shading Update"
    bl_options = {'REGISTER', 'UNDO'}

    action: StringProperty()

    def execute(self, context):
        if not context.selected_objects:
            return {'CANCELLED'}
            
        for obj in context.selected_objects:
            if obj.type != 'MESH': continue
            context.view_layer.objects.active = obj
            
            if self.action == 'FLIP':
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.flip_normals()
                bpy.ops.object.mode_set(mode='OBJECT')
            elif self.action == 'AUTOSMOOTH':
                obj.data.use_auto_smooth = True # For older versions, in 4.1+ it's a modifier or different
                # We should handle Blender 4.1+ Auto Smooth if necessary
                pass
            elif self.action == 'MARK_SHARP':
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.mark_sharp()
                bpy.ops.object.mode_set(mode='OBJECT')
            elif self.action == 'CLEAR_SHARP':
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.mark_sharp(clear=True)
                bpy.ops.object.mode_set(mode='OBJECT')
                
        return {'FINISHED'}

class SKLUM_OT_MaterialAction(Operator):
    """Thao tác với Materials"""
    bl_idname = "sklum.material_action"
    bl_label = "Material Action"
    bl_options = {'REGISTER', 'UNDO'}

    action: StringProperty()

    def execute(self, context):
        selected = context.selected_objects
        if not selected:
            return {'CANCELLED'}

        if self.action == 'REMOVE':
            for obj in selected:
                if obj.type == 'MESH':
                    obj.data.materials.clear()
        elif self.action == 'DISPLAY':
            # Logic: Show material properties tab
            bpy.ops.wm.properties_context_change(context='MATERIAL')
        elif self.action == 'RENAME':
            # Logic: Rename main material to object name
            for obj in selected:
                if obj.active_material:
                    obj.active_material.name = obj.name
        return {'FINISHED'}

class SKLUM_OT_SetLocation(Operator):
    """Đặt vị trí theo trục"""
    bl_idname = "sklum.set_location"
    bl_label = "Set Location"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        settings = context.scene.sklum_object_settings
        axis = settings.location_axis
        val = settings.location_value
        
        for obj in context.selected_objects:
            if axis == 'X': obj.location.x = val
            elif axis == 'Y': obj.location.y = val
            elif axis == 'Z': obj.location.z = val
            elif axis == 'ALL':
                obj.location.x = val
                obj.location.y = val
                obj.location.z = val
        return {'FINISHED'}

class SKLUM_OT_ParentAction(Operator):
    """Thao tác với Parent"""
    bl_idname = "sklum.parent_action"
    bl_label = "Parent Action"
    bl_options = {'REGISTER', 'UNDO'}

    action: StringProperty()

    def execute(self, context):
        if self.action == 'SET':
            bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
        elif self.action == 'CLEAR':
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
        return {'FINISHED'}

class SKLUM_OT_ToggleColor(Operator):
    """Bật/Tắt chế độ màu Random"""
    bl_idname = "sklum.toggle_color"
    bl_label = "Toggle Random Color"
    
    def execute(self, context):
        shading = context.space_data.shading
        if shading.color_type == 'RANDOM':
            shading.color_type = 'MATERIAL' # Revert to default
        else:
            shading.color_type = 'RANDOM'
        return {'FINISHED'}

class SKLUM_OT_ToggleLight(Operator):
    """Bật/Tắt chế độ ánh sáng Flat"""
    bl_idname = "sklum.toggle_light"
    bl_label = "Toggle Flat Light"
    
    def execute(self, context):
        shading = context.space_data.shading
        if shading.light == 'FLAT':
            shading.light = 'STUDIO' # Revert to default
        else:
            shading.light = 'FLAT'
        return {'FINISHED'}

class SKLUM_OT_ToggleGizmo(Operator):
    """Bật/Tắt Gizmo (Move, Rotate, Scale)"""
    bl_idname = "sklum.toggle_gizmo"
    bl_label = "Toggle Gizmo"
    
    type: StringProperty() # 'TRANSLATE', 'ROTATE', 'SCALE'
    
    def execute(self, context):
        gizmo = context.space_data.overlay
        # Note: In Blender, object gizmos are managed via SpaceView3D.show_gizmo_object_*
        # But 'overlay' prop usually covers general visibility. 
        # Actually, these are directly on SpaceView3D or Overlay struct depending on version.
        # Checking 'context.space_data.show_gizmo_object_translate'
        
        space = context.space_data
        if self.type == 'TRANSLATE':
            space.show_gizmo_object_translate = not space.show_gizmo_object_translate
        elif self.type == 'ROTATE':
            space.show_gizmo_object_rotate = not space.show_gizmo_object_rotate
        elif self.type == 'SCALE':
            space.show_gizmo_object_scale = not space.show_gizmo_object_scale
            
        # Ensure main Gizmo toggle is ON if we enable any specific one
        if space.show_gizmo_object_translate or space.show_gizmo_object_rotate or space.show_gizmo_object_scale:
            space.show_gizmo = True
            
        return {'FINISHED'}

classes = (
    SKLUM_OT_ObjectRename,
    SKLUM_OT_SelectByType,
    SKLUM_OT_ApplyTransform,
    SKLUM_OT_QuickOrigin,
    SKLUM_OT_ShadingUpdate,
    SKLUM_OT_MaterialAction,
    SKLUM_OT_SetLocation,
    SKLUM_OT_ParentAction,
    SKLUM_OT_ToggleColor,
    SKLUM_OT_ToggleLight,
    SKLUM_OT_ToggleGizmo,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
