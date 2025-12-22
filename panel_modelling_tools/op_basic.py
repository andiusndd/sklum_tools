import bpy
import mathutils

# --- PIVOT TOOLS ---

class MODELLING_OT_FloorIt(bpy.types.Operator):
    bl_idname = "modelling.floor_it"
    bl_label = "Floor It"
    bl_description = "Move pivot to bottom center and object to world origin"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type != 'MESH': continue
            
            # Use bbox to find bottom center
            matrix_world = obj.matrix_world
            local_bbox = [Vector(v) for v in obj.bound_box]
            
            # Bottom center in local space
            z_min = min(v.z for v in local_bbox)
            bottom_center_local = Vector((0, 0, z_min)) # Assuming 0,0 is center in local
            
            # Alternative: average of X and Y
            x_min = min(v.x for v in local_bbox)
            x_max = max(v.x for v in local_bbox)
            y_min = min(v.y for v in local_bbox)
            y_max = max(v.y for v in local_bbox)
            bottom_center_local = Vector(((x_min + x_max)/2, (y_min + y_max)/2, z_min))
            
            # World location of bottom center
            world_bottom_center = matrix_world @ bottom_center_local
            
            # Set cursor to that point and set origin
            old_cursor_loc = context.scene.cursor.location.copy()
            context.scene.cursor.location = world_bottom_center
            
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            
            # Move object to world origin
            obj.location = (0, 0, 0)
            
            # Restore cursor
            context.scene.cursor.location = old_cursor_loc
            
        return {'FINISHED'}

class MODELLING_OT_PivotToZero(bpy.types.Operator):
    bl_idname = "modelling.pivot_to_zero"
    bl_label = "Pivot to Zero"
    bl_description = "Set Origin to (0,0,0) without moving mesh"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        old_cursor_loc = context.scene.cursor.location.copy()
        context.scene.cursor.location = (0, 0, 0)
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        context.scene.cursor.location = old_cursor_loc
        return {'FINISHED'}

class MODELLING_OT_NinePointPivot(bpy.types.Operator):
    bl_idname = "modelling.nine_point_pivot"
    bl_label = "9-Point Pivot"
    bl_description = "Set pivot to specialized points on bounding box"
    bl_options = {'REGISTER', 'UNDO'}
    
    point: bpy.props.EnumProperty(
        items=[
            ('BOTTOM_CENTER', "Bottom Center", ""),
            ('CENTER', "Center", ""),
            ('TOP_CENTER', "Top Center", ""),
        ],
        default='BOTTOM_CENTER'
    )

    def execute(self, context):
        # Implementation for 9-point pivot (simplified to 3 for now as requested/planned)
        for obj in context.selected_objects:
            if obj.type != 'MESH': continue
            
            local_bbox = [Vector(v) for v in obj.bound_box]
            x_min = min(v.x for v in local_bbox)
            x_max = max(v.x for v in local_bbox)
            y_min = min(v.y for v in local_bbox)
            y_max = max(v.y for v in local_bbox)
            z_min = min(v.z for v in local_bbox)
            z_max = max(v.z for v in local_bbox)
            z_mid = (z_min + z_max) / 2
            x_mid = (x_min + x_max) / 2
            y_mid = (y_min + y_max) / 2
            
            target_local = Vector((x_mid, y_mid, z_min))
            if self.point == 'CENTER':
                target_local = Vector((x_mid, y_mid, z_mid))
            elif self.point == 'TOP_CENTER':
                target_local = Vector((x_mid, y_mid, z_max))
                
            world_target = obj.matrix_world @ target_local
            
            old_cursor = context.scene.cursor.location.copy()
            context.scene.cursor.location = world_target
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            context.scene.cursor.location = old_cursor
            
        return {'FINISHED'}

# --- MESH QUICK-FIX ---

class MODELLING_OT_DeleteInterior(bpy.types.Operator):
    bl_idname = "modelling.delete_interior"
    bl_label = "Delete Interior"
    bl_description = "Remove interior faces"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_interior_faces()
        bpy.ops.mesh.delete(type='FACE')
        bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}

class MODELLING_OT_QuickCleanup(bpy.types.Operator):
    bl_idname = "modelling.quick_cleanup"
    bl_label = "Quick Cleanup"
    bl_description = "Dissolve redundant edges and degenerate geometry"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type != 'MESH': continue
            context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.dissolve_degenerate()
            bpy.ops.mesh.delete_loose()
            bpy.ops.mesh.dissolve_limited(angle_limit=0.01) 
            bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}

# --- SHADING ---

class MODELLING_OT_AutoSmooth(bpy.types.Operator):
    bl_idname = "modelling.auto_smooth"
    bl_label = "Auto Smooth"
    bl_description = "Sets shading to smooth and enables auto smooth"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                context.view_layer.objects.active = obj
                bpy.ops.object.shade_smooth()
                # Compatibility for Blender 4.2+
                if hasattr(obj.data, "use_auto_smooth"):
                    obj.data.use_auto_smooth = True
                    obj.data.auto_smooth_angle = 0.523599 # 30 deg
                else:
                    # New system: check for Smooth by Angle modifier or similar attribute
                    # For now just smooth it.
                    pass
        return {'FINISHED'}

classes = [
    MODELLING_OT_FloorIt,
    MODELLING_OT_PivotToZero,
    MODELLING_OT_NinePointPivot,
    MODELLING_OT_DeleteInterior,
    MODELLING_OT_QuickCleanup,
    MODELLING_OT_AutoSmooth,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
