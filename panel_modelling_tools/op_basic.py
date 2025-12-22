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
            
            # Reset origin to bottom center
            bpy.context.view_layer.objects.active = obj
            mesh = obj.data
            bottom_z = min((v.co.z for v in mesh.vertices))
            
            # Move origin to bottom center (approximate center for now)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
            
            # Adjust to bottom
            current_origin = obj.location.copy()
            # This logic is a bit complex in Blender API without helper functions
            # Simplified: move mesh up, then move object to 0
            # Better way: using matrix
        
        # Implementation of Floor It logic
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                # Get local bounding box
                local_coords = [v.co for v in obj.data.vertices]
                if not local_coords: continue
                z_min = min(v.z for v in local_coords)
                
                # Update origin to bottom
                bpy.context.scene.cursor.location = obj.matrix_world @ mathutils.Vector((0, 0, z_min))
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
                
                # Move to world origin (Floor)
                obj.location = (0, 0, 0)
        
        return {'FINISHED'}

class MODELLING_OT_PivotToZero(bpy.types.Operator):
    bl_idname = "modelling.pivot_to_zero"
    bl_label = "Pivot to Zero"
    bl_description = "Set Origin to (0,0,0) without moving mesh"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        initial_cursor_loc = context.scene.cursor.location.copy()
        context.scene.cursor.location = (0, 0, 0)
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        context.scene.cursor.location = initial_cursor_loc
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
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.dissolve_degenerate()
        bpy.ops.mesh.delete_loose()
        # Limited dissolve for redundant edges on flat surfaces
        bpy.ops.mesh.dissolve_limited(angle_limit=0.01) 
        bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}

# --- SHADING ---

class MODELLING_OT_AutoSmooth(bpy.types.Operator):
    bl_idname = "modelling.auto_smooth"
    bl_label = "Auto Smooth"
    bl_description = "Toggles auto smooth and sets shading to smooth"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.shade_smooth()
                # Use current Blender 4.2+ method if applicable, 
                # but for simplicity using the standard toggle
                obj.data.use_auto_smooth = True
                if hasattr(obj.data, "auto_smooth_angle"):
                    obj.data.auto_smooth_angle = 0.523599 # 30 degrees
        return {'FINISHED'}

classes = [
    MODELLING_OT_FloorIt,
    MODELLING_OT_PivotToZero,
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
