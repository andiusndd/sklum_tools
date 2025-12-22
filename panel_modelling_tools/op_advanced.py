import bpy
import bmesh
from mathutils import Vector, Matrix

# --- ADVANCED DIMENSIONS ---

class MODELLING_OT_CreateGhostBounds(bpy.types.Operator):
    bl_idname = "modelling.create_ghost_bounds"
    bl_label = "Create Ghost Bounds"
    bl_description = "Create a wireframe bounding box for dimension reference"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active_obj = context.active_object
        if not active_obj: return {'CANCELLED'}
        
        # Get dimensions and transform
        matrix_world = active_obj.matrix_world.copy()
        local_bbox = [Vector(v) for v in active_obj.bound_box]
        
        # Create cube
        bpy.ops.mesh.primitive_cube_add(size=1)
        ghost = context.active_object
        ghost.name = f"Ghost_{active_obj.name}"
        
        # Match dimensions and position
        x_min = min(v.x for v in local_bbox)
        x_max = max(v.x for v in local_bbox)
        y_min = min(v.y for v in local_bbox)
        y_max = max(v.y for v in local_bbox)
        z_min = min(v.z for v in local_bbox)
        z_max = max(v.z for v in local_bbox)
        
        center_local = Vector(((x_min + x_max)/2, (y_min + y_max)/2, (z_min + z_max)/2))
        size_local = Vector((x_max - x_min, y_max - y_min, z_max - z_min))
        
        ghost.scale = size_local
        ghost.location = matrix_world @ center_local
        ghost.rotation_euler = active_obj.rotation_euler
        
        ghost.display_type = 'WIRE'
        ghost.hide_render = True
        # Keep non-selectable by default? Or just color it
        ghost.color = (0.0, 1.0, 1.0, 0.5) # Cyan
        ghost.show_wire = True
        
        return {'FINISHED'}

# --- PRO SHADING ---

class MODELLING_OT_SmartHardener(bpy.types.Operator):
    bl_idname = "modelling.smart_hardener"
    bl_label = "Smart Hardener"
    bl_description = "Apply Weighted Normal and Sharpen Edges"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                context.view_layer.objects.active = obj
                
                # Apply Weighted Normal modifier if not already present
                if not any(m.type == 'WEIGHTED_NORMAL' for m in obj.modifiers):
                    mod = obj.modifiers.new(name="Weighted Normal", type='WEIGHTED_NORMAL')
                    mod.keep_sharp = True
                
                # Setup Auto Smooth (required for Weighted Normal)
                if hasattr(obj.data, "use_auto_smooth"):
                    obj.data.use_auto_smooth = True
                
                # Clear and Set Sharp Edges based on angle
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.edges_select_sharp(sharpness=0.523599) # 30 deg
                bpy.ops.mesh.mark_sharp()
                bpy.ops.object.mode_set(mode='OBJECT')
                
        return {'FINISHED'}

# --- ADVANCED GEOMETRY ---

class MODELLING_OT_PlanarSnap(bpy.types.Operator):
    bl_idname = "modelling.planar_snap"
    bl_label = "Planar Snap"
    bl_description = "Flatten nearly planar faces to fix shading artifacts"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active_obj = context.active_object
        if not active_obj or active_obj.type != 'MESH':
            return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='EDIT')
        
        # More robust flattening logic using bmesh
        me = active_obj.data
        bm = bmesh.from_edit_mesh(me)
        
        # Group faces by normals (simplified)
        # For each selected face, project verts to its own plane
        selected_faces = [f for f in bm.faces if f.select]
        if not selected_faces:
            selected_faces = bm.faces # If nothing selected, process all
            
        for f in selected_faces:
            center = f.calc_center_median()
            normal = f.normal
            for v in f.verts:
                # Project vertex onto plane
                vec = v.co - center
                dist = vec.dot(normal)
                v.co -= dist * normal
                
        bmesh.update_edit_mesh(me)
        bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}

class MODELLING_OT_AlignToActive(bpy.types.Operator):
    bl_idname = "modelling.align_to_active"
    bl_label = "Align Pivot to Active"
    bl_description = "Align selected object pivots to the active object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active_obj = context.active_object
        if not active_obj: return {'CANCELLED'}
        
        target_matrix = active_obj.matrix_world.copy()
        target_loc = target_matrix.to_translation()
        
        for obj in context.selected_objects:
            if obj == active_obj: continue
            
            old_cursor = context.scene.cursor.location.copy()
            context.scene.cursor.location = target_loc
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            context.scene.cursor.location = old_cursor
            
        return {'FINISHED'}

classes = [
    MODELLING_OT_CreateGhostBounds,
    MODELLING_OT_SmartHardener,
    MODELLING_OT_PlanarSnap,
    MODELLING_OT_AlignToActive,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
